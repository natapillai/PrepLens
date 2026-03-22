import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)


class Settings:
    APP_NAME: str = "PrepLens API"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", "5"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ALLOWED_ORIGINS", "http://localhost:3000"
    ).split(",")


settings = Settings()
