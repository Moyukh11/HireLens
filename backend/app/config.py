import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ML_MODELS_DIR = BASE_DIR.parent / "ml" / "training" / "saved_models"

class Settings:
    PROJECT_NAME: str = "HireLens API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    MODEL_DIR: Path = ML_MODELS_DIR

settings = Settings()
