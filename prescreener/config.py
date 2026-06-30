import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-prod")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'prescreener.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    TEMP_FOLDER = str(BASE_DIR / "tmp")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2 GB

    MAX_VIDEO_DURATION = 4 * 3600  # 4 hours
    MAX_MOMENTS = 15

    WHISPER_RATE_PER_MIN = 0.006
    CLAUDE_MODEL = "claude-sonnet-4-6"
    CLAUDE_INPUT_RATE = 3.00 / 1_000_000
    CLAUDE_OUTPUT_RATE = 15.00 / 1_000_000

    TOTAL_BUDGET = 2000.00
