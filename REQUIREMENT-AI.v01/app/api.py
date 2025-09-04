from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from app.core.engine import PipelineEngine


class ProcessRequest(BaseModel):
    input_dir: str = "data/docs"
    out_dir: str = "out"
    query: str = "Project requirements"
    config_path: str = "config/config.yaml"


app = FastAPI(title="Requirement-AI Backend", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/process")
def process(req: ProcessRequest):
    engine = PipelineEngine(req.config_path)
    result = engine.run(req.input_dir, req.out_dir, req.query)
    # return minimal file hints
    out = Path(req.out_dir)
    return {
        "result": result,
        "artifacts": {
            "docx": str(out / "requirements.docx"),
            "excel": str(out / "requirements.xlsx"),
            "stories": str(out / "user_stories.txt"),
        },
    }


