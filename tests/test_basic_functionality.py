"""Basic functionality tests for Tsearch project."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from src.lit_review_agent.utils.config import Config
from src.lit_review_agent.utils.helpers import (
    clean_text,
    extract_keywords,
    estimate_tokens,
    chunk_text,
    safe_filename,
    validate_email,
)
from src.lit_review_agent.exceptions import LiteratureReviewError, ConfigurationError


@pytest.mark.unit
class TestConfig:
    """Test configuration management."""

    def test_config_initialization(self):
        """Test basic config initialization."""
        config = Config()
        assert config.app_name == "AI Literature Review Agent"
        assert config.version == "0.1.0"
        assert config.llm_provider in ["openai", "deepseek", "ollama", "mock"]

    def test_config_with_custom_values(self):
        """Test config with custom values."""
        config = Config(llm_provider="openai", debug=True, log_level="DEBUG")
        assert config.llm_provider == "openai"
        assert config.debug is True
        assert str(config.log_level) == "DEBUG"

    def test_is_development_property(self):
        """Test development mode detection."""
        config = Config(log_level="DEBUG")
        assert config.is_development is True

        config = Config(log_level="INFO")
        assert config.is_development is False


@pytest.mark.unit
class TestHelpers:
    """Test helper functions."""

    def test_clean_text(self):
        """Test text cleaning functionality."""
        dirty_text = "   Hello   world!   \n\n  "
        clean = clean_text(dirty_text)
        assert clean == "Hello world!"

    def test_clean_text_with_special_chars(self):
        """Test text cleaning with special characters."""
        dirty_text = "Hello @#$ world! 😀"
        clean = clean_text(dirty_text, remove_special_chars=True)
        assert "Hello" in clean
        assert "world" in clean
        assert "@#$" not in clean

    @patch("src.lit_review_agent.utils.helpers._get_spacy_model")
    def test_extract_keywords_fallback(self, mock_spacy):
        """Test keyword extraction fallback when spaCy is not available."""
        mock_spacy.return_value = None

        text = "This is a test document about machine learning and artificial intelligence."
        keywords = extract_keywords(text, max_keywords=5)

        assert isinstance(keywords, list)
        assert len(keywords) <= 5

    def test_estimate_tokens(self):
        """Test token estimation."""
        text = "This is a simple test text with some words."
        tokens = estimate_tokens(text)
        assert tokens > 0
        assert isinstance(tokens, int)

    def test_chunk_text(self):
        """Test text chunking."""
        text = "This is a long text. " * 100  # Create long text
        chunks = chunk_text(text, chunk_size=100, overlap=20)

        assert len(chunks) > 1
        # accounting for overlap
        assert all(len(chunk) <= 120 for chunk in chunks)

    def test_safe_filename(self):
        """Test safe filename generation."""
        unsafe_name = "test/file<name>with:illegal*chars?"
        safe_name = safe_filename(unsafe_name)

        assert "/" not in safe_name
        assert "<" not in safe_name
        assert ">" not in safe_name
        assert ":" not in safe_name
        assert "*" not in safe_name
        assert "?" not in safe_name

    def test_validate_email(self):
        """Test email validation."""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name+tag@domain.co.uk") is True
        assert validate_email("invalid.email") is False
        assert validate_email("@domain.com") is False
        assert validate_email("user@") is False


@pytest.mark.unit
class TestExceptions:
    """Test custom exceptions."""

    def test_base_exception(self):
        """Test base literature review exception."""
        error = LiteratureReviewError("Test error", error_code="TEST_001")
        assert str(error) == "TEST_001: Test error"

        error_dict = error.to_dict()
        assert error_dict["error_type"] == "LiteratureReviewError"
        assert error_dict["message"] == "Test error"
        assert error_dict["error_code"] == "TEST_001"

    def test_configuration_error(self):
        """Test configuration specific error."""
        error = ConfigurationError("Missing API key", config_key="openai_api_key")
        assert "Missing API key" in str(error)
        assert error.details["config_key"] == "openai_api_key"


@pytest.mark.integration
class TestProjectStructure:
    """Test project structure and imports."""

    def test_package_imports(self):
        """Test that main package imports work."""
        from src.lit_review_agent import __version__, LiteratureAgent

        assert __version__ == "0.1.0"
        assert LiteratureAgent is not None

    def test_core_modules_import(self):
        """Test that core modules can be imported."""
        from src.lit_review_agent.utils import Config
        from src.lit_review_agent.exceptions import LiteratureReviewError
        from src.lit_review_agent.agent import LiteratureAgent

        # Basic instantiation test
        config = Config()
        assert config is not None

    def test_directories_creation(self):
        """Test that necessary directories can be created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test directory creation like in the config
            directories = [
                temp_path / "data",
                temp_path / "logs",
                temp_path / "outputs",
            ]

            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                assert directory.exists()
                assert directory.is_dir()


@pytest.mark.slow
class TestModelLoading:
    """Test model loading (marked as slow)."""

    def test_sentence_transformer_loading(self):
        """Test that sentence transformer can be loaded."""
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer("all-MiniLM-L6-v2")

            # Test basic encoding
            text = "This is a test sentence."
            embedding = model.encode(text)

            assert embedding is not None
            assert len(embedding) > 0

        except Exception as e:
            pytest.skip(f"SentenceTransformer not available: {e}")

    @patch("spacy.load")
    def test_spacy_model_loading(self, mock_spacy_load):
        """Test spaCy model loading (mocked)."""
        mock_nlp = Mock()
        mock_spacy_load.return_value = mock_nlp

        from src.lit_review_agent.utils.helpers import _get_spacy_model

        model = _get_spacy_model("en_core_web_sm")
        assert model is not None
        mock_spacy_load.assert_called_with("en_core_web_sm")


@pytest.mark.async_test
class TestAsyncFunctionality:
    """Test async functionality."""

    @pytest.mark.asyncio
    async def test_pdf_processor_init(self):
        """Test PDF processor initialization."""
        from src.lit_review_agent.retrieval.pdf_processor import PDFProcessor

        processor = PDFProcessor()
        assert processor is not None

    @pytest.mark.asyncio
    async def test_llm_manager_init(self):
        """Test LLM manager initialization."""
        from src.lit_review_agent.ai_core.llm_manager import LLMManager

        config = Config(llm_provider="mock")
        manager = LLMManager(config)
        assert manager is not None
        assert manager.provider == "mock"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
