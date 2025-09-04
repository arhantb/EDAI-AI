# Requirement-AI v0.1

<p align="center">
  <img width=200px height=200px src="EDAI.png" alt="Requirement-AI Logo">
</p>

<h3 align="center">Automated Requirements Authoring with RAG + OCR</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-red.svg)]()

</div>

---

<p align="center">
Requirement-AI streamlines requirements engineering by automating extraction, validation, and prioritization from PDFs, images (OCR), and text. It combines FAISS-based retrieval, NLP parsing, semantic validation, and MoSCoW prioritization to produce clean DOCX/PDF/Excel outputs and user stories ready for project tools.
</p>

##  Features

- **Multi-Format Ingestion**: PDFs, TXT, and scanned images via OCR (Tesseract)
- **RAG Context**: FAISS vector search + context synthesis for requirement candidates
- **NLP Parsing & Classification**: Clean, normalize, and classify into functional/non-functional
- **Validation & Gap Analysis**: Detect ambiguity, conflicts, and missing details
- **Prioritization**: MoSCoW tagging with optional ML ranking stub
- **Standardized Outputs**: DOCX requirements, Excel report, and user stories export
- **Web Interface**: Streamlit UI for easy runs and downloads
- **REST API**: FastAPI backend for programmatic processing

##  Table of Contents

