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

### Core Features
- **Multi-Format Ingestion**: PDFs, TXT, and scanned images via OCR (Tesseract)
- **RAG Context**: FAISS vector search + context synthesis for requirement candidates
- **NLP Parsing & Classification**: Clean, normalize, and classify into functional/non-functional
- **Validation & Gap Analysis**: Detect ambiguity, conflicts, and missing details
- **Prioritization**: MoSCoW tagging with optional ML ranking stub
- **Standardized Outputs**: DOCX requirements, Excel report, and user stories export
- **Web Interface**: Streamlit UI for easy runs and downloads
- **REST API**: FastAPI backend for programmatic processing

### 🚀 New Advanced Features
- **📊 Analytics Dashboard**: Real-time insights into requirement processing
- **✅ Quick Validator**: Instant validation of requirements text
- **📝 Template Builder**: Standard requirement document templates
- **🎯 Priority Assistant**: AI-powered MoSCoW prioritization
- **⚡ Performance Monitor**: Backend health and performance tracking
- **🔄 Smart Caching**: Optimized processing with intelligent caching
- **📈 Visual Analytics**: Interactive charts and metrics

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

### Quick Setup (Optimized)

1. **Navigate to project directory**
   ```powershell
   cd F:\EDAI-DOC-AI.v.01\REQUIREMENT-AI.v01
   ```

2. **One-click startup (Recommended)**
   ```powershell
   .\start_all.ps1
   ```

3. **Manual setup (if needed)**
   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   - If using hosted LLMs, set provider keys (e.g., `OPENAI_API_KEY`).
   - Configure `config/config.yaml` for embeddings, chunking, retrieval, and outputs.

### Performance Optimizations

- **Lazy Loading**: Models are loaded only when needed
- **Engine Caching**: Pipeline engines cached for faster subsequent runs
- **Smart Memory Management**: Efficient resource utilization
- **Concurrent Processing**: Async file uploads and processing

##  Usage

### Quick Start (Optimized Commands)

#### Option 1: One-Click Startup (Recommended)
```powershell
# Navigate to project root
cd F:\EDAI-DOC-AI.v.01\REQUIREMENT-AI.v01

# Start both backend and frontend automatically
.\start_all.ps1
```

#### Option 2: Manual Startup
**Terminal 1 - Backend (FastAPI):**
```powershell
# Navigate to project root
cd F:\EDAI-DOC-AI.v.01\REQUIREMENT-AI.v01

# Start backend with script
.\start_backend.ps1
```

**Terminal 2 - Frontend (Streamlit):**
```powershell
# Navigate to project root
cd F:\EDAI-DOC-AI.v.01\REQUIREMENT-AI.v01

# Start frontend with script
.\start_frontend.ps1
```

#### Option 3: Manual Commands
```powershell
# Backend
.\venv\Scripts\Activate.ps1
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
.\venv\Scripts\Activate.ps1
streamlit run ui/ui_app.py
```

### Access Points

- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Analytics**: http://localhost:8000/analytics/summary

### 🚀 New Features Usage

#### Analytics Dashboard
- View processing statistics and performance metrics
- Monitor MoSCoW distribution and common requirements
- Track system health and cached engines

#### Quick Validator
- Validate requirements text without full processing
- Get instant feedback on requirement quality
- Receive improvement suggestions

#### Template Builder
- Generate standard requirement document outlines
- Download customizable templates
- Follow industry best practices

#### Priority Assistant
- AI-powered MoSCoW prioritization
- Customizable priority weights
- Visual priority indicators

### CLI

Run the pipeline from the command line:
```bash
python -m app.main --input data/docs --out out --query "Project requirements"
```

## 🔌 API Reference

### Core Endpoints

#### `GET /health`
Health check for the backend service with performance metrics.

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

#### `POST /upload-and-process`
Upload files and process them immediately.

### 🚀 New Advanced Endpoints

#### `GET /analytics/summary`
Get analytics summary of processed requirements.
```json
{
  "total_sessions": 5,
  "avg_processing_time": "N/A",
  "most_common_requirements": ["User authentication", "Data validation"],
  "moscow_distribution": {"must": 45, "should": 30, "could": 20, "wont": 5}
}
```

#### `POST /requirements/validate`
Validate requirements text without full processing.
```json
{
  "validated_requirements": [
    {
      "text": "The system shall authenticate users",
      "valid": true,
      "suggestions": []
    }
  ]
}
```

#### `GET /templates/outline`
Get standard requirement document outline.
```json
{
  "sections": [
    "1. INTRODUCTION",
    "2. PROJECT OVERVIEW",
    "3. FUNCTIONAL REQUIREMENTS",
    "..."
  ],
  "description": "Standard software requirements document outline"
}
```

#### `POST /requirements/prioritize`
Prioritize requirements using MoSCoW method.
```json
{
  "prioritized_requirements": [
    {
      "requirement": "User authentication system",
      "priority": "must",
      "score": 4,
      "rank": 1
    }
  ],
  "criteria_used": {"must": 4, "should": 3, "could": 2, "wont": 1}
}
```

#### `POST /clear_cache`
Clear engine cache for better memory management.

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
streamlit run ui/ui_app.py

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



