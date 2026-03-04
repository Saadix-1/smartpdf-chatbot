import os
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Saad AI Cloud"
    API_V1_STR: str = "/api/v1"
    
    # Cloud API Keys
    OPENAI_API_KEY: str = ""
    PINECONE_API_KEY: str = ""
    PINECONE_INDEX_NAME: str = "smartpdf-index"
    
    @field_validator("OPENAI_API_KEY", "PINECONE_API_KEY")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip() if v else v

    model_config = {
        "case_sensitive": True,
        "env_file": ".env"
    }

settings = Settings()

