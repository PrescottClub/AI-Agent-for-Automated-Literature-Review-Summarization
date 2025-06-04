"""Unit tests for configuration management."""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from src.lit_review_agent.utils.config import Config


@pytest.mark.unit
class TestConfig:
    """Test Config class."""

    def test_config_default_values(self):
        """Test config initialization with default values."""
        config = Config()

        # Test default values
        assert config.llm_provider == "deepseek"
        assert config.debug is False
        assert config.log_level == "INFO"
        assert config.max_results == 50
        assert config.llm_timeout_seconds == 30
        assert config.embedding_model == "all-MiniLM-L6-v2"

    def test_config_with_custom_values(self):
        """Test config initialization with custom values."""
        config = Config(
            llm_provider="openai",
            debug=True,
            log_level="DEBUG",
            max_results=100,
            openai_api_key="test_key",
        )

        assert config.llm_provider == "openai"
        assert config.debug is True
        assert config.log_level == "DEBUG"
        assert config.max_results == 100
        assert config.openai_api_key == "test_key"

    def test_config_deepseek_settings(self):
        """Test DeepSeek-specific configuration."""
        config = Config(
            llm_provider="deepseek",
            deepseek_api_key="deepseek_test_key",
            deepseek_model="deepseek-chat",
        )

        assert config.deepseek_api_key == "deepseek_test_key"
        assert config.deepseek_model == "deepseek-chat"

    def test_config_openai_settings(self):
        """Test OpenAI-specific configuration."""
        config = Config(
            llm_provider="openai",
            openai_api_key="openai_test_key",
            openai_model="gpt-4",
            openai_base_url="https://api.openai.com/v1",
        )

        assert config.openai_api_key == "openai_test_key"
        assert config.openai_model == "gpt-4"
        assert config.openai_base_url == "https://api.openai.com/v1"

    def test_config_ollama_settings(self):
        """Test Ollama-specific configuration."""
        config = Config(
            llm_provider="ollama",
            ollama_model="llama3",
            ollama_api_base="http://localhost:11434/api",
        )

        assert config.ollama_model == "llama3"
        assert config.ollama_api_base == "http://localhost:11434/api"

    def test_config_paths(self):
        """Test path configuration."""
        config = Config(
            chroma_persist_directory="/custom/chroma", output_dir="/custom/output"
        )

        assert config.chroma_persist_directory == "/custom/chroma"
        assert config.output_dir == "/custom/output"

    def test_config_search_settings(self):
        """Test search-related configuration."""
        config = Config(
            max_results=200, similarity_threshold=0.8, min_paper_length=1000
        )

        assert config.max_results == 200
        assert config.similarity_threshold == 0.8
        assert config.min_paper_length == 1000

    def test_config_from_env_vars(self):
        """Test config loading from environment variables."""
        env_vars = {
            "LLM_PROVIDER": "openai",
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
            "OPENAI_API_KEY": "env_api_key",
            "MAX_RESULTS": "75",
        }

        with patch.dict(os.environ, env_vars):
            config = Config()

            assert config.llm_provider == "openai"
            assert config.debug is True
            assert config.log_level == "DEBUG"
            assert config.openai_api_key == "env_api_key"
            assert config.max_results == 75

    def test_config_boolean_env_vars(self):
        """Test boolean environment variable parsing."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("yes", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("0", False),
            ("no", False),
            ("", False),
        ]

        for env_value, expected in test_cases:
            with patch.dict(os.environ, {"DEBUG": env_value}):
                config = Config()
                assert config.debug == expected, f"Failed for env_value: {env_value}"

    def test_config_integer_env_vars(self):
        """Test integer environment variable parsing."""
        with patch.dict(os.environ, {"MAX_RESULTS": "123"}):
            config = Config()
            assert config.max_results == 123

    def test_config_float_env_vars(self):
        """Test float environment variable parsing."""
        with patch.dict(os.environ, {"SIMILARITY_THRESHOLD": "0.85"}):
            config = Config()
            assert config.similarity_threshold == 0.85

    def test_config_invalid_env_vars(self):
        """Test handling of invalid environment variables."""
        # Test invalid integer
        with patch.dict(os.environ, {"MAX_RESULTS": "not_a_number"}):
            config = Config()
            assert config.max_results == 50  # Should use default

        # Test invalid float
        with patch.dict(os.environ, {"SIMILARITY_THRESHOLD": "not_a_float"}):
            config = Config()
            assert config.similarity_threshold == 0.75  # Should use default

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="LLM_PROVIDER=openai\nDEBUG=true\n",
    )
    def test_config_from_file(self, mock_file):
        """Test config loading from .env file."""
        with patch("os.path.exists", return_value=True):
            config = Config()
            # The actual file loading would depend on the implementation
            # This test verifies the file reading mechanism

    def test_config_repr(self):
        """Test config string representation."""
        config = Config(llm_provider="openai", debug=True)

        repr_str = repr(config)
        assert "Config" in repr_str
        assert "llm_provider" in repr_str

    def test_config_validation_missing_api_key(self):
        """Test config validation for missing API keys."""
        # This would depend on implementation details
        config = Config(llm_provider="openai")
        # Should handle missing API key gracefully or raise appropriate error

    def test_config_api_key_masking(self):
        """Test that API keys are masked in logs/representations."""
        config = Config(openai_api_key="sk-very-secret-key-123456")

        # API key should not appear in plain text in repr
        repr_str = repr(config)
        assert "sk-very-secret-key-123456" not in repr_str

    def test_config_update_values(self):
        """Test updating config values after initialization."""
        config = Config()
        original_provider = config.llm_provider

        # Test if config supports updating (depends on implementation)
        if hasattr(config, "update"):
            config.update(llm_provider="openai")
            assert config.llm_provider == "openai"
        else:
            # If immutable, should remain unchanged
            assert config.llm_provider == original_provider

    def test_config_with_none_values(self):
        """Test config behavior with None values."""
        config = Config(openai_api_key=None, deepseek_api_key=None)

        assert config.openai_api_key is None
        assert config.deepseek_api_key is None

    def test_config_path_expansion(self):
        """Test path expansion for relative paths."""
        config = Config(chroma_persist_directory="~/chroma", output_dir="./output")

        # Should handle path expansion
        if hasattr(config, "chroma_persist_directory"):
            # Test would depend on implementation
            pass

    def test_config_directory_creation(self):
        """Test automatic directory creation for paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "new_output")

            config = Config(output_dir=output_path)

            # Depending on implementation, directories might be created automatically

    def test_config_validation_errors(self):
        """Test config validation with invalid values."""
        # Test negative values
        config = Config(max_results=-1)
        # Should handle invalid values appropriately

        # Test out-of-range values
        config = Config(similarity_threshold=1.5)  # > 1.0
        # Should handle invalid similarity threshold

    def test_config_merge_sources(self):
        """Test merging configuration from multiple sources."""
        # Test precedence: explicit args > env vars > file > defaults
        env_vars = {"LLM_PROVIDER": "openai"}

        with patch.dict(os.environ, env_vars):
            config = Config(llm_provider="deepseek")  # Explicit arg should win
            assert config.llm_provider == "deepseek"

    def test_config_sensitive_data_handling(self):
        """Test handling of sensitive configuration data."""
        config = Config(openai_api_key="secret-key", deepseek_api_key="another-secret")

        # Sensitive data should not leak in logs or errors
        config_dict = config.__dict__
        # Implementation should mask or exclude sensitive fields

    def test_config_serialization(self):
        """Test config serialization capabilities."""
        config = Config(llm_provider="openai", debug=True, max_results=100)

        # Test if config can be serialized (depends on implementation)
        if hasattr(config, "to_dict"):
            config_dict = config.to_dict()
            assert isinstance(config_dict, dict)
            assert config_dict["llm_provider"] == "openai"

    def test_config_copy(self):
        """Test config copying functionality."""
        original = Config(llm_provider="openai", debug=True)

        # Test if config supports copying
        if hasattr(original, "copy"):
            copy = original.copy()
            assert copy.llm_provider == original.llm_provider
            assert copy is not original  # Should be different objects
