"""Configuration de l'application Parle"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path
from dotenv import load_dotenv

# Chargement du fichier .env
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    APP_NAME: str = "Parle"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://localhost:5173,https://localhost"
    
    # Database
    DATABASE_URL: str = "postgresql://parle_user:parle_password@localhost:5432/parle"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production-min-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # File storage
    UPLOAD_DIR: str = "/var/www/parle/uploads"
    AUDIO_DIR: str = "/var/www/parle/audio"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instance globale
settings = Settings()

# Création des répertoires locaux en dev
if settings.DEBUG:
    upload_dir = Path("uploads")
    audio_dir = Path("audio")
    upload_dir.mkdir(exist_ok=True)
    audio_dir.mkdir(exist_ok=True)
else:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.AUDIO_DIR, exist_ok=True)

