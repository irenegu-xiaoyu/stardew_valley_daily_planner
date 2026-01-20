import os
from dotenv import load_dotenv

def load_env_config() -> dict:
    """Load Gemini configuration from environment variables"""
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
    
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please set it in your .env file."
        )
    
    config = {"api_key": api_key, "model": model}
    print(f" ✈️  Load LLM model config: {config}")
    return config

