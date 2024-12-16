import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    PROJECT_NAME: str = "AI Navigator"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database configuration
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "ai_navigator")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    # Test database configuration
    TEST_POSTGRES_DB: str = os.getenv("TEST_POSTGRES_DB", "ai_navigator_test")

    @property
    def DATABASE_URL(self) -> str:
        """Get the database URL based on the environment."""
        if os.getenv("TESTING"):
            db_name = self.TEST_POSTGRES_DB
        else:
            db_name = self.POSTGRES_DB

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{db_name}"
        )

    # JWT configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS configuration
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Default Vite dev server
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    # Email configuration
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
