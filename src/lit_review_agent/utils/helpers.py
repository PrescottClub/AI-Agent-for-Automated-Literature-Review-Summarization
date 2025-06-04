"""Helper utilities for the literature review agent."""

import re
import unicodedata
from pathlib import Path
from typing import List, Optional, Set

import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Global model cache to avoid reloading models repeatedly
_SPACY_MODEL_CACHE = {}
_STOPWORDS_CACHE = {}


def _get_spacy_model(model_name: str = "en_core_web_sm"):
    """Get cached spaCy model or load it if not cached."""
    if model_name not in _SPACY_MODEL_CACHE:
        try:
            _SPACY_MODEL_CACHE[model_name] = spacy.load(model_name)
        except OSError:
            # Model not found, return None
            _SPACY_MODEL_CACHE[model_name] = None
    return _SPACY_MODEL_CACHE[model_name]


def _get_stopwords(language: str = "english"):
    """Get cached stopwords or load them if not cached."""
    if language not in _STOPWORDS_CACHE:
        try:
            _STOPWORDS_CACHE[language] = set(stopwords.words(language))
        except Exception:
            _STOPWORDS_CACHE[language] = set()
    return _STOPWORDS_CACHE[language]


def clean_text(text: str, remove_special_chars: bool = True) -> str:
    """
    Clean and normalize text for processing.

    Args:
        text: Input text to clean
        remove_special_chars: Whether to remove special characters

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)

    # Remove extra whitespace and newlines
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    # Remove special characters if requested
    if remove_special_chars:
        # Keep alphanumeric, spaces, and basic punctuation
        text = re.sub(r"[^\w\s\.\,\;\:\!\?\-\(\)]", "", text)

    return text


def extract_keywords(
    text: str,
    max_keywords: int = 10,
    min_length: int = 3,
    custom_stopwords: Optional[Set[str]] = None,
) -> List[str]:
    """
    Extract keywords from text using NLP techniques.

    Args:
        text: Input text
        max_keywords: Maximum number of keywords to return
        min_length: Minimum length of keywords
        custom_stopwords: Additional stopwords to filter out

    Returns:
        List of extracted keywords
    """
    if not text:
        return []

    try:
        # Get cached spaCy model
        nlp = _get_spacy_model("en_core_web_sm")
        if nlp is None:
            raise OSError("spaCy model not available")

        doc = nlp(text.lower())

        # Get cached stopwords
        stop_words = _get_stopwords("english")
        if custom_stopwords:
            stop_words.update(custom_stopwords)

        # Extract keywords based on POS tags and named entities
        keywords = []

        # Add named entities
        for ent in doc.ents:
            if (
                ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT", "EVENT"]
                and len(ent.text) >= min_length
                and ent.text.lower() not in stop_words
            ):
                keywords.append(ent.text.lower())

        # Add important nouns and adjectives
        for token in doc:
            if (
                token.pos_ in ["NOUN", "PROPN", "ADJ"]
                and not token.is_stop
                and not token.is_punct
                and len(token.text) >= min_length
                and token.text.lower() not in stop_words
            ):
                keywords.append(token.lemma_.lower())

        # Remove duplicates and limit results
        # Preserve order while removing duplicates
        keywords = list(dict.fromkeys(keywords))
        return keywords[:max_keywords]

    except OSError:
        # Fallback to simple tokenization if spaCy model is not available
        tokens = word_tokenize(text.lower())
        stop_words = _get_stopwords("english")
        if custom_stopwords:
            stop_words.update(custom_stopwords)

        keywords = [
            token
            for token in tokens
            if (
                len(token) >= min_length and token.isalpha() and token not in stop_words
            )
        ]

        return list(dict.fromkeys(keywords))[:max_keywords]


def validate_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise
    """
    if not email:
        return False

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_pattern, email))


