"""
AI Agent for Automated Literature Review & Summarization

A Python package for automating literature review and summarization using LLMs,
vector databases, and advanced NLP techniques.
"""

__version__ = "0.1.0"
__author__ = "Literature Review AI Team"
__email__ = "team@litreview.ai"

from .agent import LiteratureAgent
from .utils.config import Config
from .utils.logger import setup_logger

# Package-level configuration
config = Config()
logger = setup_logger()

__all__ = [
    "LiteratureAgent",
    "config",
    "logger",
    "Config",
    "setup_logger",
] 