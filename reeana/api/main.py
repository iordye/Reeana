#main.py
from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Form
from reeana.orchestrator import resume_orchestrator
import logging


# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


#  Initialize FastAPI App
app = FastAPI(
    title="Reeana API",
    description="An AI-powered resume analysis and feedback generator tool",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    """Check if the API is running"""
    return {
        "status": "healthy",
        "message": "Reeana API is running"
    }

#run ochestrator
@app.post("/analyze", response_model=dict)
async def analyze_resume(file: UploadFile = File(...), job_role: str = Form("general")):
    """
    Analyze a resume file and return structured feedback.

    Parameters
    ----------
    file : UploadFile
        Resume file (PDF, DOCX, or TXT). Max 5MB.
    job_role : str
        Target job role (e.g., "software engineer", "chef", "data scientist")
    """
    logger.info(f"New request | File: {file.filename} | Role: {job_role}")

    try:
        # Delegate EVERYTHING to the orchestrator
        result = resume_orchestrator.run(file, job_role=job_role)
        return result

    except HTTPException as e:
        # Pipeline already raised a proper HTTPException
        raise e

    except Exception as e:
        # Safety net 
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

