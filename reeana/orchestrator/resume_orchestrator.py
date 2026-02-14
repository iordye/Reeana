#ochestrator.py
from reeana.validator.file_validator import FileValidator
from reeana.extractor.text_extractor import TextExtractor
from reeana.validator.content_validator import ContentValidator
from reeana.analyzer.analyzer import ResumeAnalyzer
from fastapi import UploadFile, HTTPException, File, Form
from google import genai
from reeana.api import config
import logging

logger = logging.getLogger(__name__)

def run(file: UploadFile = File(...), job_role: str = Form(default="general")):

    """Orchestrates resume analysis"""

    # 1. Validate file
    try:
        FileValidator.validate_file(file)
        print(f"✅ File validation passed: {file.filename}")
    except HTTPException as e:
        logger.error(f"❌ Validation failed: {e.detail}")
        raise e
        
    # 2. Read file bytes
    try:
          file_bytes = file.file.read()
    except Exception as e:
          logger.error(f"Failed to read uploaded file: {str(e)}")
          raise HTTPException(
                status_code=400,
                detail=f"Failed to read uploaded file: {str(e)}"
          )
    
    filename = file.filename.lower()

    # 3. Extract text
    try:  
        if filename.endswith('.pdf'):
            resume_text = TextExtractor.extract_from_pdf(file_bytes)
        elif filename.endswith('.docx'):
                resume_text = TextExtractor.extract_from_docx(file_bytes)
        elif filename.endswith('.txt'):
                resume_text = TextExtractor.extract_from_txt(file_bytes)
        else:
            raise HTTPException(400, "Unsupported file format")
    except Exception as e:
                logger.error(f"Failed to read uploaded file: {str(e)}")
                raise HTTPException(400, f"Failed to extract text: {str(e)}")
                
     
    # 4. Validate content
    try:
            ContentValidator.validate_resume_text(resume_text)
    except ValueError as e:
            logger.error('Content Validator Failed')
            raise HTTPException(
        status_code=400,
        detail=str(e)
    )

    # 5. Build promp and Run Gemini analysis
    try:
          analyzer = analyzer = ResumeAnalyzer(config.settings.google_api_key)
          result = analyzer.analyze(resume_text=resume_text, job_role=job_role)

    except Exception as e:
          logger.error(f'Resume analysis failed: {str(e)}')
          raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(e)}"
        )
    return result
        