def safe_filename(filename: str, max_length: int = 200) -> str:
    """
    Convert a string to a safe filename by removing/replacing invalid characters.

    Args:
        filename: Original filename
        max_length: Maximum length of the filename

    Returns:
        Safe filename
    """
    if not filename:
        return "untitled"

    # Remove/replace invalid characters
    safe_chars = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Remove control characters
    safe_chars = re.sub(r"[\x00-\x1f\x7f]", "", safe_chars)

    # Collapse multiple underscores
    safe_chars = re.sub(r"_+", "_", safe_chars)

    # Strip leading/trailing spaces and dots
    safe_chars = safe_chars.strip(" .")

    # Ensure it's not empty
    if not safe_chars:
        safe_chars = "untitled"

    # Truncate if too long
    if len(safe_chars) > max_length:
        safe_chars = safe_chars[:max_length].rstrip("_")

    return safe_chars


def chunk_text(
    text: str, chunk_size: int = 1000, overlap: int = 200, separator: str = "\n\n"
) -> List[str]:
    """
    Split text into overlapping chunks for processing.

    Args:
        text: Text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
        separator: Preferred split separator

    Returns:
        List of text chunks
    """
    if not text or len(text) <= chunk_size:
        return [text] if text else []

    chunks = []
    start = 0

    while start < len(text):
        # Determine end position
        end = start + chunk_size

        if end >= len(text):
            # Last chunk
            chunks.append(text[start:])
            break

        # Try to find a good break point
        chunk_end = end

        # Look for separator within the last part of the chunk
        sep_pos = text[start:end].rfind(separator)
        if sep_pos > chunk_size // 2:  # Only use if separator is in the latter half
            chunk_end = start + sep_pos + len(separator)
        else:
            # Look for sentence endings
            for punct in [". ", "! ", "? "]:
                punct_pos = text[start:end].rfind(punct)
                if punct_pos > chunk_size // 2:
                    chunk_end = start + punct_pos + len(punct)
                    break
            else:
                # Look for word boundaries
                space_pos = text[start:end].rfind(" ")
                if space_pos > chunk_size // 2:
                    chunk_end = start + space_pos + 1

        chunks.append(text[start:chunk_end].strip())

        # Move start position with overlap
        start = max(start + 1, chunk_end - overlap)

    return [chunk for chunk in chunks if chunk.strip()]


def estimate_tokens(text: str, chars_per_token: float = 4.0) -> int:
    """
    Estimate the number of tokens in a text.

    This is a simple estimation. For more accurate token counting,
    use the actual tokenizer of the target LLM model.

    Args:
        text: Input text
        chars_per_token: Average characters per token

    Returns:
        Estimated token count
    """
    if not text:
        return 0

    # Simple word-based estimation that's usually more accurate than pure character count
    word_count = len(text.split())
    char_estimate = int(len(text) / chars_per_token)

    # Use the average of word count and character-based estimate
    # This tends to be more accurate for most texts
    return int((word_count + char_estimate) / 2)


def truncate_text(text: str, max_tokens: int, chars_per_token: float = 4.0) -> str:
    """
    Truncate text to fit within token limit.

    Args:
        text: Input text
        max_tokens: Maximum allowed tokens
        chars_per_token: Average characters per token

    Returns:
        Truncated text
    """
    if not text:
        return ""

    max_chars = int(max_tokens * chars_per_token)

    if len(text) <= max_chars:
        return text

    # Truncate and try to end at a sentence boundary
    truncated = text[:max_chars]

    # Find the last sentence ending
    for punct in [". ", "! ", "? "]:
        last_punct = truncated.rfind(punct)
        if last_punct > max_chars * 0.8:  # Only if we don't lose too much text
            return truncated[: last_punct + 1].strip()

    # If no good sentence boundary, truncate at word boundary
    last_space = truncated.rfind(" ")
    if last_space > max_chars * 0.8:
        return truncated[:last_space].strip()

    return truncated.strip()
