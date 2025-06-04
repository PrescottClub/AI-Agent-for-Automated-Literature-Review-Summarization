"""Embeddings manager for generating and managing text embeddings."""

from typing import Dict, List, Optional, Union

import numpy as np
from sentence_transformers import SentenceTransformer

from ..utils.logger import LoggerMixin


class EmbeddingsManager(LoggerMixin):
    """Manager for text embeddings generation and operations."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embeddings manager.

        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the sentence transformer model."""
        try:
            self.model = SentenceTransformer(self.model_name)
            self.logger.info(f"Loaded embeddings model: {self.model_name}")
        except Exception as e:
            self.logger.error(f"Failed to load embeddings model: {e}")
            self.model = None

    def generate_embedding(self, text: str) -> Optional[np.ndarray]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text

        Returns:
            Embedding vector or None if failed
        """
        if not self.model or not text:
            return None

        try:
            embedding = self.model.encode(text)
            return embedding
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            return None

    def generate_embeddings(self, texts: List[str]) -> List[Optional[np.ndarray]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        if not self.model or not texts:
            return []

        try:
            embeddings = self.model.encode(texts)
            return [emb for emb in embeddings]
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            return [None] * len(texts)

    def calculate_similarity(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score between -1 and 1
        """
        try:
            # Normalize vectors
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            # Calculate cosine similarity
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            return float(similarity)

        except Exception as e:
            self.logger.error(f"Error calculating similarity: {e}")
            return 0.0

    def find_most_similar(
        self,
        query_embedding: np.ndarray,
        candidate_embeddings: List[np.ndarray],
        top_k: int = 5,
    ) -> List[tuple]:
        """
        Find most similar embeddings to a query embedding.

        Args:
            query_embedding: Query embedding vector
            candidate_embeddings: List of candidate embeddings
            top_k: Number of top results to return

        Returns:
            List of (index, similarity_score) tuples
        """
        if not candidate_embeddings:
            return []

        similarities = []
        for i, candidate in enumerate(candidate_embeddings):
            if candidate is not None:
                similarity = self.calculate_similarity(query_embedding, candidate)
                similarities.append((i, similarity))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the loaded model.

        Returns:
            Dictionary with model information
        """
        if not self.model:
            return {"error": "No model loaded"}

        return {
            "model_name": self.model_name,
            "max_seq_length": str(getattr(self.model, "max_seq_length", "Unknown")),
            "embedding_dimension": (
                str(len(self.model.encode("test"))) if self.model else "Unknown"
            ),
        }