- [About](#about)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)

##  About

Requirement-AI helps business analysts and engineers accelerate and standardize requirement authoring by automatically extracting candidate statements, validating them against rules, and prioritizing them for execution. It supports OCR for scanned sources and produces ready-to-share artifacts.

Key capabilities:
- **Document Ingestion**: Parse text from PDFs, TXT, PNG/JPG (OCR)
- **Text Chunking**: Overlapping chunks suitable for vector search
- **Vector Indexing**: FAISS-based similarity search for context
- **Candidate Synthesis**: Heuristic/LLM-ready synthesis of requirement lines
- **Validation**: Ambiguity/conflict detection and gap flags
- **Prioritization**: MoSCoW tagging and sort

##  Architecture

The system follows a modular architecture with clear separation of concerns:

```
REQUIREMENT-AI.v01/
├── app/                    # Core application logic
│   ├── core/               # Core components (engine, retriever, embedder, nlp, validation)
│   ├── ingestion/          # Document loading and chunking
│   └── main.py             # CLI entry point
├── ui/                     # Streamlit user interface
├── config/                 # Configuration files
├── data/                   # Documents and knowledge store
└── scripts/                # Utility scripts
```

### Core Components

- **Engine**: Orchestrates ingestion → embeddings → retrieval → synthesis → validation → prioritization → outputs
- **Retriever**: FAISS index management and top-k retrieval
- **Embedder**: Sentence-transformers embeddings
- **NLP**: Cleaning and classification (functional vs non-functional)
- **Validation**: Ambiguity and conflict checks, missing-info flags
- **Output**: DOCX/Excel and user story generation

##  Installation

### Prerequisites

- Python 3.12 or higher
- Tesseract OCR (for images/scanned PDFs) on PATH
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd REQUIREMENT-AI.v01
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On Unix/MacOS
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   - If using hosted LLMs, set provider keys (e.g., `OPENAI_API_KEY`).
   - Configure `config/config.yaml` for embeddings, chunking, retrieval, and outputs.

##  Usage

### Web Interface (Recommended)

1. **Launch the Streamlit interface**
   ```bash
   streamlit run ui/ui_app.py
   ```

2. **Set input/output**
   - In the sidebar, set “Input directory” (defaults to `data/docs`).
   - Click “Run Pipeline”.
   - Download artifacts: DOCX, Excel, and user stories.

### Backend API

1. **Start the FastAPI backend**
   ```bash
   uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Call endpoints**
   - Health:
     ```bash
     curl http://localhost:8000/health
     ```
   - Process:
     ```bash
     curl -X POST http://localhost:8000/process \
       -H "Content-Type: application/json" \
       -d '{"input_dir":"data/docs","out_dir":"out","query":"Project requirements","config_path":"config/config.yaml"}'
     ```

### CLI

Run the pipeline from the command line:
```bash
python -m app.main --input data/docs --out out --query "Project requirements"
```

## 🔌 API Reference

### Endpoints

#### `GET /health`
Health check for the backend service.

#### `POST /process`
Run the end-to-end pipeline over a directory of documents.

Request (JSON):
```json
{
  "input_dir": "data/docs",
  "out_dir": "out",
  "query": "Project requirements",
  "config_path": "config/config.yaml"
}
```

Response (JSON excerpt):
```json
{
  "result": {
    "files": ["..."],
    "num_chunks": 123,
    "num_candidates": 10,
    "validation": {"flags": [], "missing": []},
    "output_dir": "out"
  },
  "artifacts": {
    "docx": "out/requirements.docx",
    "excel": "out/requirements.xlsx",
    "stories": "out/user_stories.txt"
  }
}
```

## Configuration

The system configuration is managed through `config/config.yaml`:

```yaml
embedding:
  model: sentence-transformers/all-MiniLM-L6-v2
chunking:
  size: 800
  overlap: 120
rag:
  k: 6
output:
  generate_docx: true
  generate_excel: true
  generate_user_stories: true
```

##  Project Structure

```
REQUIREMENT-AI.v01/
├── app/                           # Core application
│   ├── core/                     # Core components
│   │   ├── embedder.py          # Text embeddings
│   │   ├── engine.py            # Orchestration engine
│   │   ├── nlp.py               # Cleaning and classification
│   │   ├── output.py            # DOCX/Excel and stories
│   │   ├── prioritization.py    # MoSCoW and ranking stub
│   │   ├── rag.py               # Context synthesis (LLM-ready)
│   │   ├── retriever.py         # FAISS vector retrieval
│   │   └── validation.py        # Ambiguity/conflict checks
│   ├── ingestion/               # Document processing
│   │   ├── chunk.py             # Text chunking
│   │   └── load.py              # PDF/TXT/OCR loading
│   ├── api.py                   # FastAPI application
│   └── main.py                  # CLI entrypoint
├── config/
│   └── config.yaml              # Pipeline configuration
├── data/
│   ├── docs/                    # Input documents
│   └── knowledge/               # Optional historical standards
├── scripts/
│   └── index_build.py           # Index utilities
├── ui/
│   └── ui_app.py                # Streamlit application
├── requirements.txt             # Python dependencies
├── Procfile                     # Process definition (Streamlit)
└── README.md                    # This file
```

##  Dependencies

### Core Dependencies
- **FastAPI** (≥0.111) - Web API
- **Streamlit** (≥1.36) - UI
- **Uvicorn** (≥0.30) - ASGI server

### AI & ML
- **Sentence Transformers** (≥2.7) - Embeddings
- **FAISS-CPU** (≥1.7.4) - Vector search
- **LangChain** (≥0.2) - LLM framework (optional)

### Document Processing
- **PyMuPDF** (≥1.24) - PDF processing
- **Python-DOCX** (≥1.1.2) - DOCX output
- **Pytesseract** (≥0.3.10) + Tesseract - OCR

### Utilities
- **NumPy** (≥1.26), **Pandas** (≥2.2), **SciPy** (≥1.11)
- **Scikit-learn** (≥1.5), **XGBoost** (≥2.0)

##  Deployment

### Local Development
```bash
# Backend
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

# Frontend
streamlit run ui/ui_app.py
```

### Production Deployment
1. Set up a production server
2. Install dependencies
3. Configure environment variables and `config/config.yaml`
4. Use a production ASGI server (e.g., Uvicorn/Gunicorn) behind a reverse proxy

##  Testing

Run utility scripts:

```bash
python scripts/index_build.py --input data/docs --index data/index/faiss
python -m app.main --input data/docs --out out --query "Project requirements"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Acknowledgments

- **FAISS** for efficient vector similarity search
- **FastAPI** and **Streamlit** for robust web tooling
- **Sentence Transformers** for embeddings
- **Tesseract OCR** for image-to-text extraction

**Requirement-AI v0.1** - Automating clear, consistent, and prioritized requirements.

## REQUIREMENT-AI.v01 — Automated Requirements Authoring with RAG + OCR

### Overview
REQUIREMENT-AI.v01 automates writing clear, complete, and prioritized software requirements by combining OCR, Retrieval-Augmented Generation (RAG), and advanced NLP/ML. It ingests multi-format sources (text, PDFs, images/scans), extracts and validates candidate requirements against historical data, industry standards, and compliance rules, asks targeted clarifications, and outputs standardized documents (DOCX/PDF) and Excel reports. It also generates structured user stories suitable for JIRA import.

### Key Capabilities
- **RAG for contextual insights**: Enriches extracted content using historical requirements, standards, and regulations via vector search (FAISS) and LLM synthesis (LangChain).
- **Advanced NLP parsing & classification**: Uses spaCy and transformer models to normalize, parse, and classify requirements into functional/non-functional groups.
- **Semantic validation & gap analysis**: Cross-verifies against business rules/compliance, detects ambiguity/conflicts/missing details, and generates clarification questions.
- **Prioritization**: Implements MoSCoW, with an optional ML ranking stub (XGBoost/Decision Trees) to suggest sequencing.
- **Standardized outputs**: Produces DOCX/PDF requirements, Excel traceability reports, and user stories compatible with project tools.

### Project Structure
```
REQUIREMENT-AI.v01/
  app/
    core/
      ocr.py              # OCR and PDF/text ingestion helpers
      embedder.py         # Sentence embeddings
      retriever.py        # FAISS vector store
      rag.py              # RAG assembly via LangChain
      nlp.py              # Parsing, cleaning, classification
      validation.py       # Rules, ambiguity checks, gap analysis
      prioritization.py   # MoSCoW + ML ranking stub
      output.py           # DOCX/PDF/Excel and user stories
      engine.py           # Orchestration of end-to-end pipeline
    ingestion/
      load.py             # File loading and conversion pipeline
      chunk.py            # Chunking strategies
    main.py               # CLI entrypoint
  config/
    config.yaml           # Model names, paths, thresholds
  scripts/
    index_build.py        # Build/update vector index
  ui/
    app.py                # Streamlit UI
  requirements.txt
  Procfile
  README.md
```

### Quickstart
1) Create and activate a virtual environment (Windows PowerShell):
```powershell
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

2) Configure environment variables:
- `OPENAI_API_KEY` (or set `LLM_PROVIDER=none` to run without LLM calls)
- Optional: `HF_HOME` for model cache, `TESSDATA_PREFIX` for Tesseract data

3) Install Tesseract OCR (required for image/scanned PDFs):
- Windows: Download installer from `https://github.com/tesseract-ocr/tesseract` and ensure `tesseract.exe` is on PATH.

