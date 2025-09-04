from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class TextEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str | None = None):
        self.model = SentenceTransformer(model_name, device=device)
        self.dim = int(self.model.get_sentence_embedding_dimension())

    def embed(self, texts: List[str], batch_size: int = 64) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dim), dtype=np.float32)
        arr = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        arr = np.array(arr)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        return arr.astype(np.float32, copy=False)


