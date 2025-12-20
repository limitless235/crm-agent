from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AntiGravity AI Worker"
    
    # DB (for saving responses)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "support_db"
    POSTGRES_PORT: int = 5432
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    TICKET_EVENTS_STREAM: str = "ticket_events"
    CONSUMER_GROUP: str = "ai_processor_group"
    
    # AI
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    LLM_MODEL_PATH: str = "/app/data/models/model.gguf"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
