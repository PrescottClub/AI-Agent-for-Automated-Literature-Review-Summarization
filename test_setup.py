#!/usr/bin/env python3
"""
Test script to verify the AI Literature Review Agent setup and configuration.
Run this script to check if everything is properly configured.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.lit_review_agent.utils.config import Config
from src.lit_review_agent.ai_core.llm_manager import LLMManager
from src.lit_review_agent.processing.vector_store import VectorStore


def test_config():
    """Test configuration loading."""
    print("🔧 Testing Configuration...")
    try:
        config = Config()
        print(f"✅ Configuration loaded successfully")
        print(f"   LLM Provider: {config.llm_provider}")
        print(f"   DeepSeek API Key: {'✅ Set' if config.deepseek_api_key else '❌ Not set'}")
        print(f"   OpenAI API Key: {'✅ Set' if config.openai_api_key else '❌ Not set'}")
        print(f"   Sentence Transformer Model: {config.sentence_transformer_model}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


async def test_llm_manager():
    """Test LLM Manager with mock provider."""
    print("\n🤖 Testing LLM Manager...")
    try:
        # Test with mock provider to avoid API calls
        config = Config(llm_provider="mock")
        llm_manager = LLMManager(config)
        
        # Test chat completion
        response = await llm_manager.generate_chat_completion(
            messages=[{"role": "user", "content": "Hello, test!"}]
        )
        print(f"✅ Chat completion test passed")
        
        # Test embedding
        embeddings = await llm_manager.generate_embedding(["Test text"])
        print(f"✅ Embedding test passed (dimension: {len(embeddings[0])})")
        
        return True
    except Exception as e:
        print(f"❌ LLM Manager error: {e}")
        return False


def test_vector_store():
    """Test Vector Store initialization."""
    print("\n📊 Testing Vector Store...")
    try:
        config = Config()
        vector_store = VectorStore(
            persist_directory="./test_data/chroma_db",
            collection_name="test_collection",
            embedding_model=config.sentence_transformer_model
        )
        print(f"✅ Vector Store initialized successfully")
        
        # Test basic functionality
        stats = vector_store.get_collection_stats()
        print(f"   Collection stats: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Vector Store error: {e}")
        return False


def test_dependencies():
    """Test required dependencies."""
    print("\n📦 Testing Dependencies...")
    
    dependencies = [
        ("httpx", "HTTP client for API calls"),
        ("chromadb", "Vector database"),
        ("sentence_transformers", "Embedding models"),
        ("typer", "CLI framework"),
        ("rich", "Rich text and beautiful formatting"),
        ("pydantic", "Data validation"),
        ("python-dotenv", "Environment variable loading"),
    ]
    
    all_good = True
    for package, description in dependencies:
        try:
            __import__(package)
            print(f"✅ {package}: {description}")
        except ImportError:
            print(f"❌ {package}: Missing - {description}")
            all_good = False
    
    return all_good


async def main():
    """Run all tests."""
    print("🚀 AI Literature Review Agent - Setup Test\n")
    
    tests = [
        ("Configuration", test_config),
        ("Dependencies", test_dependencies),
        ("LLM Manager", test_llm_manager),
        ("Vector Store", test_vector_store),
    ]
    
    results = []
    for test_name, test_func in tests:
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("📋 Test Results Summary:")
    print("="*50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Copy config/config.example.env to .env")
        print("2. Add your API keys to .env")
        print("3. Run: python -m src.lit_review_agent.cli setup")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Check your .env configuration")
        print("3. Ensure API keys are properly set")


if __name__ == "__main__":
    asyncio.run(main()) 