4) Prepare data:
- Place source documents under `data/docs/` (PDFs, images, .docx exported to PDF, or .txt)
- Optionally add historical requirements/standards under `data/knowledge/`

5) Build or update the vector index:
```powershell
python scripts/index_build.py --input data/docs --index data/index/faiss
```

6) Run the CLI pipeline:
```powershell
python -m app.main --input data/docs --out out/ --moscow --stories
```

7) Launch the Streamlit UI:
```powershell
streamlit run ui/app.py
```

### Configuration
See `config/config.yaml` for:
- Embedding model, chunk sizes, overlap
- FAISS index path
- NLP toggles (spaCy model, transformer classifier)
- Validation thresholds and ambiguity detectors
- MoSCoW weighting and ML ranking flags
- Output formats and templates

### Notes on Models and Performance
- Default embeddings use `sentence-transformers/all-MiniLM-L6-v2` for speed. Switch to larger models for quality.
- OCR quality depends on input scans; consider preprocessing (deskew, denoise) for best results.
- The ML ranking component is provided as a stub; plug in your trained model or export features.

### Security and Compliance
- Keep regulated data in your environment. Avoid sending sensitive content to external LLMs by setting `LLM_PROVIDER=none` or hosting a local model.
- PII handling is your responsibility; enable redaction if required before indexing.

### License
Apache-2.0


