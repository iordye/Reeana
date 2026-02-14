# backend/validators/content_validator.py

class ContentValidator:
    """Validate extracted resume content"""
    
    MIN_WORDS = 50  # A real resume should have at least this
    MAX_WORDS = 5000  # Probably not a resume if longer
    
    @classmethod
    def validate_resume_text(cls, text: str) -> None:
        """
        Validate extracted resume text.
        Raises ValueError if invalid.
        """
        
        # Check 1: Not empty after extraction
        if not text or not text.strip():
            raise ValueError("No text could be extracted from file")
        
        # Check 2: Minimum content
        word_count = len(text.split())
        if word_count < cls.MIN_WORDS:
            raise ValueError(
                f"Resume too short ({word_count} words). "
                f"Minimum: {cls.MIN_WORDS} words"
            )
        
        # Check 3: Maximum content (prevent abuse)
        if word_count > cls.MAX_WORDS:
            raise ValueError(
                f"Resume too long ({word_count} words). "
                f"Maximum: {cls.MAX_WORDS} words"
            )
        
        # Check 4: Contains resume-like content
        # Basic heuristic: should have some common resume keywords
        resume_keywords = {
            'experience', 'education', 'skills', 'work', 'hobbies',
            'university', 'degree', 'project', 'summary'
        }
        
        text_lower = text.lower()
        matches = sum(1 for keyword in resume_keywords if keyword in text_lower)
        
        if matches < 3:
            raise ValueError(
                "File doesn't appear to be a resume. "
                "Please upload a valid resume document."
            )