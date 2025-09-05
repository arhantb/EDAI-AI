from pathlib import Path
from typing import List, Dict

import time
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
from app.core.sectioning import annotate_sections, summarize_sections


class PipelineEngine:
    def __init__(self, config_path: str | Path):
        self.config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))

    def run(self, input_dir: str | Path, out_dir: str | Path, query: str = "Requirements for the project") -> Dict:
        cfg = self.config
        t0 = time.perf_counter()
        files = list_input_files(input_dir)
        t_load_start = time.perf_counter()
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

        t_embed_start = time.perf_counter()
        embedder = TextEmbedder(cfg["embedding"]["model"])
        embeddings = embedder.embed(
            [c["text"] for c in chunks],
            batch_size=cfg["embedding"].get("batch_size", 64),
        )
        if embeddings.size == 0 or embeddings.ndim != 2:
            return {
                "files": files,
                "num_chunks": len(chunks),
                "num_candidates": 0,
                "validation": {"flags": [], "missing": []},
                "output_dir": str(Path(out_dir)),
                "message": "Failed to compute embeddings. Check model and inputs."
            }

        t_retriever_start = time.perf_counter()
        retriever = FaissRetriever(dim=embeddings.shape[1])
        retriever.add(embeddings, chunks)

        query_vec = embedder.embed([query])
        if query_vec.size == 0:
            query_vec = embeddings[:1]
        results = retriever.search(query_vec, k=cfg["rag"].get("k", 6)) [0]
        contexts = [doc for _score, doc in results]

        t_rag_start = time.perf_counter()
        candidates = synthesize_requirements(query, contexts, cfg["rag"].get("llm_provider"))
        parsed = normalize_and_classify(candidates)
        validation = validate_requirements(parsed)
        prioritized = prioritize(parsed)
        # NLP-based sectioning (with optional external enrichment via env)
        try:
            allow_api = bool(int(str(cfg.get("sectioning", {}).get("allow_api", "1"))))
        except Exception:
            allow_api = True
        prioritized = annotate_sections(prioritized, allow_api=allow_api)
        sections_summary = summarize_sections(prioritized)

        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        if cfg["output"]["generate_docx"]:
            write_docx(prioritized, out / "requirements.docx")
        if cfg["output"]["generate_excel"]:
            write_excel(prioritized, out / "requirements.xlsx")
        if cfg["output"].get("generate_user_stories", True):
            stories = generate_user_stories(prioritized)
            write_user_stories(stories, out / "user_stories.txt")

        timings = {
            "list_files_ms": int((t_load_start - t0) * 1000),
            "load_and_chunk_ms": int((t_embed_start - t_load_start) * 1000),
            "embed_ms": int((t_retriever_start - t_embed_start) * 1000),
            "index_and_search_ms": int((t_rag_start - t_retriever_start) * 1000),
            "rag_nlp_validate_prioritize_ms": None,
            "total_ms": None,
        }
        t_after_outputs = time.perf_counter()
        timings["rag_nlp_validate_prioritize_ms"] = int((t_after_outputs - t_rag_start) * 1000)
        timings["total_ms"] = int((t_after_outputs - t0) * 1000)

        return {
            "files": files,
            "num_chunks": len(chunks),
            "num_candidates": len(candidates),
            "validation": validation,
            "output_dir": str(out),
            "timings": timings,
            "prioritized": prioritized,
            "user_stories": stories if cfg["output"].get("generate_user_stories", True) else [],
            "sections_summary": sections_summary,
        }


