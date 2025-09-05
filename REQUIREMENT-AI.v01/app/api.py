from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import asyncio

from app.core.engine import PipelineEngine


class ProcessRequest(BaseModel):
    input_dir: str = "data/docs"
    out_dir: str = "out"
    query: str = "Project requirements"
    config_path: str = "config/config.yaml"


app = FastAPI(title="Requirement-AI Backend", version="0.1.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Requirement-AI backend is running", "docs": "/docs", "health": "/health"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/process")
async def process(req: ProcessRequest):
    loop = asyncio.get_running_loop()
    engine = PipelineEngine(req.config_path)
    # Run CPU-bound pipeline in a thread to keep event loop responsive
    result = await loop.run_in_executor(None, engine.run, req.input_dir, req.out_dir, req.query)
    out = Path(req.out_dir)
    return {
        "result": result,
        "artifacts": {
            "docx": str(out / "requirements.docx"),
            "excel": str(out / "requirements.xlsx"),
            "stories": str(out / "user_stories.txt"),
        },
    }


@app.post("/upload-and-process")
async def upload_and_process(
    files: List[UploadFile] = File(...),
    query: str = "Project requirements",
    out_dir: str = "out",
    config_path: str = "config/config.yaml",
):
    tmp_dir = Path("temp_uploads")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    session_dir = tmp_dir / ("session_" + str(asyncio.get_event_loop().time()).replace(".", ""))
    session_dir.mkdir(parents=True, exist_ok=True)

    # Save uploads concurrently
    async def _save_file(f: UploadFile):
        dest = session_dir / f.filename
        data = await f.read()
        dest.write_bytes(data)
        return str(dest)

    saved_paths = await asyncio.gather(*[_save_file(f) for f in files])

    # Run pipeline against the session dir
    loop = asyncio.get_running_loop()
    engine = PipelineEngine(config_path)
    result = await loop.run_in_executor(None, engine.run, str(session_dir), out_dir, query)
    out = Path(out_dir)
    return {
        "input_files": saved_paths,
        "result": result,
        "artifacts": {
            "docx": str(out / "requirements.docx"),
            "excel": str(out / "requirements.xlsx"),
            "stories": str(out / "user_stories.txt"),
        },
    }

