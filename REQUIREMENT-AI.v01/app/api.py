from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import asyncio
import time
from functools import lru_cache
import threading

# Lazy imports to reduce startup time
def get_engine():
    from app.core.engine import PipelineEngine
    return PipelineEngine

# Global cache for engines
_engine_cache = {}
_cache_lock = threading.Lock()


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
    return {
        "status": "healthy",
        "message": "Requirement-AI v0.1 is running",
        "timestamp": time.time(),
        "cached_engines": len(_engine_cache)
    }

@app.post("/clear_cache")
async def clear_cache():
    """Clear engine cache"""
    with _cache_lock:
        _engine_cache.clear()
    return {"status": "success", "message": "Engine cache cleared"}

def get_cached_engine(config_path: str):
    """Get or create cached engine instance"""
    with _cache_lock:
        if config_path not in _engine_cache:
            PipelineEngine = get_engine()
            _engine_cache[config_path] = PipelineEngine(config_path)
        return _engine_cache[config_path]


@app.post("/process")
async def process(req: ProcessRequest):
    start_time = time.time()
    loop = asyncio.get_running_loop()
    
    # Use cached engine
    engine = get_cached_engine(req.config_path)
    
    # Run CPU-bound pipeline in a thread to keep event loop responsive
    result = await loop.run_in_executor(None, engine.run, req.input_dir, req.out_dir, req.query)
    
    processing_time = time.time() - start_time
    out = Path(req.out_dir)
    
    return {
        "result": result,
        "artifacts": {
            "docx": str(out / "requirements.docx"),
            "excel": str(out / "requirements.xlsx"),
            "stories": str(out / "user_stories.txt"),
        },
        "processing_time": processing_time,
        "performance": {
            "total_time": processing_time,
            "cached_engine": True
        }
    }


@app.post("/upload-and-process")
async def upload_and_process(
    files: List[UploadFile] = File(...),
    query: str = "Project requirements",
    out_dir: str = "out",
    config_path: str = "config/config.yaml",
):
    start_time = time.time()
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

    # Run pipeline against the session dir using cached engine
    loop = asyncio.get_running_loop()
    engine = get_cached_engine(config_path)
    result = await loop.run_in_executor(None, engine.run, str(session_dir), out_dir, query)
    
    processing_time = time.time() - start_time
    out = Path(out_dir)
    
    return {
        "input_files": saved_paths,
        "result": result,
        "artifacts": {
            "docx": str(out / "requirements.docx"),
            "excel": str(out / "requirements.xlsx"),
            "stories": str(out / "user_stories.txt"),
        },
        "processing_time": processing_time,
        "performance": {
            "total_time": processing_time,
            "files_processed": len(files),
            "cached_engine": True
        }
    }

# New unique features
@app.get("/analytics/summary")
async def get_analytics_summary():
    """Get analytics summary of processed requirements"""
    try:
        # This would typically query a database or cache
        return {
            "total_sessions": len(_engine_cache),
            "avg_processing_time": "N/A",  # Would calculate from historical data
            "most_common_requirements": ["User authentication", "Data validation", "Error handling"],
            "moscow_distribution": {"must": 45, "should": 30, "could": 20, "wont": 5}
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/requirements/validate")
async def validate_requirements_text(requirements_text: str):
    """Validate requirements text without full processing"""
    try:
        # Quick validation without full pipeline
        lines = requirements_text.split('\n')
        validated = []
        for line in lines:
            if line.strip():
                validated.append({
                    "text": line.strip(),
                    "valid": len(line.strip()) > 10,  # Simple validation
                    "suggestions": ["Add more detail"] if len(line.strip()) <= 10 else []
                })
        return {"validated_requirements": validated}
    except Exception as e:
        return {"error": str(e)}

@app.get("/templates/outline")
async def get_requirement_outline():
    """Get standard requirement document outline"""
    return {
        "sections": [
            "1. INTRODUCTION",
            "2. PROJECT OVERVIEW", 
            "3. FUNCTIONAL REQUIREMENTS",
            "4. NON-FUNCTIONAL REQUIREMENTS",
            "5. SYSTEM ARCHITECTURE",
            "6. DATA REQUIREMENTS",
            "7. INTERFACE REQUIREMENTS",
            "8. SECURITY REQUIREMENTS",
            "9. PERFORMANCE REQUIREMENTS",
            "10. TESTING REQUIREMENTS",
            "11. DEPLOYMENT REQUIREMENTS",
            "12. MAINTENANCE REQUIREMENTS"
        ],
        "description": "Standard software requirements document outline"
    }

@app.post("/requirements/prioritize")
async def prioritize_requirements(requirements: List[str], criteria: dict = None):
    """Prioritize a list of requirements using MoSCoW method"""
    try:
        if criteria is None:
            criteria = {"must": 4, "should": 3, "could": 2, "wont": 1}
        
        prioritized = []
        for i, req in enumerate(requirements):
            # Simple prioritization logic (would be more sophisticated in real implementation)
            if "authentication" in req.lower() or "security" in req.lower():
                priority = "must"
            elif "performance" in req.lower() or "optimization" in req.lower():
                priority = "should"
            elif "nice" in req.lower() or "optional" in req.lower():
                priority = "could"
            else:
                priority = "should"
            
            prioritized.append({
                "requirement": req,
                "priority": priority,
                "score": criteria.get(priority, 2),
                "rank": i + 1
            })
        
        # Sort by score
        prioritized.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "prioritized_requirements": prioritized,
            "criteria_used": criteria,
            "total_count": len(requirements)
        }
    except Exception as e:
        return {"error": str(e)}

