"""Vector store for managing literature embeddings and similarity search."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from ..utils.logger import LoggerMixin
from ..utils.cache_manager import get_cache_manager, cache_embeddings
from ..utils.performance_monitor import monitor_performance, get_performance_monitor
from ..retrieval.base_retriever import LiteratureItem


class VectorStore(LoggerMixin):
    """Vector store for literature embeddings using ChromaDB."""

    def __init__(self,
                 persist_directory: str = "./data/chroma_db",
                 collection_name: str = "literature_collection",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector store.

        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
            embedding_model: Sentence transformer model for embeddings
        """
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model

        # Create directory if it doesn't exist
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        try:
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            self.logger.info(
                f"Initialized ChromaDB client at {persist_directory}")
        except Exception as e:
            self.logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

        # Get or create collection
        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Literature review embeddings"}
            )
            self.logger.info(f"Using collection: {collection_name}")
        except Exception as e:
            self.logger.error(f"Failed to create collection: {e}")
            raise

        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer(embedding_model)
            self.logger.info(f"Loaded embedding model: {embedding_model}")
        except (OSError, ImportError, ValueError) as e:
            self.logger.error(f"Failed to load embedding model: {e}")
            self.embedding_model = None
        except Exception as e:
            self.logger.error(f"Unexpected error loading embedding model: {e}")
            self.embedding_model = None

    @monitor_performance
    def add_literature_item(self, item: LiteratureItem) -> bool:
        """
        Add a literature item to the vector store.

        Args:
            item: Literature item to add

        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare text for embedding
            text_content = self._prepare_text_for_embedding(item)

            if not text_content or not self.embedding_model:
                self.logger.warning(
                    f"Cannot create embedding for item {item.id}")
                return False

            # Generate embedding
            embedding = self.embedding_model.encode(text_content).tolist()

            # Prepare metadata
            metadata = self._prepare_metadata(item)

            # Add to collection
            self.collection.add(
                ids=[item.id],
                embeddings=[embedding],
                documents=[text_content],
                metadatas=[metadata]
            )

            self.logger.info(
                f"Added literature item to vector store: {item.id}")
            return True

        except (ValueError, TypeError) as e:
            self.logger.error(
                f"Invalid data for item {item.id}: {e}")
            return False
        except Exception as e:
            self.logger.error(
                f"Unexpected error adding item {item.id} to vector store: {e}")
            return False

    def add_literature_items(self, items: List[LiteratureItem]) -> int:
        """
        Add multiple literature items to the vector store.

        Args:
            items: List of literature items to add

        Returns:
            Number of items successfully added
        """
        if not items:
            return 0

        successful_additions = 0
        batch_size = 100  # Process in batches

        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_ids = []
            batch_embeddings = []
            batch_documents = []
            batch_metadatas = []

            for item in batch:
                try:
                    # Prepare text for embedding
                    text_content = self._prepare_text_for_embedding(item)

                    if not text_content or not self.embedding_model:
                        continue

                    # Generate embedding
                    embedding = self.embedding_model.encode(
                        text_content).tolist()

                    # Prepare metadata
                    metadata = self._prepare_metadata(item)

                    batch_ids.append(item.id)
                    batch_embeddings.append(embedding)
                    batch_documents.append(text_content)
                    batch_metadatas.append(metadata)

                except Exception as e:
                    self.logger.error(f"Error preparing item {item.id}: {e}")
                    continue

            # Add batch to collection
            if batch_ids:
                try:
                    self.collection.add(
                        ids=batch_ids,
                        embeddings=batch_embeddings,
                        documents=batch_documents,
                        metadatas=batch_metadatas
                    )
                    successful_additions += len(batch_ids)
                    self.logger.info(
                        f"Added batch of {len(batch_ids)} items to vector store")
                except Exception as e:
                    self.logger.error(
                        f"Error adding batch to vector store: {e}")

        self.logger.info(
            f"Successfully added {successful_additions}/{len(items)} items")
        return successful_additions

    @monitor_performance
    def search_similar(self,
                       query: str,
                       n_results: int = 10,
                       where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar literature items.

        Args:
            query: Search query
            n_results: Number of results to return
            where: Optional metadata filters

        Returns:
            List of search results with metadata
        """
        try:
            if not self.embedding_model:
                self.logger.error("No embedding model available for search")
                return []

            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()

            # Search collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where
            )

            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                result = {
                    'id': results['ids'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None,
                    'document': results['documents'][0][i] if results['documents'] else None,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                }
                formatted_results.append(result)

            self.logger.info(
                f"Found {len(formatted_results)} similar items for query")
            return formatted_results

        except (ValueError, TypeError) as e:
            self.logger.error(f"Invalid search parameters: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error searching vector store: {e}")
            return []

    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific item by ID.

        Args:
            item_id: Literature item ID

        Returns:
            Item data or None if not found
        """
        try:
            results = self.collection.get(ids=[item_id])

            if results['ids']:
                return {
                    'id': results['ids'][0],
                    'document': results['documents'][0] if results['documents'] else None,
                    'metadata': results['metadatas'][0] if results['metadatas'] else {}
                }
            return None

        except Exception as e:
            self.logger.error(f"Error getting item {item_id}: {e}")
            return None

    def delete_item(self, item_id: str) -> bool:
        """
        Delete an item from the vector store.

        Args:
            item_id: Literature item ID

        Returns:
            True if successful, False otherwise
        """
        try:
            self.collection.delete(ids=[item_id])
            self.logger.info(f"Deleted item from vector store: {item_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting item {item_id}: {e}")
            return False

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            return {
                'total_items': count,
                'collection_name': self.collection_name,
                'embedding_model': self.embedding_model_name
            }
        except Exception as e:
            self.logger.error(f"Error getting collection stats: {e}")
            return {}

    def reset_collection(self) -> bool:
        """
        Reset (clear) the collection.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Literature review embeddings"}
            )
            self.logger.info(f"Reset collection: {self.collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error resetting collection: {e}")
            return False

    @cache_embeddings
    def _prepare_text_for_embedding(self, item: LiteratureItem) -> str:
        """
        Prepare text content for embedding generation.

        Args:
            item: Literature item

        Returns:
            Text content for embedding
        """
        # Combine title, abstract, and keywords for embedding
        parts = []

        if item.title:
            parts.append(f"Title: {item.title}")

        if item.abstract:
            parts.append(f"Abstract: {item.abstract}")

        if item.keywords:
            parts.append(f"Keywords: {', '.join(item.keywords)}")

        if item.categories:
            parts.append(f"Categories: {', '.join(item.categories)}")

        # Include a more intelligent portion of full text if available
        if item.full_text:
            # Use a larger chunk and try to break at sentence boundaries
            max_content_chars = 2000
            if len(item.full_text) > max_content_chars:
                # Find the last sentence ending within our limit
                truncated = item.full_text[:max_content_chars]
                last_sentence_end = max(
                    truncated.rfind('.'),
                    truncated.rfind('!'),
                    truncated.rfind('?')
                )
                if last_sentence_end > max_content_chars * 0.7:  # At least 70% of content
                    truncated_text = item.full_text[:last_sentence_end + 1]
                else:
                    truncated_text = truncated
            else:
                truncated_text = item.full_text

            parts.append(f"Content: {truncated_text.strip()}")

        return " ".join(parts)

    def _prepare_metadata(self, item: LiteratureItem) -> Dict[str, Any]:
        """
        Prepare metadata for storage.

        Args:
            item: Literature item

        Returns:
            Metadata dictionary
        """
        metadata = {
            'title': item.title or "",
            'authors': json.dumps(item.authors) if item.authors else "[]",
            'source': item.source,
            'journal': item.journal or "",
            'categories': json.dumps(item.categories) if item.categories else "[]",
            'keywords': json.dumps(item.keywords) if item.keywords else "[]",
        }

        # Keep numeric metadata as numbers for better querying
        if item.year is not None:
            metadata['year'] = item.year
        if item.citation_count is not None:
            metadata['citation_count'] = item.citation_count

        # Add DOI and URLs if available
        if item.doi:
            metadata['doi'] = item.doi
        if item.url:
            metadata['url'] = item.url
        if item.arxiv_id:
            metadata['arxiv_id'] = item.arxiv_id

        # Only convert non-numeric values to strings
        processed_metadata = {}
        for k, v in metadata.items():
            if isinstance(v, (int, float)):
                processed_metadata[k] = v  # Keep numbers as numbers
            else:
                processed_metadata[k] = str(v) if v is not None else ""

        return processed_metadata
