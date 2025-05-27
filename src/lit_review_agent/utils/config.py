"""Configuration management for the literature review agent."""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Literal, List

from dotenv import load_dotenv
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration with environment variable support."""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="allow"  # Allow extra fields that might come from .env
    )
    
    # Core Settings
    app_name: str = "AI Literature Review Agent"
    version: str = "0.1.0"
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    debug: bool = Field(default=False, validation_alias="DEBUG")

    # LLM Provider Settings (OpenAI, DeepSeek, Ollama, Mock)
    llm_provider: Literal["openai", "deepseek", "ollama", "mock"] = Field(
        default="deepseek", validation_alias="LLM_PROVIDER") # Default to deepseek
    llm_timeout_seconds: int = Field(default=60, validation_alias="LLM_TIMEOUT_SECONDS")
    llm_max_retries: int = Field(default=3, validation_alias="LLM_MAX_RETRIES")
    llm_rate_limit_delay: float = Field(default=5.0, validation_alias="LLM_RATE_LIMIT_DELAY") # Seconds
    embedding_dimension_mock: int = Field(default=128, validation_alias="EMBEDDING_DIMENSION_MOCK") # For mock LLM testing

    # OpenAI Specific Settings
    openai_api_key: Optional[str] = Field(default=None, validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", validation_alias="OPENAI_MODEL")
    openai_embedding_model: str = Field(default="text-embedding-ada-002", validation_alias="OPENAI_EMBEDDING_MODEL")
    openai_api_base: Optional[str] = Field(default=None, validation_alias="OPENAI_API_BASE") # For Azure OpenAI or compatible APIs

    # DeepSeek Specific Settings
    deepseek_api_key: Optional[str] = Field(default=None, validation_alias="DEEPSEEK_API_KEY")
    deepseek_model: str = Field(default="deepseek-chat", validation_alias="DEEPSEEK_MODEL") # Or "deepseek-coder"
    deepseek_embedding_model: Optional[str] = Field(default=None, validation_alias="DEEPSEEK_EMBEDDING_MODEL") # If they offer one
    deepseek_api_base: Optional[str] = Field(default="https://api.deepseek.com/v1", validation_alias="DEEPSEEK_API_BASE")

    # Ollama Specific Settings (if using a local Ollama server)
    ollama_api_base: Optional[str] = Field(default="http://localhost:11434/api", validation_alias="OLLAMA_API_BASE")
    ollama_model: Optional[str] = Field(default="llama3", validation_alias="OLLAMA_MODEL")
    ollama_embedding_model: Optional[str] = Field(default="nomic-embed-text", validation_alias="OLLAMA_EMBEDDING_MODEL")
    ollama_request_timeout: int = Field(default=120, validation_alias="OLLAMA_REQUEST_TIMEOUT")

    # Semantic Scholar Specific Settings
    semantic_scholar_api_key: Optional[str] = Field(default=None, validation_alias="SEMANTIC_SCHOLAR_API_KEY")
    semantic_scholar_timeout_seconds: int = Field(default=30, validation_alias="SEMANTIC_SCHOLAR_TIMEOUT_SECONDS")
    # Note: Semantic Scholar API URL is usually fixed, defined in the client itself.

    # Default LLM completion parameters (can be overridden per call)
    # Structure: { "provider_name": { "param1": value1, ... } }
    default_llm_completion_config: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            "openai": {"max_tokens": 1024, "temperature": 0.7},
            "deepseek": {"max_tokens": 2048, "temperature": 0.7}, # Deepseek might support larger contexts
            "ollama": {"max_tokens": 2048, "temperature": 0.8}, # Ollama defaults can vary by model
            "mock": {"max_tokens": 500, "temperature": 0.5}
        }
    )

    # Retrieval Settings
    arxiv_api_url: str = Field(default="http://export.arxiv.org/api/", validation_alias="ARXIV_API_URL")
    arxiv_max_results: int = Field(default=100, validation_alias="ARXIV_MAX_RESULTS")
    arxiv_query_prefix: Optional[str] = Field(default=None, validation_alias="ARXIV_QUERY_PREFIX")

    # Processing Settings
    # PDF Processing
    pdf_user_agent: str = Field(default="Mozilla/5.0 (compatible; AIResearchAgent/0.1; +http://example.com/bot)", validation_alias="PDF_USER_AGENT")
    pdf_processing_timeout: int = Field(default=120, validation_alias="PDF_PROCESSING_TIMEOUT")

    # Text Processing Settings
    spacy_model_name: str = Field(default="en_core_web_sm", validation_alias="SPACY_MODEL_NAME")
    nltk_data_path: Optional[str] = Field(default=None, validation_alias="NLTK_DATA_PATH")
    
    # Embedding Settings for Vector Store
    sentence_transformer_model: str = Field(default="all-MiniLM-L6-v2", validation_alias="SENTENCE_TRANSFORMER_MODEL")

    # Advanced Settings & Defaults
    default_retrieval_sources: List[str] = Field(default_factory=lambda: ["arxiv", "semantic_scholar"], validation_alias="DEFAULT_RETRIEVAL_SOURCES")
    
    # Vector Database Configuration
    chroma_persist_directory: str = Field(default="./data/chroma_db", validation_alias="CHROMA_PERSIST_DIRECTORY")
    chroma_collection_name: str = Field(default="literature_collection", validation_alias="CHROMA_COLLECTION_NAME")
    
    # Application Configuration
    log_file: str = Field(default="./logs/app.log", validation_alias="LOG_FILE")
    max_chunk_size: int = Field(default=1000, validation_alias="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, validation_alias="CHUNK_OVERLAP")
    
    # Rate Limiting
    max_requests_per_minute: int = Field(default=60, validation_alias="MAX_REQUESTS_PER_MINUTE")
    max_tokens_per_request: int = Field(default=4000, validation_alias="MAX_TOKENS_PER_REQUEST")
    
    # Output Configuration
    output_dir: str = Field(default="./data/outputs", validation_alias="OUTPUT_DIR")
    report_format: str = Field(default="markdown", validation_alias="REPORT_FORMAT")
    
    def __init__(self, **kwargs):
        """Initialize configuration, loading from .env file if it exists."""
        print("DEBUG: Config.__init__ called.")
        # Pydantic's BaseSettings will automatically try to load from .env
        # based on the inner Meta class (class Config:
        #                               env_file = ".env"
        #                               ...)
        # So, explicit load_dotenv calls here might be redundant or could interfere
        # depending on pydantic-settings version and exact behavior.
        # We will rely on BaseSettings' own mechanism for now.

        # env_path = Path(".env") # For debug printing of expected path
        # print(f"DEBUG: Expecting .env file at: {env_path.absolute()}")
        
        super().__init__(**kwargs) # This is where Pydantic loads .env and populates fields
        
        print(f"DEBUG: Config super().__init__() completed.")
        print(f"DEBUG: Value of self.deepseek_api_key AFTER super init: {self.deepseek_api_key}")
        print(f"DEBUG: Value of self.llm_provider AFTER super init: {self.llm_provider}")
        if not self.deepseek_api_key and self.llm_provider == "deepseek":
            print("ERROR_DEBUG: DeepSeek API key is None and provider is deepseek!")
            # You could also check os.getenv('DEEPSEEK_API_KEY') here to see if it's in the environment
            # print(f"DEBUG: Value of os.getenv('DEEPSEEK_API_KEY') at this point: {os.getenv('DEEPSEEK_API_KEY')}")

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
    
    def env_file_location(self) -> str:
        """Get the location of the environment file."""
        env_path = Path(".env")
        if env_path.exists():
            return str(env_path.absolute())
        config_env_path = Path("config/.env")
        if config_env_path.exists():
            return str(config_env_path.absolute())
        return "No .env file found"
    
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