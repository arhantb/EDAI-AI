from typing import List, Dict

import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def classify_requirement(text: str) -> str:
    lower = text.lower()
    nonfunc_cues = ["performance", "security", "scalability", "availability", "usability", "reliability", "compliance"]
    if any(w in lower for w in nonfunc_cues):
        return "non-functional"
    return "functional"


def normalize_and_classify(lines: List[str]) -> List[Dict]:
    items: List[Dict] = []
    for line in lines:
        norm = clean_text(line)
        if not norm:
            continue
        items.append({
            "text": norm,
            "category": classify_requirement(norm)
        })
    return items


