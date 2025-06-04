"""Text processor for cleaning, preprocessing and analyzing literature text."""

import re
from typing import Dict, List, Optional, Set, Tuple

import spacy
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer

from ..utils.logger import LoggerMixin
from ..utils.helpers import clean_text, extract_keywords


class TextProcessor(LoggerMixin):
    """Advanced text processor for literature analysis."""

    def __init__(
        self,
        spacy_model: str = "en_core_web_sm",
        sentence_model: str = "all-MiniLM-L6-v2",
    ):
        """
        Initialize the text processor.

        Args:
            spacy_model: SpaCy model name for NLP processing
            sentence_model: Sentence transformer model for embeddings
        """
        self.spacy_model_name = spacy_model
        self.sentence_model_name = sentence_model

        # Load models
        try:
            self.nlp = spacy.load(spacy_model)
            self.logger.info(f"Loaded spaCy model: {spacy_model}")
        except OSError:
            self.logger.warning(
                f"Could not load spaCy model {spacy_model}, using basic processing"
            )
            self.nlp = None

        try:
            self.sentence_model = SentenceTransformer(sentence_model)
            self.logger.info(f"Loaded sentence transformer: {sentence_model}")
        except Exception as e:
            self.logger.warning(f"Could not load sentence transformer: {e}")
            self.sentence_model = None

        # Initialize stopwords
        try:
            self.stop_words = set(stopwords.words("english"))
        except Exception:
            self.stop_words = set()

        self.logger.info("Initialized TextProcessor")

    def preprocess_text(self, text: str, preserve_structure: bool = False) -> str:
        """
        Preprocess text for analysis.

        Args:
            text: Input text
            preserve_structure: Whether to preserve paragraph structure

        Returns:
            Preprocessed text
        """
        if not text:
            return ""

        # Basic cleaning
        processed = clean_text(text, remove_special_chars=False)

        # Remove citations (e.g., [1], [Smith et al., 2020])
        processed = re.sub(r"\[[\d\w\s,\.]+\]", "", processed)

        # Remove URLs
        processed = re.sub(r"http[s]?://\S+", "", processed)

        # Remove email addresses
        processed = re.sub(r"\S+@\S+", "", processed)

        # Normalize whitespace
        if preserve_structure:
            # Keep paragraph breaks
            processed = re.sub(r"\n\s*\n", "\n\n", processed)
            processed = re.sub(r"[ \t]+", " ", processed)
        else:
            processed = re.sub(r"\s+", " ", processed)

        return processed.strip()

    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract standard academic paper sections from text.

        Args:
            text: Full paper text

        Returns:
            Dictionary with section names as keys and content as values
        """
        sections = {}

        # Common section headers
        section_patterns = {
            "abstract": r"(?i)abstract\s*:?\s*(.*?)(?=\n\s*(?:introduction|keywords|1\.|background))",
            "introduction": r"(?i)(?:1\.\s*)?introduction\s*:?\s*(.*?)(?=\n\s*(?:2\.|related work|methodology|background))",
            "methodology": r"(?i)(?:2\.\s*)?(?:methodology|methods|approach)\s*:?\s*(.*?)(?=\n\s*(?:3\.|results|experiments|evaluation))",
            "results": r"(?i)(?:3\.\s*)?(?:results|experiments|evaluation)\s*:?\s*(.*?)(?=\n\s*(?:4\.|discussion|conclusion|limitations))",
            "conclusion": r"(?i)(?:4\.\s*)?(?:conclusion|conclusions|summary)\s*:?\s*(.*?)(?=\n\s*(?:references|acknowledgments|appendix|$))",
        }

        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                section_content = match.group(1).strip()
                if section_content:
                    sections[section_name] = self.preprocess_text(section_content)

        # If no sections found, treat entire text as content
        if not sections:
            sections["full_text"] = self.preprocess_text(text)

        return sections

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text.

        Args:
            text: Input text

        Returns:
            Dictionary with entity types as keys and entity lists as values
        """
        entities = {
            "persons": [],
            "organizations": [],
            "locations": [],
            "technologies": [],
            "concepts": [],
        }

        if not self.nlp or not text:
            return entities

        try:
            doc = self.nlp(text)

            for ent in doc.ents:
                entity_text = ent.text.strip()
                if len(entity_text) < 2:
                    continue

                if ent.label_ in ["PERSON"]:
                    entities["persons"].append(entity_text)
                elif ent.label_ in ["ORG", "CORP"]:
                    entities["organizations"].append(entity_text)
                elif ent.label_ in ["GPE", "LOC"]:
                    entities["locations"].append(entity_text)
                elif ent.label_ in ["PRODUCT", "WORK_OF_ART"]:
                    entities["technologies"].append(entity_text)
                elif ent.label_ in ["EVENT", "LAW", "LANGUAGE"]:
                    entities["concepts"].append(entity_text)

            # Remove duplicates while preserving order
            for key in entities:
                entities[key] = list(dict.fromkeys(entities[key]))

        except Exception as e:
            self.logger.error(f"Error extracting entities: {e}")

        return entities

    def extract_research_keywords(self, text: str, max_keywords: int = 20) -> List[str]:
        """
        Extract research-specific keywords from text.

        Args:
            text: Input text
            max_keywords: Maximum number of keywords to return

        Returns:
            List of research keywords
        """
        # Get basic keywords
        basic_keywords = extract_keywords(text, max_keywords=max_keywords * 2)

        # Research-specific filtering
        research_keywords = []

        # Academic terms that indicate research concepts
        research_indicators = {
            "algorithm",
            "model",
            "method",
            "approach",
            "framework",
            "system",
            "analysis",
            "evaluation",
            "experiment",
            "study",
            "research",
            "technique",
            "strategy",
            "mechanism",
            "process",
            "procedure",
            "optimization",
            "performance",
            "accuracy",
            "efficiency",
            "neural",
            "machine",
            "learning",
            "deep",
            "artificial",
            "intelligence",
        }

        for keyword in basic_keywords:
            # Prefer multi-word terms
            if len(keyword.split()) > 1:
                research_keywords.append(keyword)
            # Include single words that are research-related
            elif any(indicator in keyword.lower() for indicator in research_indicators):
                research_keywords.append(keyword)
            # Include technical terms (often have specific patterns)
            elif re.match(r"^[a-z]+[A-Z][a-z]*", keyword):  # camelCase
                research_keywords.append(keyword)
            elif "-" in keyword or "_" in keyword:  # hyphenated or underscored
                research_keywords.append(keyword)

        return research_keywords[:max_keywords]

    def get_text_statistics(self, text: str) -> Dict[str, int]:
        """
        Get basic statistics about the text.

        Args:
            text: Input text

        Returns:
            Dictionary with text statistics
        """
        if not text:
            return {}

        # Basic counts
        char_count = len(text)
        word_count = len(word_tokenize(text))

        try:
            sentence_count = len(sent_tokenize(text))
        except:
            sentence_count = len([s for s in text.split(".") if s.strip()])

        paragraph_count = len([p for p in text.split("\n\n") if p.strip()])

        return {
            "characters": char_count,
            "words": word_count,
            "sentences": sentence_count,
            "paragraphs": paragraph_count,
            "avg_words_per_sentence": word_count / max(sentence_count, 1),
            "avg_chars_per_word": char_count / max(word_count, 1),
        }

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score between 0 and 1
        """
        if not self.sentence_model or not text1 or not text2:
            return 0.0

        try:
            # Get embeddings
            embeddings = self.sentence_model.encode([text1, text2])

            # Calculate cosine similarity
            from numpy import dot
            from numpy.linalg import norm

            similarity = dot(embeddings[0], embeddings[1]) / (
                norm(embeddings[0]) * norm(embeddings[1])
            )

            return float(similarity)

        except Exception as e:
            self.logger.error(f"Error calculating similarity: {e}")
            return 0.0

    def identify_research_gaps(self, texts: List[str]) -> List[str]:
        """
        Identify potential research gaps by analyzing multiple texts.

        Args:
            texts: List of research paper texts

        Returns:
            List of identified research gaps
        """
        # This is a simplified implementation
        # In practice, this would use more sophisticated NLP techniques

        gaps = []

        # Look for limitation statements
        limitation_patterns = [
            r"(?i)limitation[s]?\s*:?\s*([^.]+)",
            r"(?i)future work\s*:?\s*([^.]+)",
            r"(?i)however[,]?\s*([^.]+)",
            r"(?i)although\s*([^.]+)",
            r"(?i)despite\s*([^.]+)",
        ]

        for text in texts:
            for pattern in limitation_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if len(match.strip()) > 20:  # Only meaningful statements
                        gaps.append(match.strip())

        # Remove duplicates and return top gaps
        unique_gaps = list(dict.fromkeys(gaps))
        return unique_gaps[:10]
