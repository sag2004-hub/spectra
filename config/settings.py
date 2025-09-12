import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # App Settings
    WAKE_WORD = os.getenv("WAKE_WORD", "spectra")
    USE_INTERNET_TTS = os.getenv("USE_INTERNET_TTS", "true").lower() == "true"
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CODE_DIRECTORY = os.path.join(BASE_DIR, "generated_code")