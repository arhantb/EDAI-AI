from typing import List, Dict


MOSCOW_WEIGHTS = {"must": 4, "should": 3, "could": 2, "wont": 1}


def assign_moscow(text: str) -> str:
    lower = text.lower()
    if "must" in lower or "shall" in lower:
        return "must"
    if "should" in lower:
        return "should"
    if "could" in lower:
        return "could"
    return "wont"


def prioritize(reqs: List[Dict]) -> List[Dict]:
    prioritized: List[Dict] = []
    for r in reqs:
        tag = assign_moscow(r["text"]) if "moscow" not in r else r["moscow"]
        score = MOSCOW_WEIGHTS.get(tag, 1)
        prioritized.append({**r, "moscow": tag, "priority_score": score})
    prioritized.sort(key=lambda x: (-x["priority_score"], x["category"]))
    return prioritized


