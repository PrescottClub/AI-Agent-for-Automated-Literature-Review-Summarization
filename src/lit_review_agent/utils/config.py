"""Configuration management for the literature review agent."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    """Application configuration with environment variable support."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4-turbo-preview", env="OPENAI_MODEL")
    openai_embedding_model: str = Field("text-embedding-ada-002", env="OPENAI_EMBEDDING_MODEL")
    openai_api_base: Optional[str] = Field(None, env="OPENAI_API_BASE")
    
    # DeepSeek Configuration (Optional)
    deepseek_api_key: Optional[str] = Field(None, env="DEEPSEEK_API_KEY")
    deepseek_model: str = Field("deepseek-chat", env="DEEPSEEK_MODEL")
    deepseek_api_base: Optional[str] = Field("https://api.deepseek.com", env="DEEPSEEK_API_BASE")
    
    # LLM Provider Selection
    llm_provider: str = Field("openai", env="LLM_PROVIDER")
    
    # Vector Database Configuration
    chroma_persist_directory: str = Field("./data/chroma_db", env="CHROMA_PERSIST_DIRECTORY")
    chroma_collection_name: str = Field("literature_collection", env="CHROMA_COLLECTION_NAME")
    
    # Application Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("./logs/app.log", env="LOG_FILE")
    max_chunk_size: int = Field(1000, env="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    
    # Rate Limiting
    max_requests_per_minute: int = Field(60, env="MAX_REQUESTS_PER_MINUTE")
    max_tokens_per_request: int = Field(4000, env="MAX_TOKENS_PER_REQUEST")
    
    # Data Sources
    arxiv_max_results: int = Field(100, env="ARXIV_MAX_RESULTS")
    semantic_scholar_api_key: Optional[str] = Field(None, env="SEMANTIC_SCHOLAR_API_KEY")
    
    # Output Configuration
    output_dir: str = Field("./data/outputs", env="OUTPUT_DIR")
    report_format: str = Field("markdown", env="REPORT_FORMAT")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        """Initialize configuration, loading from .env file if it exists."""
        # Try to load from .env file in current directory first
        env_path = Path(".env")
        if env_path.exists():
            load_dotenv(env_path)
        else:
            # Try to load from config directory
            config_env_path = Path("config/.env")
            if config_env_path.exists():
                load_dotenv(config_env_path)
        
        super().__init__(**kwargs)
        
        # Ensure directories exist
        self._create_directories()
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            Path(self.chroma_persist_directory).parent,
            Path(self.log_file).parent,
            Path(self.output_dir),
            Path("./data"),
            Path("./logs"),
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.dict()
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.log_level.upper() == "DEBUG"
    
    @property
    def chroma_settings(self) -> Dict[str, Any]:
        """Get Chroma database settings."""
        return {
            "persist_directory": self.chroma_persist_directory,
            "collection_name": self.chroma_collection_name,
        }
    
    @property
    def openai_settings(self) -> Dict[str, Any]:
        """Get OpenAI API settings."""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "embedding_model": self.openai_embedding_model,
            "api_base": self.openai_api_base,
        }
    
    @property
    def deepseek_settings(self) -> Dict[str, Any]:
        """Get DeepSeek API settings."""
        return {
            "api_key": self.deepseek_api_key,
            "model": self.deepseek_model,
            "api_base": self.deepseek_api_base,
        } 