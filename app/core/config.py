import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Coach API"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Admin credentials
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "korky")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "korkabayo")
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS from environment variable if provided"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Database Settings (Railway PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_coach.db")
    
    # Groq API
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3-8b-8192")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
