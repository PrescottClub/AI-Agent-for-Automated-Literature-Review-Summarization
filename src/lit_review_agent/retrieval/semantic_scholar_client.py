"""Semantic Scholar API client for literature retrieval (placeholder)."""

from typing import List, Optional, Dict, Any
import httpx
import asyncio
from datetime import datetime

from ..utils.logger import get_logger, LoggerMixin
from .base_retriever import BaseRetriever, LiteratureItem
from ..utils.config import Config # To access potential API key or other configs

logger = get_logger(__name__)

class SemanticScholarError(Exception):
    """Custom exception for Semantic Scholar client errors."""
    pass

class SemanticScholarClient(BaseRetriever, LoggerMixin):
    """
    A client to retrieve literature from the Semantic Scholar API.
    """
    # API details: https://api.semanticscholar.org/api-docs/graph
    DEFAULT_API_URL = "https://api.semanticscholar.org/graph/v1"
    # Fields to request for paper search. Add more as needed based on LiteratureItem.
    # Details: https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers
    DEFAULT_PAPER_FIELDS = [
        "paperId", "externalIds", "url", "title", "abstract", "authors", 
        "venue", "year", "publicationDate", "publicationTypes", "journal",
        "citationCount", "fieldsOfStudy", "s2FieldsOfStudy"
    ]

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None, config: Optional[Config] = None):
        super().__init__() # Initialize LoggerMixin
        BaseRetriever.__init__(self) # Initialize BaseRetriever
        self.api_url = api_url or self.DEFAULT_API_URL
        self.api_key = api_key # May be needed for higher rate limits or specific features
        self.config = config # General app config if needed

        if self.config and not self.api_key:
            self.api_key = self.config.semantic_scholar_api_key
        
        self.logger.info(f"SemanticScholarClient initialized. API URL: {self.api_url}, API Key set: {bool(self.api_key)}")

    def get_source_name(self) -> str:
        return "semantic_scholar"

    def _parse_publication_date(self, pub_date_str: Optional[str]) -> Optional[datetime]:
        if not pub_date_str:
            return None
        try:
            # Common formats: YYYY-MM-DD, YYYY-MM, YYYY
            if len(pub_date_str) == 10: # YYYY-MM-DD
                return datetime.strptime(pub_date_str, "%Y-%m-%d")
            elif len(pub_date_str) == 7: # YYYY-MM
                return datetime.strptime(pub_date_str, "%Y-%m")
            elif len(pub_date_str) == 4: # YYYY
                return datetime.strptime(pub_date_str, "%Y")
        except ValueError as e:
            self.logger.warning(f"Could not parse publication date '{pub_date_str}': {e}")
        return None

    def _to_literature_item(self, paper_data: Dict[str, Any]) -> LiteratureItem:
        """Converts a Semantic Scholar paper data dictionary to a LiteratureItem."""
        authors = [author_info["name"] for author_info in paper_data.get("authors", []) if author_info.get("name")]
        
        # Extract various IDs
        external_ids = paper_data.get("externalIds", {})
        doi = external_ids.get("DOI")
        arxiv_id_raw = external_ids.get("ArXiv")
        # ArXiv ID from S2 might have 'arXiv:' prefix or be just the ID
        arxiv_id = arxiv_id_raw.split(':')[-1] if arxiv_id_raw else None

        pub_date = self._parse_publication_date(paper_data.get("publicationDate"))
        
        # Keywords/Fields of study
        # s2FieldsOfStudy is more granular, fieldsOfStudy is broader.
        # We can combine them or choose one.
        keywords = []
        if paper_data.get("fieldsOfStudy"):
            keywords.extend(paper_data["fieldsOfStudy"])
        # for s2_field_info in paper_data.get("s2FieldsOfStudy", []):
        #     if s2_field_info.get("category") and s2_field_info["category"] not in keywords:
        #         keywords.append(s2_field_info["category"])
        # For simplicity, let's stick to fieldsOfStudy for now if present
        keywords = list(set(kw for kw in keywords if kw)) # Unique and non-empty

        journal_info = paper_data.get("journal")
        journal_name = journal_info.get("name") if journal_info else paper_data.get("venue")
        journal_volume = journal_info.get("volume") if journal_info else None
        journal_pages = journal_info.get("pages") if journal_info else None

        return LiteratureItem(
            id=f"s2:{paper_data['paperId']}", # Prefix with source
            title=paper_data.get("title", "N/A"),
            authors=authors,
            abstract=paper_data.get("abstract"),
            # full_text: Semantic Scholar API itself doesn't usually provide full text directly.
            # We rely on pdf_url if available, and PDFProcessor for extraction.
            journal=journal_name,
            publication_date=pub_date,
            volume=journal_volume,
            pages=journal_pages,
            doi=doi,
            arxiv_id=arxiv_id,
            url=paper_data.get("url"), # URL to Semantic Scholar page
            # pdf_url: S2 might provide OpenAccessPdf in externalIds, or one needs to derive it.
            # For now, we are not explicitly extracting a direct PDF URL from S2 results here,
            # as it's not a standard guaranteed field in basic paper search.
            # If needed, one would look into externalIds.OpenAccessPdf.url or similar.
            categories=paper_data.get("publicationTypes", []) or [],
            keywords=keywords,
            citation_count=paper_data.get("citationCount"),
            source=self.get_source_name(),
            metadata=paper_data # Store raw S2 data for potential further use
        )

    async def search_papers(
        self,
        query: str,
        max_results: int = 10,
        fields: Optional[List[str]] = None,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
    ) -> List[LiteratureItem]:
        """
        Searches for papers on Semantic Scholar.

        Args:
            query: The search query string.
            max_results: Maximum number of papers to return.
            fields: List of fields to retrieve for each paper.
            year_start: Filter papers published from this year.
            year_end: Filter papers published up to this year.

        Returns:
            A list of LiteratureItem objects.
        """
        search_url = f"{self.api_url}/paper/search"
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key # S2 uses x-api-key header
        
        params: Dict[str, Any] = {
            "query": query,
            "limit": max_results,
            "fields": ",".join(fields or self.DEFAULT_PAPER_FIELDS)
        }
        if year_start and year_end and year_start > year_end:
            self.logger.warning("year_start cannot be after year_end. Ignoring year filters.")
        elif year_start or year_end:            
            year_filter_parts = []
            if year_start:
                year_filter_parts.append(str(year_start))
            year_filter_parts.append("-")
            if year_end:
                year_filter_parts.append(str(year_end))
            else: # If only start_year is given, search from start_year to current year
                year_filter_parts.append(str(datetime.now().year))
            # If only end_year is given, this might be tricky with S2 range format, 
            # usually it's YYYY or YYYY-YYYY. For simplicity, if only end_year, we might ignore or handle differently.
            # S2 API documentation on year range is not explicit for /paper/search query parameter directly
            # but usually is for `year` field filtering in other contexts. Let's try with `year` in query for now.
            # Update: `year` in query doesn't work. The `publicationDate` can be used with range queries if S2 supports it, 
            # or filter post-retrieval. For now, let's rely on `year` field in the request payload if it's available for this endpoint,
            # or filter after fetching. Given the API docs, it seems best to filter post-retrieval for year range on search.
            # For /paper/search, it seems filtering by year is not a direct query parameter.
            # We will have to filter results *after* fetching if precise year range is needed beyond `year` field in results.
            # The `year` field in `fields` gives us the publication year for filtering.
            pass # Year filtering will be done post-retrieval for now.

        self.logger.info(f"Searching Semantic Scholar for: '{query}' with limit {max_results}")
        self.logger.debug(f"Request URL: {search_url}, Params: {params}")

        items: List[LiteratureItem] = []
        try:
            timeout_config = httpx.Timeout(self.config.pdf_processing_timeout if self.config else 30.0, read=60.0)
            async with httpx.AsyncClient(timeout=timeout_config) as client:
                response = await client.get(search_url, params=params, headers=headers)
                response.raise_for_status() # Raise an exception for bad status codes
                
                results_data = response.json()
                self.logger.debug(f"Semantic Scholar raw response: {results_data}")

                # S2 search results can be under 'data' or sometimes directly a list if total < limit
                papers_list = results_data.get("data", [])
                if not papers_list and isinstance(results_data, list): # If results_data itself is the list
                     papers_list = results_data
                elif not papers_list and 'paperId' in results_data: # Single result if total is 1
                    papers_list = [results_data]
                
                if not papers_list and results_data.get('total', 0) > 0:
                    self.logger.warning(f"Semantic Scholar returned total > 0 but no 'data' list. Response: {results_data}")

                self.logger.info(f"Received {len(papers_list)} raw results from Semantic Scholar. Total reported: {results_data.get('total', 0)}")

                for paper_data in papers_list:
                    if paper_data: # Ensure paper_data is not None
                        # Post-retrieval year filtering
                        s2_year = paper_data.get("year")
                        if s2_year and year_start and s2_year < year_start:
                            continue
                        if s2_year and year_end and s2_year > year_end:
                            continue
                        items.append(self._to_literature_item(paper_data))
                
                self.logger.info(f"Processed {len(items)} items from Semantic Scholar after filtering.")

        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error from Semantic Scholar API: {e.response.status_code} - {e.response.text}", exc_info=True)
            raise SemanticScholarError(f"Semantic Scholar API request failed: {e.response.status_code}") from e
        except httpx.RequestError as e:
            self.logger.error(f"Request error connecting to Semantic Scholar API: {e}", exc_info=True)
            raise SemanticScholarError(f"Could not connect to Semantic Scholar API: {e}") from e
        except Exception as e:
            self.logger.error(f"Unexpected error during Semantic Scholar search: {e}", exc_info=True)
            raise SemanticScholarError(f"An unexpected error occurred: {e}") from e
        
        return items

    async def get_by_id(self, item_id: str) -> Optional[LiteratureItem]:
        """
        Retrieve a specific paper by its Semantic Scholar ID (S2ID, DOI, ArXiv ID).
        The item_id should be prefixed e.g. "DOI:XXXX", "ARXIV:YYYY", "CorpusId:ZZZZ"
        If just an S2ID (numeric string) is passed, it assumes CorpusId.
        """
        if not item_id.strip():
            raise ValueError("Item ID cannot be empty.")

        # S2 Paper Details endpoint uses paper_id which can be S2PaperId, DOI, ArXivId, etc.
        # Ensure it's correctly formatted. If it's just a number, it's likely CorpusID.
        # If it contains 's2:', we strip it as S2 API doesn't use that for lookup.
        s2_lookup_id = item_id.replace("s2:", "")
        if s2_lookup_id.isdigit() and not any(s2_lookup_id.startswith(p) for p in ["DOI:","ARXIV:", "CorpusId:"]):
             s2_lookup_id = f"CorpusId:{s2_lookup_id}"
        elif "doi:" in s2_lookup_id.lower():
            s2_lookup_id = s2_lookup_id.upper().replace("DOI:", "DOI:") # Ensure DOI prefix is correct case for S2
        elif "arxiv:" in s2_lookup_id.lower():
             s2_lookup_id = s2_lookup_id.upper().replace("ARXIV:", "ARXIV:")

        details_url = f"{self.api_url}/paper/{s2_lookup_id}"
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        
        params = {"fields": ",".join(self.DEFAULT_PAPER_FIELDS)}
        self.logger.info(f"Fetching paper details from Semantic Scholar for ID: {s2_lookup_id}")

        try:
            timeout_config = httpx.Timeout(self.config.pdf_processing_timeout if self.config else 30.0, read=60.0)
            async with httpx.AsyncClient(timeout=timeout_config) as client:
                response = await client.get(details_url, params=params, headers=headers)
                response.raise_for_status()
                paper_data = response.json()
                if paper_data and paper_data.get("paperId"): # Check if valid paper data returned
                    return self._to_literature_item(paper_data)
                elif paper_data.get("error"): # S2 sometimes returns 200 OK with an error message
                    self.logger.error(f"Semantic Scholar API returned an error for ID {s2_lookup_id}: {paper_data['error']}")
                    return None
                else: # No paperId and no explicit error, but not valid data
                    self.logger.warning(f"No valid paper data found for ID {s2_lookup_id} from Semantic Scholar. Response: {paper_data}")
                    return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                self.logger.info(f"Paper with ID {s2_lookup_id} not found on Semantic Scholar.")
                return None
            self.logger.error(f"HTTP error fetching details from S2 API: {e.response.status_code} - {e.response.text}", exc_info=True)
            raise SemanticScholarError(f"S2 API request failed for paper details: {e.response.status_code}") from e
        except Exception as e:
            self.logger.error(f"Unexpected error fetching paper details from S2: {e}", exc_info=True)
            raise SemanticScholarError(f"An unexpected error occurred while fetching paper details: {e}") from e

