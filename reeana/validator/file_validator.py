# backend/validators/file_validator.py
from fastapi import FastAPI, UploadFile, HTTPException

class FileValidator:
    """Validate uploaded files before processing"""
    
    MAX_SIZE_MB = 5
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
    
    @classmethod
    def validate_file(cls, file: UploadFile) -> None:
        """Validate uploaded file.
        Raises HTTPException if invalid.

        Parameters
        ----------
        file: UploadFile :
            

        Returns
        -------

        """
        
        # Check 1: File extension
        filename = file.filename.lower()
        extension = '.' + filename.split('.')[-1] if '.' in filename else ''
        
        if extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {extension} not supported. "
                       f"Allowed: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )
        
        # Check 2: File size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()  # Get size
        file.file.seek(0)  # Reset to beginning
        
        max_size_bytes = cls.MAX_SIZE_MB * 1024 * 1024
        if file_size > max_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File too large ({file_size / 1024 / 1024:.1f}MB). "
                       f"Max size: {cls.MAX_SIZE_MB}MB"
            )
        
        # Check 3: File not empty
        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )