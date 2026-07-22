from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables and .env file."""
    
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/real_estate_agent"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    OPENAI_API_KEY: str = "mock-key"
    ANTHROPIC_API_KEY: str = "mock-key"
    GEMINI_API_KEY: str = "mock-key"
    
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "real-estate-sales-os"
    
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    API_KEY_SECRET: str = "dev-secret-key-12345"
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
