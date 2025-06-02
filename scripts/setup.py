#!/usr/bin/env python3
"""Setup script for Tsearch project."""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Successfully ran: {' '.join(cmd)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to run: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 9):
        print("✗ Python 3.9 or higher is required")
        return False
    print(
        f"✓ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True


def install_package():
    """Install the package in development mode."""
    print("Installing Tsearch package...")
    return run_command([sys.executable, "-m", "pip", "install", "-e", "."])


def download_spacy_model():
    """Download required spaCy model."""
    print("Downloading spaCy English model...")
    return run_command([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])


def download_nltk_data():
    """Download required NLTK data."""
    print("Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        print("✓ Successfully downloaded NLTK data")
        return True
    except Exception as e:
        print(f"✗ Failed to download NLTK data: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    directories = [
        Path("data"),
        Path("data/chroma_db"),
        Path("data/outputs"),
        Path("logs"),
        Path("config"),
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

    return True


def create_example_env():
    """Create example environment file."""
    env_content = """# Tsearch Configuration
# Copy this file to .env and customize for your setup

# Core Settings
LOG_LEVEL=INFO
DEBUG=false

# LLM Provider (openai, deepseek, ollama, mock)
LLM_PROVIDER=deepseek

# OpenAI Settings (if using OpenAI)
# OPENAI_API_KEY=your_openai_api_key_here
# OPENAI_MODEL=gpt-3.5-turbo

# DeepSeek Settings (if using DeepSeek)
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
# DEEPSEEK_MODEL=deepseek-chat

# Ollama Settings (if using local Ollama)
# OLLAMA_API_BASE=http://localhost:11434/api
# OLLAMA_MODEL=llama3

# Semantic Scholar Settings (optional, for higher rate limits)
# SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key_here

# Advanced Settings
MAX_RESULTS=50
ARXIV_MAX_RESULTS=100
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
OUTPUT_DIR=./data/outputs
"""

    config_path = Path("config/config.example.env")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(env_content)

    print(f"✓ Created example configuration: {config_path}")
    print(f"  Copy this to .env and customize for your setup")
    return True


def run_tests():
    """Run basic tests to verify installation."""
    print("Running basic tests...")
    return run_command([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"])


def main():
    """Main setup function."""
    print("🚀 Setting up Tsearch project...")
    print("=" * 50)

    steps = [
        ("Checking Python version", check_python_version),
        ("Installing package", install_package),
        ("Creating directories", create_directories),
        ("Creating example configuration", create_example_env),
        ("Downloading spaCy model", download_spacy_model),
        ("Downloading NLTK data", download_nltk_data),
    ]

    failed_steps = []

    for step_name, step_func in steps:
        print(f"\n📦 {step_name}...")
        if not step_func():
            failed_steps.append(step_name)

    print("\n" + "=" * 50)
    print("📋 Setup Summary:")

    if failed_steps:
        print(f"✗ Setup completed with {len(failed_steps)} failed steps:")
        for step in failed_steps:
            print(f"  - {step}")
        print("\n💡 You may need to:")
        print("  - Check your internet connection")
        print("  - Install missing system dependencies")
        print("  - Manually download required models")
    else:
        print("✓ Setup completed successfully!")
        print("\n🎉 Next steps:")
        print("  1. Copy config/config.example.env to .env")
        print("  2. Add your API keys to .env")
        print("  3. Run: tsearch --help")
        print("  4. Or try: python -m lit_review_agent.cli --help")

    # Optionally run tests
    if not failed_steps:
        print("\n🧪 Would you like to run tests? (y/N): ", end="")
        response = input().lower().strip()
        if response in ['y', 'yes']:
            run_tests()


if __name__ == "__main__":
    main()
