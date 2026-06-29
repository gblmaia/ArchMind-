from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')

    # ==================== LLM CONFIG ====================
    LLM_MODEL: str = "llama3.1"
    LLM_TEMPERATURE: float = 0.0
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # ==================== RAG CONFIG ====================
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # ==================== PATHS ====================
    DATA_DIRECTORY: Path = Path("data/docs")
    PERSIST_DIRECTORY: Path = Path("chroma_db")

    # ==================== APP CONFIG ====================
    APP_TITLE: str = "ArchMind API"
    APP_VERSION: str = "1.0.0"


settings = Settings()