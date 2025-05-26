"""Main Literature Review Agent class integrating all modules."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .ai_core.llm_manager import LLMManager
from .processing.text_processor import TextProcessor
from .processing.vector_store import VectorStore
from .retrieval.arxiv_client import ArxivClient
from .retrieval.base_retriever import LiteratureItem
from .retrieval.pdf_processor import PDFProcessor
from .utils.config import Config
from .utils.logger import LoggerMixin
from .ai_core.summarizer import LiteratureSummarizer
from .ai_core.trend_analyzer import TrendAnalyzer
from .ai_core.report_generator import ReportGenerator


class LiteratureAgent(LoggerMixin):
    """Main agent for automated literature review and summarization."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the Literature Agent.
        
        Args:
            config: Configuration object (uses default if None)
        """
        self.config = config or Config()
        
        # Initialize components
        self.llm_manager = LLMManager(
            config=self.config
        )
        
        self.text_processor = TextProcessor()
        
        self.vector_store = VectorStore(
            persist_directory=self.config.chroma_persist_directory,
            collection_name=self.config.chroma_collection_name,
            embedding_model=self.config.openai_embedding_model
        )
        
        self.arxiv_client = ArxivClient(
            max_results=self.config.arxiv_max_results
        )
        
        self.pdf_processor = PDFProcessor()
        
        # Initialize AI Core components needed for ReportGenerator
        self.summarizer = LiteratureSummarizer(
            llm_manager=self.llm_manager, 
            text_processor=self.text_processor
        )
        self.trend_analyzer = TrendAnalyzer(
            llm_manager=self.llm_manager, 
            text_processor=self.text_processor
        )
        self.report_generator = ReportGenerator(
            llm_manager=self.llm_manager,
            summarizer=self.summarizer,
            trend_analyzer=self.trend_analyzer
        )
        
        self.logger.info("Initialized Literature Agent")
    
    async def conduct_literature_review(self,
                                      research_topic: str,
                                      max_papers: int = 50,
                                      include_full_text: bool = False) -> Dict[str, Any]:
        """
        Conduct a comprehensive literature review on a topic.
        
        Args:
            research_topic: Research topic or query
            max_papers: Maximum number of papers to retrieve
            include_full_text: Whether to download and process full text
            
        Returns:
            Dictionary with literature review results
        """
        self.logger.info(f"Starting literature review for: {research_topic}")
        
        results = {
            "topic": research_topic,
            "timestamp": datetime.utcnow().isoformat(),
            "papers": [],
            "summary": None,
            "key_insights": [],
            "research_gaps": [],
            "trends": {},
            "statistics": {}
        }
        
        try:
            # Step 1: Search for papers
            self.logger.info("Searching for papers...")
            papers = await self.arxiv_client.search(research_topic, max_papers)
            
            if not papers:
                self.logger.warning("No papers found for the given topic")
                return results
            
            # Step 2: Process papers and extract full text if requested
            if include_full_text:
                self.logger.info("Processing full text of papers...")
                papers = await self._process_full_text(papers)
            
            # Step 3: Add papers to vector store
            self.logger.info("Adding papers to vector store...")
            added_count = self.vector_store.add_literature_items(papers)
            self.logger.info(f"Added {added_count} papers to vector store")
            
            # Step 4: Generate summaries and insights
            self.logger.info("Generating summaries and insights...")
            paper_texts = []
            processed_papers = []
            
            for paper in papers[:max_papers]:
                # Process paper text
                text_content = self._get_paper_text(paper)
                if text_content:
                    paper_texts.append(text_content)
                
                # Extract additional information
                paper_data = {
                    "id": paper.id,
                    "title": paper.title,
                    "authors": paper.authors,
                    "abstract": paper.abstract,
                    "publication_date": paper.publication_date.isoformat() if paper.publication_date else None,
                    "journal": paper.journal,
                    "categories": paper.categories,
                    "url": paper.url,
                    "summary": None,
                    "keywords": [],
                    "entities": {}
                }
                
                # Generate summary for individual paper
                if text_content:
                    summary = await self.llm_manager.generate_summary(
                        text_content,
                        summary_type="abstract",
                        max_length=200
                    )
                    paper_data["summary"] = summary
                    
                    # Extract keywords and entities
                    paper_data["keywords"] = self.text_processor.extract_research_keywords(text_content)
                    paper_data["entities"] = self.text_processor.extract_entities(text_content)
                
                processed_papers.append(paper_data)
            
            results["papers"] = processed_papers
            
            # Step 5: Generate overall summary
            if paper_texts:
                self.logger.info("Generating overall literature review summary...")
                combined_text = "\n\n".join(paper_texts[:10])  # Limit for token constraints
                
                overall_summary = await self.llm_manager.generate_summary(
                    combined_text,
                    summary_type="executive",
                    max_length=1000
                )
                results["summary"] = overall_summary
                
                # Step 6: Extract key insights
                self.logger.info("Extracting key insights...")
                insights = await self.llm_manager.extract_key_insights(combined_text)
                results["key_insights"] = insights or []
                
                # Step 7: Identify research gaps
                self.logger.info("Identifying research gaps...")
                gaps = await self.llm_manager.identify_research_gaps(paper_texts[:5])
                results["research_gaps"] = gaps or []
                
                # Step 8: Analyze trends
                self.logger.info("Analyzing trends...")
                trends = await self.llm_manager.analyze_trends(paper_texts[:5])
                results["trends"] = trends or {}
            
            # Step 9: Generate statistics
            results["statistics"] = self._generate_statistics(papers)
            
            self.logger.info("Literature review completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error conducting literature review: {e}")
            results["error"] = str(e)
            return results
    
    async def search_similar_papers(self,
                                  query: str,
                                  n_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for papers similar to a query using vector similarity.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of similar papers
        """
        try:
            self.logger.info(f"Searching for similar papers: {query}")
            
            results = self.vector_store.search_similar(
                query=query,
                n_results=n_results
            )
            
            self.logger.info(f"Found {len(results)} similar papers")
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching similar papers: {e}")
            return []
    
    async def generate_custom_summary(self,
                                    paper_ids: List[str],
                                    summary_type: str = "executive") -> Optional[str]:
        """
        Generate a custom summary for specific papers.
        
        Args:
            paper_ids: List of paper IDs
            summary_type: Type of summary to generate
            
        Returns:
            Generated summary or None if failed
        """
        try:
            self.logger.info(f"Generating custom summary for {len(paper_ids)} papers")
            
            # Retrieve papers from vector store
            paper_texts = []
            for paper_id in paper_ids:
                paper_data = self.vector_store.get_item_by_id(paper_id)
                if paper_data and paper_data["document"]:
                    paper_texts.append(paper_data["document"])
            
            if not paper_texts:
                self.logger.warning("No paper texts found for summary generation")
                return None
            
            # Combine texts
            combined_text = "\n\n---\n\n".join(paper_texts)
            
            # Generate summary
            summary = await self.llm_manager.generate_summary(
                combined_text,
                summary_type=summary_type,
                max_length=1000
            )
            
            self.logger.info("Custom summary generated successfully")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating custom summary: {e}")
            return None
    
    async def export_results(self,
                           results: Dict[str, Any],
                           output_format: str = "markdown",
                           output_file: Optional[str] = None) -> bool:
        """
        Export literature review results to file.
        
        Args:
            results: Literature review results
            output_format: Output format (markdown, json, txt)
            output_file: Output file path (auto-generated if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate output filename if not provided
            if not output_file:
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                topic_safe = "".join(c for c in results.get("topic", "review") if c.isalnum() or c in (' ', '-', '_')).rstrip()
                topic_safe = topic_safe.replace(' ', '_')[:50]
                
                output_file = f"{self.config.output_dir}/literature_review_{topic_safe}_{timestamp}.{output_format}"
            
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate content based on format
            if output_format == "markdown":
                content = self._generate_markdown_report(results)
            elif output_format == "json":
                import json
                content = json.dumps(results, indent=2, ensure_ascii=False)
            else:  # txt
                content = self._generate_text_report(results)
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Results exported to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting results: {e}")
            return False
    
    async def generate_full_report(self, 
                                 papers: List[LiteratureItem], 
                                 topic: str, 
                                 output_format: str = "markdown") -> Dict[str, Any]:
        """
        Generates a comprehensive literature review report using ReportGenerator.

        Args:
            papers: List of literature items.
            topic: The research topic.
            output_format: The desired output format (markdown, html, latex).

        Returns:
            A dictionary containing the report content and metadata.
        """
        self.logger.info(f"Generating full report for topic '{topic}' in {output_format} format.")
        if not self.report_generator:
            self.logger.error("ReportGenerator is not initialized.")
            return {"error": "ReportGenerator not initialized."}
        
        try:
            report_data = await self.report_generator.generate_comprehensive_report(
                papers=papers,
                topic=topic,
                output_format=output_format
            )
            self.logger.info(f"Successfully generated full report for topic '{topic}'.")
            return report_data
        except Exception as e:
            self.logger.error(f"Error generating full report: {e}")
            return {"error": str(e)}
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics.
        
        Returns:
            Dictionary with agent statistics
        """
        try:
            vector_stats = self.vector_store.get_collection_stats()
            
            return {
                "vector_store": vector_stats,
                "llm_requests": getattr(self.llm_manager, 'request_count', 0),
                "config": {
                    "model": self.config.openai_model,
                    "max_papers": self.config.arxiv_max_results
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {}
    
    async def _process_full_text(self, papers: List[LiteratureItem]) -> List[LiteratureItem]:
        """Process full text for papers with PDF URLs."""
        processed_papers = []
        
        for paper in papers:
            if paper.pdf_url:
                try:
                    full_text = await self.pdf_processor.extract_text_from_url(paper.pdf_url)
                    if full_text:
                        paper.full_text = full_text
                        self.logger.info(f"Extracted full text for: {paper.title}")
                except Exception as e:
                    self.logger.warning(f"Failed to extract full text for {paper.title}: {e}")
            
            processed_papers.append(paper)
        
        return processed_papers
    
    def _get_paper_text(self, paper: LiteratureItem) -> str:
        """Get the best available text content for a paper."""
        if paper.full_text:
            return paper.full_text
        elif paper.abstract:
            title_and_abstract = f"Title: {paper.title}\n\nAbstract: {paper.abstract}"
            return title_and_abstract
        else:
            return paper.title or ""
    
    def _generate_statistics(self, papers: List[LiteratureItem]) -> Dict[str, Any]:
        """Generate statistics about the retrieved papers."""
        if not papers:
            return {}
        
        # Year distribution
        years = [p.year for p in papers if p.year]
        year_counts = {}
        for year in years:
            year_counts[year] = year_counts.get(year, 0) + 1
        
        # Author analysis
        all_authors = []
        for paper in papers:
            all_authors.extend(paper.authors)
        
        author_counts = {}
        for author in all_authors:
            author_counts[author] = author_counts.get(author, 0) + 1
        
        # Category analysis
        all_categories = []
        for paper in papers:
            all_categories.extend(paper.categories)
        
        category_counts = {}
        for category in all_categories:
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "total_papers": len(papers),
            "date_range": {
                "earliest": min(years) if years else None,
                "latest": max(years) if years else None
            },
            "top_authors": sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "top_categories": sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "year_distribution": year_counts
        }
    
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate a markdown report from results."""
        lines = []
        
        lines.append(f"# Literature Review: {results.get('topic', 'Unknown Topic')}")
        lines.append(f"\nGenerated on: {results.get('timestamp', 'Unknown')}")
        lines.append("\n---\n")
        
        # Summary
        if results.get("summary"):
            lines.append("## Executive Summary\n")
            lines.append(results["summary"])
            lines.append("\n")
        
        # Key Insights
        if results.get("key_insights"):
            lines.append("## Key Insights\n")
            for i, insight in enumerate(results["key_insights"], 1):
                lines.append(f"{i}. {insight}")
            lines.append("\n")
        
        # Research Gaps
        if results.get("research_gaps"):
            lines.append("## Research Gaps and Future Opportunities\n")
            for i, gap in enumerate(results["research_gaps"], 1):
                lines.append(f"{i}. {gap}")
            lines.append("\n")
        
        # Statistics
        if results.get("statistics"):
            stats = results["statistics"]
            lines.append("## Statistics\n")
            lines.append(f"- Total Papers: {stats.get('total_papers', 0)}")
            
            if stats.get("date_range"):
                dr = stats["date_range"]
                lines.append(f"- Date Range: {dr.get('earliest', 'Unknown')} - {dr.get('latest', 'Unknown')}")
            
            if stats.get("top_categories"):
                lines.append("\n### Top Categories")
                for category, count in stats["top_categories"][:5]:
                    lines.append(f"- {category}: {count} papers")
            
            lines.append("\n")
        
        # Papers
        if results.get("papers"):
            lines.append("## Papers Reviewed\n")
            for i, paper in enumerate(results["papers"], 1):
                lines.append(f"### {i}. {paper.get('title', 'Unknown Title')}")
                
                if paper.get("authors"):
                    authors = ", ".join(paper["authors"][:3])
                    if len(paper["authors"]) > 3:
                        authors += " et al."
                    lines.append(f"**Authors:** {authors}")
                
                if paper.get("publication_date"):
                    lines.append(f"**Date:** {paper['publication_date']}")
                
                if paper.get("summary"):
                    lines.append(f"**Summary:** {paper['summary']}")
                
                if paper.get("url"):
                    lines.append(f"**URL:** {paper['url']}")
                
                lines.append("\n")
        
        return "\n".join(lines)
    
    def _generate_text_report(self, results: Dict[str, Any]) -> str:
        """Generate a plain text report from results."""
        lines = []
        
        lines.append(f"LITERATURE REVIEW: {results.get('topic', 'Unknown Topic').upper()}")
        lines.append("=" * 80)
        lines.append(f"Generated on: {results.get('timestamp', 'Unknown')}")
        lines.append("")
        
        # Summary
        if results.get("summary"):
            lines.append("EXECUTIVE SUMMARY")
            lines.append("-" * 40)
            lines.append(results["summary"])
            lines.append("")
        
        # Key Insights
        if results.get("key_insights"):
            lines.append("KEY INSIGHTS")
            lines.append("-" * 40)
            for i, insight in enumerate(results["key_insights"], 1):
                lines.append(f"{i}. {insight}")
            lines.append("")
        
        # Research Gaps
        if results.get("research_gaps"):
            lines.append("RESEARCH GAPS AND FUTURE OPPORTUNITIES")
            lines.append("-" * 40)
            for i, gap in enumerate(results["research_gaps"], 1):
                lines.append(f"{i}. {gap}")
            lines.append("")
        
        # Statistics
        if results.get("statistics"):
            stats = results["statistics"]
            lines.append("STATISTICS")
            lines.append("-" * 40)
            lines.append(f"Total Papers: {stats.get('total_papers', 0)}")
            
            if stats.get("date_range"):
                dr = stats["date_range"]
                lines.append(f"Date Range: {dr.get('earliest', 'Unknown')} - {dr.get('latest', 'Unknown')}")
            
            lines.append("")
        
        return "\n".join(lines) 