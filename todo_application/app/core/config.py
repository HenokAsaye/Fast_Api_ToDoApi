from functools import lru_cache
from typing import List, Optional
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    PROJECT_NAME: str = Field(default="Todo API")
    VERSION: str = Field(default="0.1.0")
    API_V1_STR: str = Field(default="/api/v1")

    DOCS_URL: Optional[str] = Field(default="/docs")
    REDOC_URL: Optional[str] = Field(default="/redoc")
    OPENAPI_URL: Optional[str] = Field(default="/openapi.json")
    SECRET_KEY: str = Field(default="change-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)  # 24h
    ALGORITHM: str = Field(default="HS256")

    BACKEND_CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    DATABASE_URL: Optional[AnyUrl] = None
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "todo_db"

    PAGE_SIZE_DEFAULT: int = 20
    PAGE_SIZE_MAX: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """
        Prefer DATABASE_URL if provided; otherwise build from components.
        Example: postgresql+psycopg://user:pass@host:5432/dbname
        """
        if self.DATABASE_URL:
            return str(self.DATABASE_URL)
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def docs_enabled(self) -> bool:
        return self.DEBUG or self.ENV == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()