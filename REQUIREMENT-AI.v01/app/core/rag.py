from typing import List, Dict


def synthesize_requirements(query: str, contexts: List[Dict], llm_provider: str | None = None) -> List[str]:
    # Placeholder for LLM-based synthesis. For offline mode, compose simple extracts.
    top_contexts = "\n\n".join([c.get("text", "")[:800] for c in contexts[:3]])
    # Minimal heuristic extraction of candidate requirements lines
    lines = [l.strip() for l in top_contexts.splitlines() if len(l.strip()) > 0]
    candidates = [l for l in lines if any(k in l.lower() for k in ["shall", "must", "should", "could"])][:10]
    if not candidates:
        candidates = lines[:10]
    return candidates


