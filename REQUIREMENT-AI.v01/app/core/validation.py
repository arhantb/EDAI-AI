from typing import List, Dict


AMBIGUOUS_TERMS = {"fast", "easy", "user-friendly", "quickly", "optimize", "seamless"}
CONFLICT_TERMS = [("must", "should"), ("must", "could"), ("should", "wont")]


def detect_ambiguity(text: str) -> bool:
    lower = text.lower()
    return any(term in lower for term in AMBIGUOUS_TERMS)


def detect_conflict(a: str, b: str) -> bool:
    la, lb = a.lower(), b.lower()
    for t1, t2 in CONFLICT_TERMS:
        if t1 in la and t2 in lb:
            return True
        if t2 in la and t1 in lb:
            return True
    return False


def validate_requirements(reqs: List[Dict]) -> Dict:
    flags: List[Dict] = []
    # ambiguity
    for i, r in enumerate(reqs):
        if detect_ambiguity(r["text"]):
            flags.append({"type": "ambiguity", "index": i, "text": r["text"]})
    # conflicts (naive O(n^2))
    for i in range(len(reqs)):
        for j in range(i + 1, len(reqs)):
            if detect_conflict(reqs[i]["text"], reqs[j]["text"]):
                flags.append({"type": "conflict", "pair": (i, j)})
    # missing fields heuristic: look for subject + action keywords
    missing: List[int] = []
    for i, r in enumerate(reqs):
        if len(r["text"].split()) < 5:
            missing.append(i)
    return {"flags": flags, "missing": missing}


