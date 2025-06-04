"""Base classes and data models for literature retrieval."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LiteratureItem(BaseModel):
    """Data model for a literature item (paper, article, etc.)."""

    id: str = Field(..., description="Unique identifier for the item")
    title: str = Field(..., description="Title of the literature item")
    authors: List[str] = Field(default_factory=list, description="List of author names")
    abstract: Optional[str] = Field(None, description="Abstract or summary")
    full_text: Optional[str] = Field(None, description="Full text content if available")

    # Publication details
    journal: Optional[str] = Field(None, description="Journal or venue name")
    publication_date: Optional[datetime] = Field(None, description="Publication date")
    volume: Optional[str] = Field(None, description="Volume number")
    issue: Optional[str] = Field(None, description="Issue number")
    pages: Optional[str] = Field(None, description="Page numbers")

    # Identifiers
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    arxiv_id: Optional[str] = Field(None, description="arXiv identifier")
    pmid: Optional[str] = Field(None, description="PubMed identifier")
    url: Optional[str] = Field(None, description="URL to the paper")
    pdf_url: Optional[str] = Field(None, description="Direct PDF URL")

    # Categories and tags
    categories: List[str] = Field(
        default_factory=list, description="Subject categories"
    )
    keywords: List[str] = Field(default_factory=list, description="Keywords or tags")

    # Metrics
    citation_count: Optional[int] = Field(None, description="Number of citations")

    # Metadata
    source: str = Field(
        ..., description="Source of the literature (e.g., 'arxiv', 'pubmed')"
    )
    retrieved_at: datetime = Field(
        default_factory=datetime.utcnow, description="When item was retrieved"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat() if v else None}

    @property
    def author_string(self) -> str:
        """Get formatted author string."""
        if not self.authors:
            return "Unknown"
        elif len(self.authors) == 1:
            return self.authors[0]
        elif len(self.authors) <= 3:
            return ", ".join(self.authors)
        else:
            return f"{self.authors[0]} et al."

    @property
    def year(self) -> Optional[int]:
        """Get publication year."""
        return self.publication_date.year if self.publication_date else None

    def to_citation(self, style: str = "apa") -> str:
        """
        Generate a citation string.

        Args:
            style: Citation style ('apa', 'mla', 'chicago')

        Returns:
            Formatted citation string
        """
        if style.lower() == "apa":
            author_part = self.author_string
            year_part = f"({self.year})" if self.year else ""
            title_part = self.title
            journal_part = f"{self.journal}" if self.journal else ""

            parts = [p for p in [author_part, year_part, title_part, journal_part] if p]
            return ". ".join(parts) + "."

        # Default to simple format
        return f"{self.author_string}. {self.title}. {self.journal or 'Unknown'}. {self.year or 'Unknown'}."


class BaseRetriever(ABC):
    """Abstract base class for literature retrievers."""

    def __init__(self, **kwargs):
        """Initialize the retriever."""
        self.config = kwargs

    @abstractmethod
    async def search(
        self, query: str, max_results: int = 10, **kwargs
    ) -> List[LiteratureItem]:
        """
        Search for literature items.

        Args:
            query: Search query
            max_results: Maximum number of results to return
            **kwargs: Additional search parameters

        Returns:
            List of literature items
        """
        pass

    @abstractmethod
    async def get_by_id(self, item_id: str) -> Optional[LiteratureItem]:
        """
        Retrieve a specific literature item by ID.

        Args:
            item_id: Unique identifier for the item

        Returns:
            Literature item if found, None otherwise
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get the name of this retriever's source.

        Returns:
            Source name (e.g., 'arxiv', 'pubmed')
        """
        pass

    async def search_multiple_queries(
        self, queries: List[str], max_results_per_query: int = 10
    ) -> List[LiteratureItem]:
        """
        Search for multiple queries and combine results.

        Args:
            queries: List of search queries
            max_results_per_query: Maximum results per query

        Returns:
            Combined list of literature items
        """
        all_items = []
        seen_ids = set()

        for query in queries:
            items = await self.search(query, max_results_per_query)
            for item in items:
                if item.id not in seen_ids:
                    all_items.append(item)
                    seen_ids.add(item.id)

        return all_items

    def filter_by_date(
        self,
        items: List[LiteratureItem],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[LiteratureItem]:
        """
        Filter literature items by publication date.

        Args:
            items: List of literature items
            start_date: Minimum publication date
            end_date: Maximum publication date

        Returns:
            Filtered list of items
        """
        filtered = []

        for item in items:
            if not item.publication_date:
                continue

            if start_date and item.publication_date < start_date:
                continue

            if end_date and item.publication_date > end_date:
                continue

            filtered.append(item)

        return filtered

    def sort_by_relevance(
        self, items: List[LiteratureItem], query: str
    ) -> List[LiteratureItem]:
        """
        Sort literature items by relevance to query.

        Args:
            items: List of literature items
            query: Original search query

        Returns:
            Sorted list of items
        """
        # Simple relevance scoring based on query terms in title and abstract
        query_terms = set(query.lower().split())

        def relevance_score(item: LiteratureItem) -> float:
            score = 0.0

            # Check title
            if item.title:
                title_terms = set(item.title.lower().split())
                score += len(query_terms.intersection(title_terms)) * 2.0

            # Check abstract
            if item.abstract:
                abstract_terms = set(item.abstract.lower().split())
                score += len(query_terms.intersection(abstract_terms)) * 1.0

            # Boost recent papers
            if item.publication_date:
                years_old = (datetime.utcnow() - item.publication_date).days / 365.25
                score += max(0, 5 - years_old) * 0.1

            # Boost highly cited papers
            if item.citation_count:
                score += min(item.citation_count / 100.0, 2.0)

            return score

        return sorted(items, key=relevance_score, reverse=True)
