from pathlib import Path
from typing import List, Dict, Tuple

import faiss
import numpy as np


class FaissRetriever:
    def __init__(self, dim: int, index_path: str | Path | None = None):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.docs: List[Dict] = []
        self.index_path = Path(index_path) if index_path else None

    def add(self, embeddings: np.ndarray, docs: List[Dict]) -> None:
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(np.float32)
        self.index.add(embeddings)
        self.docs.extend(docs)

    def search(self, query_embeddings: np.ndarray, k: int = 6) -> List[List[Tuple[float, Dict]]]:
        if query_embeddings.dtype != np.float32:
            query_embeddings = query_embeddings.astype(np.float32)
        scores, idxs = self.index.search(query_embeddings, k)
        results: List[List[Tuple[float, Dict]]] = []
        for row_scores, row_idxs in zip(scores, idxs):
            results.append([(float(s), self.docs[i]) for s, i in zip(row_scores, row_idxs) if i >= 0 and i < len(self.docs)])
        return results


