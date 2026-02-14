from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application settings.
    Loads values from .env file automatically.
    """
    
    # API Keys
    google_api_key: str
    
    # LLM Settings
    model_name: str = "gemini-2.5-flash-lite"
        
    # File Validation Settings
    max_file_size_mb: int = 5
    allowed_extensions: List[str] = [".pdf", ".docx", ".txt"]
    
    class Config:
        env_file = ".env"

# Create a single instance to use everywhere
settings = Settings()