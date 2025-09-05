from typing import List, Optional, Tuple, Dict

import threading
import numpy as np


# Process-wide cache for heavy models to avoid repeated loads
_MODEL_CACHE: Dict[Tuple[str, Optional[str]], object] = {}
_CACHE_LOCK = threading.Lock()


def _get_model(model_name: str, device: Optional[str]) -> object:
    key = (model_name, device)
    with _CACHE_LOCK:
        if key in _MODEL_CACHE:
            return _MODEL_CACHE[key]
        # Lazy import to keep module import cheap
        from sentence_transformers import SentenceTransformer  # type: ignore
        model = SentenceTransformer(model_name, device=device)
        _MODEL_CACHE[key] = model
        return model


class TextEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: Optional[str] = None):
        self.model_name = model_name
        self.device = device
        self.model = _get_model(model_name, device)
        # Dimension lookup should be cheap; keep for fast empty-output shape
        self.dim = int(self.model.get_sentence_embedding_dimension())

    def embed(self, texts: List[str], batch_size: int = 64, normalize: bool = True) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dim), dtype=np.float32)
        # sentence-transformers handles internal batching; we pass desired batch_size
        arr = self.model.encode(
            texts,
            batch_size=max(1, int(batch_size)),
            show_progress_bar=False,
            normalize_embeddings=normalize,
            convert_to_numpy=True,
        )
        arr = np.asarray(arr)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.dtype != np.float32:
            arr = arr.astype(np.float32, copy=False)
        return arr


