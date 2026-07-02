import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


class Settings:
    llm_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    llm_temperature: float = _get_float("OLLAMA_TEMPERATURE", 0.0)
    retriever_k: int = _get_int("RETRIEVER_K", 5)
    max_agent_retries: int = _get_int("MAX_AGENT_RETRIES", 2)
    event_delay_seconds: float = _get_float("EVENT_DELAY_SECONDS", 2.0)
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    chroma_persist_dir: Path = Path(
        os.getenv("CHROMA_PERSIST_DIR", BASE_DIR / "rag" / "chroma_db")
    )
    shot_data_csv: Path = Path(
        os.getenv("SHOT_DATA_CSV", BASE_DIR / "data" / "shot_data.csv")
    )
    shot_corpus_txt: Path = Path(
        os.getenv("SHOT_CORPUS_TXT", BASE_DIR / "rag" / "shot_corpus.txt")
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
