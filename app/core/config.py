from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # OPENROUTER OR OLLAMA --> Change this to use OLLAMA and set it up
    LLM_HOST: Literal["OPENROUTER", "OLLAMA"] = "OPENROUTER"

    #Ingestion Settings
    BASE_UPLOAD_DIR: Path = Path("data/uploads")
    DOCLING_DEVICE: str = "cuda"
    DOCLING_NUM_THREADS: int = 8

    #VLM Settings
    OPEN_ROUTER_API: str 
    OPEN_ROUTER_VLM_BASE_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    OPEN_ROUTER_VLM_MODEL: str = "google/gemma-3-12b-it:free"

    OPEN_ROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    OPEN_ROUTER_EMBEDDING_MODEL: str = "openai/text-embedding-3-small"
    OPEN_ROUTER_CHAT_LLM: str = "openai/gpt-4o-mini"
    OPEN_ROUTER_GRADER_LLM: str = "openai/gpt-4o-mini"


    OLLAMA_BASE_URL: str = "http://localhost:11434/v1/chat/completions"
    OLLAMA_VLM_MODEL: str = "llama3.2-vision:latest"

    VLM_TIMEOUT: int = 240
    VLM_TEMPERATURE: float = 0.2
    VLM_PROMPT: str = "Describe this image in three sentences. Be concise and accurate."
    
    #Tokenizer Model Settings
    TOKEN_MODEL_ID: str = "BAAI/bge-m3"

    #Embedding model settings
    EMBED_MODEL_ID: str = "bge-m3:latest"

    #Milvus Vector Storage Settings
    MILVUS_HOST: str
    MILVUS_PORT: int
    MILVUS_URI: str

    #Chat Model Settings
    OLLAMA_MODEL: str = "qwen3:8b"

    #Postgres
    DB_URI: str

    #Redis + Celery
    CELERY_BROKER_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra='ignore' 
    )
settings = Settings()