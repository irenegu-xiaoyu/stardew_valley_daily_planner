import json
from pathlib import Path

def load_gemini_config() -> dict:
    path = Path(__file__).parent.resolve() / "gemini_api_config.json"

    cfg = {}
    try:
        if path.exists() and path.stat().st_size > 0:
            with path.open("r", encoding="utf-8") as f:
                cfg = json.load(f)
    except Exception as e:
        # If JSON is malformed or unreadable, raise so the server fails fast.
        raise RuntimeError(f"Failed to load Gemini config from {path}: {e}")

    api_key = cfg.get("api_key")
    model = cfg.get("model") or "gemini-3-flash-preview"

    config = {"api_key": api_key, "model": model}
    print(f" ✈️  Load LLM model config: {config}")
    return config

