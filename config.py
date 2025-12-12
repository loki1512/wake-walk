import os
from zoneinfo import ZoneInfo

USER_TZ = ZoneInfo("Asia/Kolkata")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_SECRET = os.environ.get("JWT_SECRET", "dev-jwt-secret")

    SQLALCHEMY_DATABASE_URI = "sqlite:///wakewalk.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    SMTP_HOST = os.environ.get("SMTP_HOST")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASS = os.environ.get("SMTP_PASS")
    EMAIL_FROM = os.environ.get("EMAIL_FROM", SMTP_USER)

    
