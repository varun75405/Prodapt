import os
from pathlib import Path
from dotenv import load_dotenv

from constants import PRIMARY_MODEL, FALLBACK_MODEL

# Load .env file from the parent directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in the environment.")
    
    BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
    PRIMARY_MODEL = PRIMARY_MODEL
    FALLBACK_MODEL = FALLBACK_MODEL

settings = Settings()
