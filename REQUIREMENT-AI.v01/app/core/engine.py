from pathlib import Path
from typing import List, Dict

import yaml

from app.ingestion.load import list_input_files, load_and_normalize
from app.ingestion.chunk import chunk_document
from app.core.embedder import TextEmbedder
from app.core.retriever import FaissRetriever
from app.core.rag import synthesize_requirements
from app.core.nlp import normalize_and_classify
from app.core.validation import validate_requirements
from app.core.prioritization import prioritize
from app.core.output import write_docx, write_excel, generate_user_stories, write_user_stories


class PipelineEngine:
    def __init__(self, config_path: str | Path):
        self.config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))

    def run(self, input_dir: str | Path, out_dir: str | Path, query: str = "Requirements for the project") -> Dict:
        cfg = self.config
        files = list_input_files(input_dir)
        raw_docs = [load_and_normalize(p) for p in files]

        chunks: List[Dict] = []
        for d in raw_docs:
            chunks.extend(chunk_document(d, cfg["chunking"]["size"], cfg["chunking"]["overlap"]))

        if not chunks:
            return {
                "files": files,
                "num_chunks": 0,
                "num_candidates": 0,
                "validation": {"flags": [], "missing": []},
                "output_dir": str(Path(out_dir)),
                "message": "No text extracted from inputs. Ensure docs exist and OCR is configured."
            }

        embedder = TextEmbedder(cfg["embedding"]["model"])
        embeddings = embedder.embed([c["text"] for c in chunks], batch_size=cfg["embedding"]["batch_size"])
        if embeddings.size == 0 or embeddings.ndim != 2:
            return {
                "files": files,
                "num_chunks": len(chunks),
                "num_candidates": 0,
                "validation": {"flags": [], "missing": []},
                "output_dir": str(Path(out_dir)),
                "message": "Failed to compute embeddings. Check model and inputs."
            }

        retriever = FaissRetriever(dim=embeddings.shape[1])
        retriever.add(embeddings, chunks)

        query_vec = embedder.embed([query])
        if query_vec.size == 0:
            query_vec = embeddings[:1]
        results = retriever.search(query_vec, k=cfg["rag"]["k"]) [0]
        contexts = [doc for _score, doc in results]

        candidates = synthesize_requirements(query, contexts, cfg["rag"].get("llm_provider"))
        parsed = normalize_and_classify(candidates)
        validation = validate_requirements(parsed)
        prioritized = prioritize(parsed)

        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        if cfg["output"]["generate_docx"]:
            write_docx(prioritized, out / "requirements.docx")
        if cfg["output"]["generate_excel"]:
            write_excel(prioritized, out / "requirements.xlsx")
        if cfg["output"].get("generate_user_stories", True):
            stories = generate_user_stories(prioritized)
            write_user_stories(stories, out / "user_stories.txt")

        return {
            "files": files,
            "num_chunks": len(chunks),
            "num_candidates": len(candidates),
            "validation": validation,
            "output_dir": str(out)
        }


