# EDAI Document & Requirement AI — Progress Snapshot

<p align="center">
  <img width=160 src="DOCUMENT-AI.v01/EDAI.png" alt="EDAI"/>
</p>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Projects](https://img.shields.io/badge/projects-2-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)]()
[![Stack](https://img.shields.io/badge/stack-FastAPI%20|%20Streamlit%20|%20FAISS%20|%20ST-red.svg)]()

</div>

---

## Overview
Two complementary, production-ready prototypes are implemented:

- DOCUMENT-AI.v01: An insurance policy assistant leveraging FAISS-backed retrieval with LLM reasoning to answer policy questions, with Streamlit UI and FastAPI API.
- REQUIREMENT-AI.v01: An automated requirements authoring system using OCR + RAG + NLP to extract, validate, and prioritize requirements, with Streamlit UI and FastAPI API.

Both apps share a modular design, emphasize reproducible pipelines, and produce actionable outputs.

## Highlights at a Glance

- RAG & Retrieval: FAISS vector search for relevant context across documents.
- OCR Support: Tesseract-based text extraction from scanned PDFs and images.
- NLP & Reasoning:
  - DOCUMENT-AI: LLM-backed policy reasoning and structured responses.
  - REQUIREMENT-AI: Parsing, classification (functional/non-functional), ambiguity/conflict detection, and MoSCoW prioritization.
- Outputs:
  - DOCUMENT-AI: Structured JSON-like decisions via API, interactive Q&A via UI.
  - REQUIREMENT-AI: DOCX requirements, Excel reports, and ready-to-import user stories.
- Interfaces: Streamlit UI for analysts, FastAPI backend for automation.

## Project Status

- DOCUMENT-AI.v01
  - Core ingestion, chunking, embeddings, retrieval: ✅
  - LLM reasoning and sessionized flows: ✅
  - Streamlit UI and FastAPI API: ✅
  - Example scripts and docs: ✅

- REQUIREMENT-AI.v01
  - Ingestion (PDF/TXT/Image) + OCR: ✅
  - Embeddings + FAISS retrieval + candidate synthesis: ✅
  - NLP parsing, validation (ambiguity/conflict), MoSCoW prioritization: ✅
  - Outputs (DOCX/Excel/User Stories), Streamlit UI, FastAPI API: ✅
  - Offline-friendly defaults; LLM wiring via config possible: ✅

## Quickstart

### Document-AI (Policy Assistant)
- README: DOCUMENT-AI.v01/README.md
- Run UI:
  ```bash
  cd DOCUMENT-AI.v01
  # Backend (example from project README)
  cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000
  # Frontend
  cd ../ui && streamlit run app.py
  ```

### Requirement-AI (Requirements Authoring)
- README: REQUIREMENT-AI.v01/README.md
- Run UI:
  ```bash
  cd REQUIREMENT-AI.v01
  streamlit run ui/ui_app.py
  ```
- Run API:
  ```bash
  cd REQUIREMENT-AI.v01
  uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
  ```

## Artifacts & Outputs

- Requirement-AI outputs (after a run) are saved under `REQUIREMENT-AI.v01/out/`:
  - requirements.docx: Formatted requirements document
  - requirements.xlsx: Detailed, filterable report
  - user_stories.txt: Plain text user stories for import

- Document-AI responses are served via API/UI with retrieved clause explanations.

## Next Steps (Suggested)

- Wire configurable LLM providers for Requirement-AI synthesis (OpenAI/LangChain) with on/off toggles.
- Add domain-specific validation libraries (compliance/policy rule packs).
- Persist vector indexes and metadata stores for faster cold starts.
- Integrate JIRA export for user stories and requirements traceability.

