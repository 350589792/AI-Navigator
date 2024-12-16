from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    PROJECT_NAME: str = "AI Navigator"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/test_db"

    # JWT
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()