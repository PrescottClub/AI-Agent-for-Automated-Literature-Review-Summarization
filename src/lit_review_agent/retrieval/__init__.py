"""Literature retrieval modules for accessing various academic data sources."""

from .arxiv_client import ArxivClient
from .pdf_processor import PDFProcessor
from .base_retriever import BaseRetriever, LiteratureItem

__all__ = [
    "ArxivClient",
    "PDFProcessor",
    "BaseRetriever",
    "LiteratureItem",
]
