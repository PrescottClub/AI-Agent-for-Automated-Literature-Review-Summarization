"""Trend analyzer for identifying research trends and patterns in literature."""

import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .llm_manager import LLMManager
from ..processing.text_processor import TextProcessor
from ..retrieval.base_retriever import LiteratureItem
from ..utils.logger import LoggerMixin


class TrendAnalyzer(LoggerMixin):
    """Analyzer for research trends and patterns in literature."""

    def __init__(self, llm_manager: LLMManager, text_processor: TextProcessor):
        """
        Initialize the trend analyzer.

        Args:
            llm_manager: LLM manager for generating analysis
            text_processor: Text processor for text analysis
        """
        self.llm_manager = llm_manager
        self.text_processor = text_processor
        self.logger.info("Initialized Trend Analyzer")

    async def analyze_temporal_trends(
        self, papers: List[LiteratureItem]
    ) -> Dict[str, Any]:
        """
        Analyze temporal trends in the literature.

        Args:
            papers: List of literature items

        Returns:
            Dictionary with temporal trend analysis
        """
        if not papers:
            return {}

        # Extract publication years
        yearly_data = {}
        for paper in papers:
            if paper.publication_date:
                year = paper.publication_date.year
                if year not in yearly_data:
                    yearly_data[year] = {
                        "count": 0,
                        "papers": [],
                        "keywords": [],
                        "categories": [],
                    }

                yearly_data[year]["count"] += 1
                yearly_data[year]["papers"].append(paper)
                yearly_data[year]["keywords"].extend(paper.keywords or [])
                yearly_data[year]["categories"].extend(paper.categories or [])

        # Analyze trends over time
        trend_analysis = {
            "publication_growth": self._analyze_publication_growth(yearly_data),
            "emerging_keywords": self._analyze_emerging_keywords(yearly_data),
            "evolving_categories": self._analyze_evolving_categories(yearly_data),
            "yearly_summary": {
                year: data["count"] for year, data in yearly_data.items()
            },
        }

        # Generate AI-powered temporal analysis
        if len(yearly_data) > 1:
            texts = []
            for year, data in sorted(yearly_data.items()):
                year_text = f"Year {year}: {data['count']} papers. "
                if data["keywords"]:
                    top_keywords = Counter(data["keywords"]).most_common(5)
                    year_text += (
                        f"Top keywords: {', '.join([kw for kw, _ in top_keywords])}. "
                    )
                texts.append(year_text)

            ai_analysis = await self._generate_temporal_analysis(texts)
            if ai_analysis:
                trend_analysis["ai_insights"] = ai_analysis

        return trend_analysis

    async def analyze_keyword_trends(
        self, papers: List[LiteratureItem]
    ) -> Dict[str, Any]:
        """
        Analyze keyword trends and co-occurrence patterns.

        Args:
            papers: List of literature items

        Returns:
            Dictionary with keyword trend analysis
        """
        all_keywords = []
        keyword_cooccurrence = {}

        for paper in papers:
            if paper.keywords:
                paper_keywords = [kw.lower().strip() for kw in paper.keywords]
                all_keywords.extend(paper_keywords)

                # Analyze co-occurrence
                for i, kw1 in enumerate(paper_keywords):
                    for kw2 in paper_keywords[i + 1 :]:
                        pair = tuple(sorted([kw1, kw2]))
                        keyword_cooccurrence[pair] = (
                            keyword_cooccurrence.get(pair, 0) + 1
                        )

        # Analyze keyword frequency
        keyword_freq = Counter(all_keywords)

        # Find emerging vs declining keywords by year
        keyword_by_year = self._analyze_keyword_by_year(papers)

        trend_analysis = {
            "top_keywords": keyword_freq.most_common(20),
            "keyword_cooccurrence": sorted(
                keyword_cooccurrence.items(), key=lambda x: x[1], reverse=True
            )[:15],
            "temporal_keyword_trends": keyword_by_year,
            "total_unique_keywords": len(keyword_freq),
        }

        return trend_analysis

    async def analyze_collaboration_patterns(
        self, papers: List[LiteratureItem]
    ) -> Dict[str, Any]:
        """
        Analyze author collaboration patterns and institutional trends.

        Args:
            papers: List of literature items

        Returns:
            Dictionary with collaboration analysis
        """
        all_authors = []
        author_collaboration = {}
        papers_per_author = {}

        for paper in papers:
            if paper.authors:
                paper_authors = [author.strip() for author in paper.authors]
                all_authors.extend(paper_authors)

                # Track papers per author
                for author in paper_authors:
                    papers_per_author[author] = papers_per_author.get(author, 0) + 1

                # Analyze collaboration
                for i, author1 in enumerate(paper_authors):
                    for author2 in paper_authors[i + 1 :]:
                        pair = tuple(sorted([author1, author2]))
                        author_collaboration[pair] = (
                            author_collaboration.get(pair, 0) + 1
                        )

        # Analyze author productivity
        author_freq = Counter(all_authors)

        # Analyze team sizes
        team_sizes = [len(paper.authors) for paper in papers if paper.authors]
        avg_team_size = sum(team_sizes) / len(team_sizes) if team_sizes else 0

        collaboration_analysis = {
            "most_productive_authors": author_freq.most_common(15),
            "frequent_collaborations": sorted(
                author_collaboration.items(), key=lambda x: x[1], reverse=True
            )[:10],
            "average_team_size": round(avg_team_size, 2),
            "team_size_distribution": Counter(team_sizes),
            "total_unique_authors": len(author_freq),
        }

        return collaboration_analysis

    async def analyze_methodological_trends(
        self, papers: List[LiteratureItem]
    ) -> Dict[str, Any]:
        """
        Analyze methodological trends in the literature.

        Args:
            papers: List of literature items

        Returns:
            Dictionary with methodological trend analysis
        """
        # Extract text content for analysis
        texts = []
        for paper in papers:
            if paper.abstract:
                texts.append(paper.abstract)
            elif paper.full_text:
                # Use first 1000 characters of full text
                texts.append(paper.full_text[:1000])

        if not texts:
            return {}

        # Use AI to identify methodological trends
        methodology_analysis = await self._analyze_methodologies(texts)

        # Extract methodology keywords
        methodology_keywords = self._extract_methodology_keywords(texts)

        return {
            "ai_methodology_analysis": methodology_analysis,
            "methodology_keywords": methodology_keywords,
        }

    async def identify_emerging_topics(
        self, papers: List[LiteratureItem], min_year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Identify emerging topics and research directions.

        Args:
            papers: List of literature items
            min_year: Minimum year to consider for emerging topics

        Returns:
            Dictionary with emerging topics analysis
        """
        if min_year is None:
            min_year = datetime.now().year - 3  # Last 3 years

        # Filter recent papers
        recent_papers = [
            paper
            for paper in papers
            if paper.publication_date and paper.publication_date.year >= min_year
        ]

        if not recent_papers:
            return {}

        # Extract text for analysis
        recent_texts = []
        for paper in recent_papers:
            if paper.abstract:
                recent_texts.append(paper.abstract)

        # Use AI to identify emerging topics
        emerging_analysis = await self._identify_emerging_topics_ai(
            recent_texts, min_year
        )

        # Analyze keyword emergence
        keyword_emergence = self._analyze_keyword_emergence(papers, min_year)

        return {
            "ai_emerging_analysis": emerging_analysis,
            "emerging_keywords": keyword_emergence,
            "recent_papers_count": len(recent_papers),
            "analysis_period": f"{min_year}-{datetime.now().year}",
        }

    def _analyze_publication_growth(
        self, yearly_data: Dict[int, Dict]
    ) -> Dict[str, Any]:
        """Analyze publication growth patterns."""
        years = sorted(yearly_data.keys())
        if len(years) < 2:
            return {}

        counts = [yearly_data[year]["count"] for year in years]

        # Calculate growth rate
        growth_rates = []
        for i in range(1, len(counts)):
            if counts[i - 1] > 0:
                growth_rate = ((counts[i] - counts[i - 1]) / counts[i - 1]) * 100
                growth_rates.append(growth_rate)

        avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0

        return {
            "years": years,
            "publication_counts": counts,
            "average_growth_rate": round(avg_growth_rate, 2),
            "total_growth": (
                round(((counts[-1] - counts[0]) / counts[0]) * 100, 2)
                if counts[0] > 0
                else 0
            ),
        }

    def _analyze_emerging_keywords(self, yearly_data: Dict[int, Dict]) -> List[str]:
        """Identify keywords that are becoming more frequent."""
        if len(yearly_data) < 2:
            return []

        years = sorted(yearly_data.keys())
        recent_years = years[-2:]  # Last 2 years
        earlier_years = years[:-2]

        if not earlier_years:
            return []

        # Compare keyword frequency
        recent_keywords = Counter()
        earlier_keywords = Counter()

        for year in recent_years:
            recent_keywords.update(yearly_data[year]["keywords"])

        for year in earlier_years:
            earlier_keywords.update(yearly_data[year]["keywords"])

        # Find emerging keywords (more frequent recently)
        emerging = []
        for keyword, recent_count in recent_keywords.items():
            earlier_count = earlier_keywords.get(keyword, 0)
            if recent_count > earlier_count * 1.5:  # 50% increase threshold
                emerging.append(keyword)

        return emerging[:10]

    def _analyze_evolving_categories(
        self, yearly_data: Dict[int, Dict]
    ) -> Dict[str, List]:
        """Analyze how research categories evolve over time."""
        category_evolution = {}

        for year, data in sorted(yearly_data.items()):
            year_categories = Counter(data["categories"])
            category_evolution[str(year)] = year_categories.most_common(5)

        return category_evolution

    def _analyze_keyword_by_year(self, papers: List[LiteratureItem]) -> Dict[str, Dict]:
        """Analyze keyword trends by year."""
        keyword_by_year = {}

        for paper in papers:
            if paper.keywords and paper.publication_date:
                year = str(paper.publication_date.year)
                if year not in keyword_by_year:
                    keyword_by_year[year] = Counter()

                for keyword in paper.keywords:
                    keyword_by_year[year][keyword.lower().strip()] += 1

        return {
            year: dict(counter.most_common(10))
            for year, counter in keyword_by_year.items()
        }

    def _extract_methodology_keywords(self, texts: List[str]) -> Dict[str, int]:
        """Extract methodology-related keywords from texts."""
        methodology_terms = [
            "machine learning",
            "deep learning",
            "neural network",
            "cnn",
            "rnn",
            "lstm",
            "random forest",
            "svm",
            "regression",
            "classification",
            "clustering",
            "survey",
            "experiment",
            "case study",
            "simulation",
            "modeling",
            "dataset",
            "benchmark",
            "evaluation",
            "validation",
            "cross-validation",
            "supervised",
            "unsupervised",
            "reinforcement learning",
            "semi-supervised",
            "transfer learning",
            "meta-learning",
            "few-shot",
            "zero-shot",
        ]

        method_counts = Counter()

        for text in texts:
            text_lower = text.lower()
            for term in methodology_terms:
                if term in text_lower:
                    method_counts[term] += 1

        return dict(method_counts.most_common(15))

    def _analyze_keyword_emergence(
        self, papers: List[LiteratureItem], min_year: int
    ) -> List[str]:
        """Analyze which keywords are emerging in recent years."""
        recent_keywords = Counter()
        older_keywords = Counter()

        for paper in papers:
            if paper.keywords and paper.publication_date:
                year = paper.publication_date.year
                keywords = [kw.lower().strip() for kw in paper.keywords]

                if year >= min_year:
                    recent_keywords.update(keywords)
                else:
                    older_keywords.update(keywords)

        # Find keywords that are more prominent recently
        emerging = []
        for keyword, recent_count in recent_keywords.items():
            older_count = older_keywords.get(keyword, 0)
            # Consider emerging if recent frequency is significantly higher
            if recent_count >= 2 and (
                older_count == 0 or recent_count > older_count * 2
            ):
                emerging.append(keyword)

        return emerging[:15]

    async def _generate_temporal_analysis(
        self, yearly_texts: List[str]
    ) -> Optional[str]:
        """Generate AI-powered temporal trend analysis."""
        combined_text = "\n".join(yearly_texts)

        system_prompt = (
            "You are a research trend analyst. Analyze the temporal patterns "
            "in publication data and keyword evolution. Identify growth trends, "
            "emerging themes, and shifts in research focus over time."
        )

        user_prompt = f"Analyze these yearly publication trends and identify key patterns:\n\n{combined_text}"

        return await self.llm_manager.generate_completion(
            prompt=user_prompt, system_prompt=system_prompt, temperature=0.4
        )

    async def _analyze_methodologies(self, texts: List[str]) -> Optional[str]:
        """Analyze methodological trends using AI."""
        combined_text = "\n\n---\n\n".join(texts[:10])  # Limit for token constraints

        system_prompt = (
            "You are a methodology expert. Analyze research methodologies, "
            "experimental designs, and analytical approaches used in academic papers. "
            "Identify common patterns, emerging methods, and methodological trends."
        )

        user_prompt = (
            f"Analyze the methodological approaches in these research abstracts "
            f"and identify key trends:\n\n{combined_text}"
        )

        return await self.llm_manager.generate_completion(
            prompt=user_prompt, system_prompt=system_prompt, temperature=0.4
        )

    async def _identify_emerging_topics_ai(
        self, texts: List[str], min_year: int
    ) -> Optional[str]:
        """Identify emerging topics using AI analysis."""
        combined_text = "\n\n---\n\n".join(texts[:8])  # Limit for token constraints

        system_prompt = (
            "You are a research trend analyst specializing in identifying "
            "emerging topics and novel research directions. Focus on new "
            "concepts, innovative applications, and evolving research areas."
        )

        user_prompt = (
            f"Based on these recent research abstracts from {min_year} onwards, "
            f"identify emerging topics and novel research directions:\n\n{combined_text}"
        )

        return await self.llm_manager.generate_completion(
            prompt=user_prompt, system_prompt=system_prompt, temperature=0.5
        )
