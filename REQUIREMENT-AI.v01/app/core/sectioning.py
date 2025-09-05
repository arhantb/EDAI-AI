from __future__ import annotations

from typing import Dict, List, Optional
import os
import re

try:
    import requests  # type: ignore
except Exception:
    requests = None


OUTLINE_SECTIONS: List[str] = [
    "INTRODUCTION",
    "PROJECT MANAGEMENT APPROACH",
    "PROJECT SCOPE",
    "MILESTONE LIST",
    "SCHEDULE BASELINE AND WORK BREAKDOWN STRUCTURE",
    "CHANGE MANAGEMENT PLAN",
    "COMMUNICATIONS MANAGEMENT PLAN",
    "COST MANAGEMENT PLAN",
    "PROCUREMENT MANAGEMENT PLAN",
    "PROJECT SCOPE MANAGEMENT PLAN",
    "SCHEDULE MANAGEMENT PLAN",
    "QUALITY MANAGEMENT PLAN",
    "RISK MANAGEMENT PLAN",
    "RISK REGISTER",
    "STAFFING MANAGEMENT PLAN",
    "RESOURCE CALENDAR",
    "COST BASELINE",
    "QUALITY BASELINE",
    "SPONSOR ACCEPTANCE",
]


# Simple keyword registry for heuristics
SECTION_KEYWORDS: Dict[str, List[str]] = {
    "INTRODUCTION": ["introduction", "overview", "purpose", "background"],
    "PROJECT MANAGEMENT APPROACH": ["management approach", "project management", "governance"],
    "PROJECT SCOPE": ["scope", "in-scope", "out of scope", "deliverables"],
    "MILESTONE LIST": ["milestone", "milestones", "timeline"],
    "SCHEDULE BASELINE AND WORK BREAKDOWN STRUCTURE": ["schedule baseline", "wbs", "work breakdown"],
    "CHANGE MANAGEMENT PLAN": ["change management", "change control", "change request"],
    "COMMUNICATIONS MANAGEMENT PLAN": ["communication", "stakeholder comms", "status report"],
    "COST MANAGEMENT PLAN": ["cost", "budget", "funding", "estimate"],
    "PROCUREMENT MANAGEMENT PLAN": ["procurement", "vendor", "contract"],
    "PROJECT SCOPE MANAGEMENT PLAN": ["scope management", "requirements management"],
    "SCHEDULE MANAGEMENT PLAN": ["schedule management", "planning", "gantt"],
    "QUALITY MANAGEMENT PLAN": ["quality", "qa", "qc", "acceptance criteria"],
    "RISK MANAGEMENT PLAN": ["risk management", "risk mitigation", "risk response"],
    "RISK REGISTER": ["risk register", "risk id", "probability", "impact"],
    "STAFFING MANAGEMENT PLAN": ["staffing", "resource plan", "roles and responsibilities", "raci"],
    "RESOURCE CALENDAR": ["resource calendar", "availability", "capacity"],
    "COST BASELINE": ["cost baseline", "baseline budget"],
    "QUALITY BASELINE": ["quality baseline", "baseline quality"],
    "SPONSOR ACCEPTANCE": ["sponsor acceptance", "approval", "sign-off", "signoff"],
}


def _heuristic_detect(text: str) -> str:
    t = (text or "").lower()
    # priority: direct section name first
    for sec in OUTLINE_SECTIONS:
        if sec.lower() in t:
            return sec
    # keyword based
    for sec, keys in SECTION_KEYWORDS.items():
        for k in keys:
            if k in t:
                return sec
    return "OTHER"


def _api_detect(text: str, timeout_s: int = 8) -> Optional[str]:
    if requests is None:
        return None
    # 1) Custom enrichment endpoint (highest priority)
    url = os.getenv("REQUIREMENT_SECTION_ENRICH_URL")
    if url:
        try:
            resp = requests.post(url, json={"text": text}, timeout=timeout_s)
            if resp.status_code == 200:
                data = resp.json()
                label = (data.get("section") or "").strip().upper()
                if label in OUTLINE_SECTIONS:
                    return label
        except Exception:
            pass
    # 2) Hugging Face Inference API zero-shot classification (fallback)
    hf_token = os.getenv("HF_API_TOKEN")
    if hf_token:
        try:
            headers = {"Authorization": f"Bearer {hf_token}"}
            zsl_body = {
                "inputs": text,
                "parameters": {
                    "candidate_labels": OUTLINE_SECTIONS,
                    "multi_label": False,
                },
            }
            resp = requests.post(
                "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
                headers=headers,
                json=zsl_body,
                timeout=timeout_s,
            )
            if resp.status_code == 200:
                data = resp.json()
                labels = data.get("labels") or []
                if labels:
                    top = str(labels[0]).strip().upper()
                    if top in OUTLINE_SECTIONS:
                        return top
        except Exception:
            pass
    return None


def detect_section(text: str, allow_api: bool = True) -> str:
    if allow_api:
        label = _api_detect(text)
        if label:
            return label
    return _heuristic_detect(text)


def annotate_sections(requirements: List[Dict], allow_api: bool = True) -> List[Dict]:
    annotated: List[Dict] = []
    for r in requirements:
        section = r.get("section") or detect_section(r.get("text", ""), allow_api=allow_api)
        annotated.append({**r, "section": section})
    return annotated


def summarize_sections(requirements: List[Dict]) -> Dict[str, int]:
    summary: Dict[str, int] = {sec: 0 for sec in OUTLINE_SECTIONS}
    summary["OTHER"] = 0
    for r in requirements:
        sec = r.get("section") or "OTHER"
        if sec not in summary:
            summary[sec] = 0
        summary[sec] += 1
    return summary


