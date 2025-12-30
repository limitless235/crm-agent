from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AntiGravity AI Worker"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    TICKET_EVENTS_STREAM: str = "ticket_events"
    AI_RESPONSES_STREAM: str = "ai_responses"
    CONSUMER_GROUP: str = "ai_processor_group"
    
    # AI - Chroma
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    CHROMA_COLLECTION_NAME: str = "knowledge_base"
    
    # AI - Embeddings
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    # AI - LLM
    LLM_MODEL_PATH: str = "/data/models/mistral-7b-v0.1.Q5_K_M.gguf"
    LLM_CONTEXT_WINDOW: int = 2048
    LLM_MAX_TOKENS: int = 500
    LLM_TIMEOUT: int = 30 # Seconds
    
    # Persistence - FAISS
    FAISS_INDEX_PATH: str = "/data/faiss/index.bin"
    
    # Safety
    IDEMPOTENCY_TTL: int = 86400 # 24 hours
    
    # Postgres (Raw SQL only if required, no ORM)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "support_db"
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
