from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from functools import lru_cache


class Settings(BaseSettings):
    # API Settings
    api_v1_prefix: str = Field(default="/api/v1")
    project_name: str = Field(default="IT Support Chatbot")
    debug: bool = Field(default=True)
    
    # Model Settings
    gemma_model_id: str = Field(default="google/gemma-2-2b-it")
    llm_model_id : str = Field(default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    embedding_model: str = Field(default="paraphrase-multilingual-MiniLM-L12-v2")
    
    # FAISS Settings
    faiss_index_path: str = Field(default="./data/it_support_faiss_index.bin")
    metadata_path: str = Field(default="./data/it_support_metadata.pkl")
    config_path: str = Field(default="./data/it_support_config.json")
    
    # Search Settings
    top_k_results: int = Field(default=4, ge=1, le=20)
    max_tokens: int = Field(default=130, ge=50, le=500)
    
    # Server Settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=1)
    
    # Logging
    log_level: str = Field(default="INFO")
    
    # Password keywords for filtering
    password_keywords: set = Field(
        default={
            "password", "passwort", "login", "credential", 
            "account", "reset", "zurücksetzen", "otp", "2fa", "mfa"
        }
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    @validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of {valid_levels}")
        return v.upper()


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()