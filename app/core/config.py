from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Ustawienia globalne aplikacji.
    """
    PROJECT_NAME: str = "Library API"
    DATABASE_URL: str = "sqlite:///./library.db"

settings = Settings()