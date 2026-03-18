"""
Configuración centralizada de la aplicación.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # App
    APP_NAME: str = "Test Plan Generator"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True  # True para desarrollo local
    
    # Database - SQLite para entorno local
    DATABASE_URL: str = "sqlite:///./test_plan_generator.db"
    
    # Security (modo single-user, no se usa autenticación aún)
    SECRET_KEY: str = "local-secret-key-change-in-production"  # Cambiar si es necesario
    AUTH_REQUIRED: bool = False  # Modo single-user
    DEFAULT_USER_ID: int = 1
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL_TRANSLATION: str = "gpt-4.1-mini"
    OPENAI_MODEL_GENERATION: str = "gpt-4.1"
    
    # CORS - Permisivo para desarrollo local
    CORS_ORIGINS: List[str] = ["*"]
    
    # File Storage
    EXPORT_STORAGE_PATH: str = "./exports"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
