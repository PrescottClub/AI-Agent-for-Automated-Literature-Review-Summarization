"""Unit tests for LLMManager class."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from typing import List, Dict, Any

from src.lit_review_agent.ai_core.llm_manager import LLMManager, LLMManagerError
from src.lit_review_agent.utils.config import Config


@pytest.mark.unit
class TestLLMManager:
    """Test cases for LLMManager class."""

    def test_init_with_mock_provider(self, mock_config):
        """Test LLMManager initialization with mock provider."""
        llm_manager = LLMManager(config=mock_config)
        
        assert llm_manager.provider == "mock"
        assert llm_manager.model_name == "mock_model"
        assert llm_manager.api_key is None
        assert llm_manager.timeout == mock_config.llm_timeout_seconds

    def test_init_with_openai_provider(self):
        """Test LLMManager initialization with OpenAI provider."""
        config = Config(
            llm_provider="openai",
            openai_api_key="test_key",
            openai_model="gpt-4"
        )
        
        llm_manager = LLMManager(config=config)
        
        assert llm_manager.provider == "openai"
        assert llm_manager.api_key == "test_key"
        assert llm_manager.model_name == "gpt-4"
        assert llm_manager.base_url == "https://api.openai.com/v1"

    def test_init_with_deepseek_provider(self):
        """Test LLMManager initialization with DeepSeek provider."""
        config = Config(
            llm_provider="deepseek",
            deepseek_api_key="test_deepseek_key",
            deepseek_model="deepseek-chat"
        )
        
        llm_manager = LLMManager(config=config)
        
        assert llm_manager.provider == "deepseek"
        assert llm_manager.api_key == "test_deepseek_key"
        assert llm_manager.model_name == "deepseek-chat"
        assert llm_manager.base_url == "https://api.deepseek.com/v1"

    def test_init_without_api_key_raises_error(self):
        """Test that missing API key raises LLMManagerError."""
        config = Config(llm_provider="openai")  # No API key provided
        
        with pytest.raises(LLMManagerError, match="OpenAI API key is not configured"):
            LLMManager(config=config)

    def test_init_with_unsupported_provider_raises_error(self):
        """Test that unsupported provider raises LLMManagerError."""
        config = Config(llm_provider="unsupported_provider")
        
        with pytest.raises(LLMManagerError, match="Unsupported LLM provider"):
            LLMManager(config=config)

    @pytest.mark.asyncio
    async def test_generate_chat_completion_mock_provider(self, mock_llm_manager, mock_api_response):
        """Test chat completion with mock provider."""
        messages = [{"role": "user", "content": "Hello, world!"}]
        
        response = await mock_llm_manager.generate_chat_completion(messages)
        
        assert response is not None
        assert "choices" in response
        assert len(response["choices"]) > 0
        assert response["choices"][0]["message"]["content"] == "This is a mock response."

    @pytest.mark.asyncio
    async def test_generate_chat_completion_with_parameters(self, mock_llm_manager):
        """Test chat completion with custom parameters."""
        messages = [{"role": "user", "content": "Test message"}]
        
        response = await mock_llm_manager.generate_chat_completion(
            messages=messages,
            max_tokens=100,
            temperature=0.5
        )
        
        assert response is not None
        assert "choices" in response

    @pytest.mark.asyncio
    async def test_generate_embedding_mock_provider(self, mock_llm_manager):
        """Test embedding generation with mock provider."""
        input_texts = ["Hello world", "Test embedding"]
        
        embeddings = await mock_llm_manager.generate_embedding(input_texts)
        
        assert embeddings is not None
        assert len(embeddings) == len(input_texts)
        assert all(isinstance(emb, list) for emb in embeddings)

    def test_configure_provider_ollama(self):
        """Test configuration for Ollama provider."""
        config = Config(
            llm_provider="ollama",
            ollama_model="llama3",
            ollama_api_base="http://localhost:11434/api"
        )
        
        llm_manager = LLMManager(config=config)
        
        assert llm_manager.provider == "ollama"
        assert llm_manager.model_name == "llama3"
        assert llm_manager.base_url == "http://localhost:11434/api"
        assert llm_manager.api_key is None  # Ollama doesn't use API key

    @pytest.mark.asyncio
    async def test_generate_chat_completion_empty_messages(self, mock_llm_manager):
        """Test chat completion with empty messages."""
        messages = []
        
        response = await mock_llm_manager.generate_chat_completion(messages)
        
        # Mock provider should still return a response
        assert response is not None

    @pytest.mark.asyncio
    async def test_generate_embedding_empty_input(self, mock_llm_manager):
        """Test embedding generation with empty input."""
        input_texts = []
        
        embeddings = await mock_llm_manager.generate_embedding(input_texts)
        
        assert embeddings == []

    @pytest.mark.asyncio
    async def test_generate_embedding_single_text(self, mock_llm_manager):
        """Test embedding generation with single text."""
        input_texts = ["Single test text"]
        
        embeddings = await mock_llm_manager.generate_embedding(input_texts)
        
        assert len(embeddings) == 1
        assert isinstance(embeddings[0], list)


@pytest.mark.integration
class TestLLMManagerIntegration:
    """Integration tests for LLMManager with real API calls."""
    
    @pytest.mark.requires_api
    @pytest.mark.slow
    async def test_real_openai_api_call(self):
        """Test actual OpenAI API call (requires valid API key)."""
        # This test requires a real API key and will be skipped by default
        pytest.skip("Requires real OpenAI API key")
        
        # Uncomment and add real API key for integration testing
        # config = Config(
        #     llm_provider="openai",
        #     openai_api_key="your-real-api-key-here"
        # )
        # llm_manager = LLMManager(config=config)
        # 
        # messages = [{"role": "user", "content": "Hello!"}]
        # response = await llm_manager.generate_chat_completion(messages)
        # 
        # assert response is not None
        # assert "choices" in response 