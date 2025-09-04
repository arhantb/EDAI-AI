from typing import List, Dict


def simple_chunk(text: str, size: int, overlap: int) -> List[str]:
    if size <= 0:
        return [text]
    chunks: List[str] = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + size, length)
        chunks.append(text[start:end])
        if end == length:
            break
        start = end - overlap if overlap > 0 else end
        if start < 0:
            start = 0
    return chunks


def chunk_document(doc: Dict, size: int, overlap: int) -> List[Dict]:
    text = doc.get("text", "")
    chunks = simple_chunk(text, size=size, overlap=overlap)
    return [{"source": doc.get("source"), "text": c, "meta": {"offset": i}} for i, c in enumerate(chunks)]


