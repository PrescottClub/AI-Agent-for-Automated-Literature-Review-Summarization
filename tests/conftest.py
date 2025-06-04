"""Pytest configuration and fixtures for the literature review agent tests."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any, List
import tempfile
import os

# Import our application modules
from src.lit_review_agent.utils.config import Config
from src.lit_review_agent.ai_core.llm_manager import LLMManager


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return Config(
        llm_provider="mock",
        debug=True,
        log_level="DEBUG",
        chroma_persist_directory=tempfile.mkdtemp(),
        output_dir=tempfile.mkdtemp(),
    )


@pytest.fixture
def mock_llm_manager(mock_config):
    """Mock LLM manager for testing."""
    return LLMManager(config=mock_config)


@pytest.fixture
def sample_papers() -> List[Dict[str, Any]]:
    """Sample paper data for testing."""
    return [
        {
            "title": "Deep Learning for Natural Language Processing",
            "authors": [{"name": "John Doe", "affiliation": "MIT"}],
            "abstract": "This paper explores deep learning techniques for NLP tasks.",
            "publication_date": "2023-01-15",
            "doi": "10.1000/123456",
            "arxiv_id": "2301.12345",
            "url": "https://arxiv.org/abs/2301.12345",
            "source": "arxiv",
        },
        {
            "title": "Transformer Architecture for Text Generation",
            "authors": [
                {"name": "Jane Smith", "affiliation": "Stanford"},
                {"name": "Bob Johnson", "affiliation": "Google"},
            ],
            "abstract": "We propose improvements to transformer architecture.",
            "publication_date": "2023-02-20",
            "doi": "10.1000/654321",
            "semantic_scholar_id": "abc123",
            "url": "https://semanticscholar.org/paper/abc123",
            "source": "semantic_scholar",
        },
    ]


@pytest.fixture
def sample_search_response():
    """Sample search response for testing."""
    return {
        "status": "success",
        "data": {
            "papers": [],
            "total_found": 0,
            "search_time": 0.5,
            "query": "test query",
        },
        "message": "Search completed successfully",
    }


@pytest.fixture
def mock_api_response():
    """Mock API response for testing external API calls."""
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response for testing.",
                }
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
    }


@pytest.fixture
async def async_mock():
    """Create an async mock for testing async functions."""
    mock = AsyncMock()
    return mock


@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Cleanup temporary files after each test."""
    temp_dirs = []

    def track_temp_dir(path):
        temp_dirs.append(path)
        return path

    yield track_temp_dir

    # Cleanup
    import shutil

    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


# Custom markers for different test types
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line(
        "markers", "requires_api: mark test as requiring external API"
    )


# Test data constants
TEST_SEARCH_QUERY = "machine learning natural language processing"
TEST_MAX_RESULTS = 5
TEST_PAPER_ID = "test_paper_123"
TEST_DOI = "10.1000/test.123"
TEST_ARXIV_ID = "2301.12345"
