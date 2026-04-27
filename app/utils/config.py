import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_DIR = os.path.join(BASE_DIR, 'db')
os.makedirs(DB_DIR, exist_ok=True)

class Config:
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://delcom.org/api")
    LLM_TOKEN = os.getenv("LLM_TOKEN", "")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(DB_DIR, 'recipe.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    APP_PORT = int(os.getenv("APP_PORT", 5000))