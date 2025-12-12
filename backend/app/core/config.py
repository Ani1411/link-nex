from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "URL Shortener"
    VERSION: str = "1.0.0"
    DATABASE_URL: str # "postgresql://username:password@localhost:5432/url_shortener_db"
    SECRET_KEY: str # "your-secret-key-here"
    BASE_URL: str = "http://localhost:8000"
    REDIS_URL: str # "redis://localhost:6379/0"
    CACHE_TTL: int = 60 * 60 * 24
    
    class Config:
        env_file = ".env"

settings = Settings()