# Example Usage (for testing)
async def main_s2_test():
    print("Testing SemanticScholarClient...")
    # This test requires network access and Semantic Scholar API to be available.
    # For a more robust test, you might mock httpx.AsyncClient responses.
    
    # If you have a config.env with SEMANTIC_SCHOLAR_API_KEY, it will be used
    test_config = Config()
    s2_client = SemanticScholarClient(config=test_config) 

    query = "artificial intelligence in education"
    print(f"\nSearching for '{query}' (max 5 papers, years 2020-2022)...")
    try:
        papers = await s2_client.search_papers(query, max_results=5, year_start=2020, year_end=2022)
        if papers:
            print(f"Found {len(papers)} papers:")
            for i, paper in enumerate(papers):
                print(f"  {i+1}. Title: {paper.title}")
                print(f"     Authors: {paper.author_string}")
                print(f"     Year: {paper.year}")
                print(f"     Source: {paper.source}")
                print(f"     Abstract snippet: {paper.abstract[:100] if paper.abstract else 'N/A'}...")
                print(f"     Keywords: {paper.keywords[:5]}")
                print(f"     ID: {paper.id}")
        else:
            print("No papers found for the query.")
    except SemanticScholarError as e:
        print(f"Error during search: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during search test: {e}")

    print("\n--- Testing Get by ID --- (Example with a known S2 Paper ID)")
    # Replace with a real S2 Paper ID for testing (e.g., from a previous search)
    # Or a DOI like "10.1038/s41586-021-03430-5"
    test_paper_id = "649def34f8be52c8b66281af98ae884c09aef38b" # Example S2 CorpusId
    test_doi = "DOI:10.18653/v1/2020.acl-main.196"
    print(f"Fetching paper by S2 CorpusId: {test_paper_id}")
    try:
        paper_by_id = await s2_client.get_by_id(test_paper_id)
        if paper_by_id:
            print(f"Found paper by ID: {paper_by_id.title}")
            print(f"  Authors: {paper_by_id.author_string}")
            print(f"  DOI: {paper_by_id.doi}")
        else:
            print(f"Paper with ID {test_paper_id} not found.")
            
        print(f"\nFetching paper by DOI: {test_doi}")
        paper_by_doi = await s2_client.get_by_id(test_doi)
        if paper_by_doi:
            print(f"Found paper by DOI: {paper_by_doi.title}")
            print(f"  Authors: {paper_by_doi.author_string}")
            print(f"  S2 ID: {paper_by_doi.id}")
        else:
            print(f"Paper with DOI {test_doi} not found.")

    except SemanticScholarError as e:
        print(f"Error during get_by_id: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during get_by_id test: {e}")

if __name__ == "__main__":
    # To run this test directly:
    # Ensure you are in the project root and run: python -m src.lit_review_agent.retrieval.semantic_scholar_client
    asyncio.run(main_s2_test()) 