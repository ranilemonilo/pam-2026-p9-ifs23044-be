import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_PORT = os.getenv("APP_PORT", 5000)
    BASE_URL = os.getenv("LLM_BASE_URL")
    LLM_TOKEN = os.getenv("LLM_TOKEN")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/data.db"