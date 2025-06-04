"""Text chunking strategies for processing long documents."""

import re
from typing import List, Optional

from ..utils.logger import LoggerMixin


class ChunkingStrategy(LoggerMixin):
    """Base class for text chunking strategies."""

    def __init__(
        self, chunk_size: int = 1000, overlap: int = 200, separator: str = "\n\n"
    ):
        """
        Initialize the chunking strategy.

        Args:
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks
            separator: Preferred separator for splitting
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separator = separator
        self.logger.info(
            f"Initialized chunking strategy: size={chunk_size}, overlap={overlap}"
        )

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        if not text or len(text) <= self.chunk_size:
            return [text] if text else []

        chunks = []
        start = 0

        while start < len(text):
            # Determine end position
            end = start + self.chunk_size

            if end >= len(text):
                # Last chunk
                chunks.append(text[start:])
                break

            # Try to find a good break point
            chunk_end = self._find_break_point(text, start, end)
            chunks.append(text[start:chunk_end].strip())

            # Move start position with overlap
            start = max(start + 1, chunk_end - self.overlap)

        # Filter out empty chunks
        return [chunk for chunk in chunks if chunk.strip()]

    def _find_break_point(self, text: str, start: int, end: int) -> int:
        """
        Find the best break point for chunking.

        Args:
            text: Full text
            start: Start position of current chunk
            end: Proposed end position

        Returns:
            Actual end position
        """
        chunk_text = text[start:end]

        # Try to find separator within the last part of the chunk
        sep_pos = chunk_text.rfind(self.separator)
        if (
            sep_pos > self.chunk_size // 2
        ):  # Only use if separator is in the latter half
            return start + sep_pos + len(self.separator)

        # Look for sentence endings
        for punct in [". ", "! ", "? "]:
            punct_pos = chunk_text.rfind(punct)
            if punct_pos > self.chunk_size // 2:
                return start + punct_pos + len(punct)

        # Look for word boundaries
        space_pos = chunk_text.rfind(" ")
        if space_pos > self.chunk_size // 2:
            return start + space_pos + 1

        # If no good break point found, use the proposed end
        return end


class SemanticChunkingStrategy(ChunkingStrategy):
    """Semantic chunking strategy that preserves meaning."""

    def __init__(
        self, chunk_size: int = 1000, overlap: int = 200, min_chunk_size: int = 100
    ):
        """
        Initialize semantic chunking strategy.

        Args:
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks
            min_chunk_size: Minimum size of a chunk
        """
        super().__init__(chunk_size, overlap, "\n\n")
        self.min_chunk_size = min_chunk_size

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into semantic chunks.

        Args:
            text: Text to chunk

        Returns:
            List of semantic chunks
        """
        if not text:
            return []

        # First, try to split by paragraphs
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > self.chunk_size:
                if current_chunk and len(current_chunk) >= self.min_chunk_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    # If current chunk is too small, merge with paragraph
                    current_chunk += "\n\n" + paragraph if current_chunk else paragraph

                    # If still too large, use sentence-based splitting
                    if len(current_chunk) > self.chunk_size:
                        sentence_chunks = self._split_by_sentences(current_chunk)
                        chunks.extend(sentence_chunks[:-1])
                        current_chunk = sentence_chunks[-1] if sentence_chunks else ""
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph

        # Add the last chunk
        if current_chunk and len(current_chunk) >= self.min_chunk_size:
            chunks.append(current_chunk.strip())

        return chunks

    def _split_by_sentences(self, text: str) -> List[str]:
        """
        Split text by sentences when paragraph splitting is not sufficient.

        Args:
            text: Text to split

        Returns:
            List of sentence-based chunks
        """
        # Simple sentence splitting using regex
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    # If single sentence is too large, use character-based splitting
                    char_chunks = super().chunk_text(sentence)
                    chunks.extend(char_chunks)
                    current_chunk = ""
            else:
                current_chunk += " " + sentence if current_chunk else sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks


class FixedSizeChunkingStrategy(ChunkingStrategy):
    """Fixed-size chunking strategy with strict size limits."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize fixed-size chunking strategy.

        Args:
            chunk_size: Exact size of each chunk
            overlap: Number of characters to overlap between chunks
        """
        super().__init__(chunk_size, overlap, " ")

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into fixed-size chunks.

        Args:
            text: Text to chunk

        Returns:
            List of fixed-size chunks
        """
        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            # Try to end at word boundary if possible
            if end < len(text):
                # Find last space within chunk
                space_pos = text[:end].rfind(" ", start)
                if space_pos > start:
                    end = space_pos

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = max(start + 1, end - self.overlap)

        return chunks


class TokenBasedChunkingStrategy(ChunkingStrategy):
    """Token-based chunking strategy that estimates token counts."""

    def __init__(
        self,
        max_tokens: int = 250,
        overlap_tokens: int = 50,
        chars_per_token: float = 4.0,
    ):
        """
        Initialize token-based chunking strategy.

        Args:
            max_tokens: Maximum tokens per chunk
            overlap_tokens: Number of tokens to overlap
            chars_per_token: Estimated characters per token
        """
        chunk_size = int(max_tokens * chars_per_token)
        overlap = int(overlap_tokens * chars_per_token)
        super().__init__(chunk_size, overlap, "\n\n")

        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.chars_per_token = chars_per_token

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in text.

        Args:
            text: Input text

        Returns:
            Estimated token count
        """
        return int(len(text) / self.chars_per_token)

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into token-based chunks.

        Args:
            text: Text to chunk

        Returns:
            List of chunks within token limits
        """
        if not text:
            return []

        estimated_tokens = self.estimate_tokens(text)
        if estimated_tokens <= self.max_tokens:
            return [text]

        # Use base chunking strategy with token-adjusted sizes
        chunks = super().chunk_text(text)

        # Verify and adjust chunks that might exceed token limits
        adjusted_chunks = []
        for chunk in chunks:
            if self.estimate_tokens(chunk) > self.max_tokens:
                # Further split large chunks
                sub_chunks = self._split_large_chunk(chunk)
                adjusted_chunks.extend(sub_chunks)
            else:
                adjusted_chunks.append(chunk)

        return adjusted_chunks

    def _split_large_chunk(self, chunk: str) -> List[str]:
        """
        Split a chunk that exceeds token limits.

        Args:
            chunk: Chunk to split

        Returns:
            List of smaller chunks
        """
        # Use a smaller chunk size for splitting
        smaller_strategy = FixedSizeChunkingStrategy(
            chunk_size=int(self.max_tokens * self.chars_per_token * 0.8),
            overlap=int(self.overlap_tokens * self.chars_per_token),
        )
        return smaller_strategy.chunk_text(chunk)
