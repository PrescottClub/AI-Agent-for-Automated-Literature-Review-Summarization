"""ArXiv API client for literature retrieval."""

import asyncio
from datetime import datetime
from typing import List, Optional

import arxiv
from ..utils.logger import LoggerMixin
from .base_retriever import BaseRetriever, LiteratureItem


class ArxivClient(BaseRetriever, LoggerMixin):
    """Client for retrieving literature from arXiv."""

    def __init__(self, max_results: int = 100, **kwargs):
        """
        Initialize the ArXiv client.

        Args:
            max_results: Default maximum results per query
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.max_results = max_results
        self.client = arxiv.Client()

        self.logger.info(f"Initialized ArXiv client with max_results={max_results}")

    def get_source_name(self) -> str:
        """Get the source name."""
        return "arxiv"

    async def search(
        self,
        query: str,
        max_results: int = 10,
        sort_by: arxiv.SortCriterion = arxiv.SortCriterion.Relevance,
        sort_order: arxiv.SortOrder = arxiv.SortOrder.Descending,
        **kwargs,
    ) -> List[LiteratureItem]:
        """
        Search ArXiv for papers.

        Args:
            query: Search query
            max_results: Maximum number of results
            sort_by: Sort criterion
            sort_order: Sort order
            **kwargs: Additional search parameters

        Returns:
            List of literature items
        """
        try:
            self.logger.info(
                f"Searching ArXiv: query='{query}', max_results={max_results}"
            )

            # Create search object
            search = arxiv.Search(
                query=query,
                max_results=min(max_results, self.max_results),
                sort_by=sort_by,
                sort_order=sort_order,
            )

            # Execute search asynchronously
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None, lambda: list(self.client.results(search))
            )

            # Convert to LiteratureItem objects
            literature_items = []
            for result in results:
                item = self._convert_arxiv_result(result)
                literature_items.append(item)

            self.logger.info(f"Retrieved {len(literature_items)} papers from ArXiv")
            return literature_items

        except Exception as e:
            self.logger.error(f"Error searching ArXiv: {e}")
            return []

    async def get_by_id(self, item_id: str) -> Optional[LiteratureItem]:
        """
        Retrieve a specific paper by ArXiv ID.

        Args:
            item_id: ArXiv ID (e.g., '2301.12345')

        Returns:
            Literature item if found, None otherwise
        """
        try:
            self.logger.info(f"Retrieving ArXiv paper by ID: {item_id}")

            # Create search for specific ID
            search = arxiv.Search(id_list=[item_id])

            # Execute search asynchronously
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None, lambda: list(self.client.results(search))
            )

            if results:
                item = self._convert_arxiv_result(results[0])
                self.logger.info(f"Found ArXiv paper: {item.title}")
                return item
            else:
                self.logger.warning(f"ArXiv paper not found: {item_id}")
                return None

        except Exception as e:
            self.logger.error(f"Error retrieving ArXiv paper {item_id}: {e}")
            return None

    async def search_by_category(
        self, category: str, max_results: int = 10, **kwargs
    ) -> List[LiteratureItem]:
        """
        Search ArXiv by category.

        Args:
            category: ArXiv category (e.g., 'cs.AI', 'cs.LG')
            max_results: Maximum number of results
            **kwargs: Additional search parameters

        Returns:
            List of literature items
        """
        query = f"cat:{category}"
        return await self.search(query, max_results, **kwargs)

    async def search_by_author(
        self, author: str, max_results: int = 10, **kwargs
    ) -> List[LiteratureItem]:
        """
        Search ArXiv by author.

        Args:
            author: Author name
            max_results: Maximum number of results
            **kwargs: Additional search parameters

        Returns:
            List of literature items
        """
        query = f"au:{author}"
        return await self.search(query, max_results, **kwargs)

    async def search_recent(
        self, query: str, days: int = 30, max_results: int = 10, **kwargs
    ) -> List[LiteratureItem]:
        """
        Search for recent papers.

        Args:
            query: Search query
            days: Number of days to look back
            max_results: Maximum number of results
            **kwargs: Additional search parameters

        Returns:
            List of recent literature items
        """
        # ArXiv doesn't support date filtering in the API directly,
        # so we'll retrieve more results and filter client-side
        expanded_results = max_results * 3
        all_items = await self.search(query, expanded_results, **kwargs)

        # Filter by date
        cutoff_date = datetime.utcnow()
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)

        recent_items = self.filter_by_date(all_items, start_date=cutoff_date)

        return recent_items[:max_results]

    def _convert_arxiv_result(self, arxiv_result) -> LiteratureItem:
        """
        Convert ArXiv result to LiteratureItem.

        Args:
            arxiv_result: ArXiv API result object

        Returns:
            LiteratureItem object
        """
        # Extract ArXiv ID from URL
        arxiv_id = arxiv_result.entry_id.split("/")[-1]

        # Extract authors
        authors = [str(author) for author in arxiv_result.authors]

        # Extract categories
        categories = [str(cat) for cat in arxiv_result.categories]

        # Create LiteratureItem
        return LiteratureItem(
            id=f"arxiv:{arxiv_id}",
            title=arxiv_result.title,
            authors=authors,
            abstract=arxiv_result.summary,
            publication_date=arxiv_result.published,
            journal=arxiv_result.journal_ref,
            doi=arxiv_result.doi,
            arxiv_id=arxiv_id,
            url=arxiv_result.entry_id,
            pdf_url=arxiv_result.pdf_url,
            categories=categories,
            source="arxiv",
            metadata={
                "updated": (
                    arxiv_result.updated.isoformat() if arxiv_result.updated else None
                ),
                "comment": arxiv_result.comment,
                "primary_category": (
                    str(arxiv_result.primary_category)
                    if arxiv_result.primary_category
                    else None
                ),
                "links": (
                    [str(link) for link in arxiv_result.links]
                    if arxiv_result.links
                    else []
                ),
            },
        )

    def get_supported_categories(self) -> List[str]:
        """
        Get list of supported ArXiv categories.

        Returns:
            List of category codes
        """
        return [
            # Computer Science
            "cs.AI",  # Artificial Intelligence
            "cs.CL",  # Computation and Language
            "cs.CV",  # Computer Vision and Pattern Recognition
            "cs.LG",  # Machine Learning
            "cs.NE",  # Neural and Evolutionary Computing
            "cs.RO",  # Robotics
            # Statistics
            "stat.ML",  # Machine Learning
            "stat.AP",  # Applications
            # Mathematics
            "math.OC",  # Optimization and Control
            "math.ST",  # Statistics Theory
            # Physics
            "physics.data-an",  # Data Analysis
            # Quantitative Biology
            "q-bio.QM",  # Quantitative Methods
            # Economics
            "econ.EM",  # Econometrics
        ]
