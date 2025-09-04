from pathlib import Path
import argparse
import yaml

from app.ingestion.load import list_input_files, load_and_normalize
from app.ingestion.chunk import chunk_document
from app.core.embedder import TextEmbedder
from app.core.retriever import FaissRetriever


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--index", required=False)
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    files = list_input_files(args.input)
    docs = [load_and_normalize(p) for p in files]

    chunks = []
    for d in docs:
        chunks.extend(chunk_document(d, cfg["chunking"]["size"], cfg["chunking"]["overlap"]))

    embedder = TextEmbedder(cfg["embedding"]["model"])
    X = embedder.embed([c["text"] for c in chunks], batch_size=cfg["embedding"]["batch_size"])

    retriever = FaissRetriever(dim=X.shape[1])
    retriever.add(X, chunks)
    print(f"Indexed {len(chunks)} chunks from {len(files)} files.")


if __name__ == "__main__":
    main()


