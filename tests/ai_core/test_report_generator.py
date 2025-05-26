import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.lit_review_agent.ai_core.report_generator import ReportGenerator
from src.lit_review_agent.ai_core.llm_manager import LLMManager
from src.lit_review_agent.ai_core.summarizer import LiteratureSummarizer
from src.lit_review_agent.ai_core.trend_analyzer import TrendAnalyzer
from src.lit_review_agent.retrieval.base_retriever import LiteratureItem
from src.lit_review_agent.utils.config import Config

class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        # Mock dependencies
        self.mock_llm_manager = MagicMock(spec=LLMManager)
        self.mock_summarizer = MagicMock(spec=LiteratureSummarizer)
        self.mock_trend_analyzer = MagicMock(spec=TrendAnalyzer)

        # Configure mocks to return AsyncMock for async methods
        self.mock_llm_manager.generate_completion = AsyncMock(return_value="Mocked LLM output")
        
        self.mock_summarizer.generate_key_findings_summary = AsyncMock(return_value=["Finding 1", "Finding 2"])
        self.mock_summarizer.generate_methodology_summary = AsyncMock(return_value="Mocked methodology summary")

        self.mock_trend_analyzer.analyze_temporal_trends = AsyncMock(return_value={"ai_insights": "Temporal insights"})
        self.mock_trend_analyzer.analyze_keyword_trends = AsyncMock(return_value={"top_keywords": [("kw1", 10)]})
        self.mock_trend_analyzer.analyze_methodological_trends = AsyncMock(return_value={"ai_methodology_analysis": "Methodology insights"})
        self.mock_trend_analyzer.analyze_collaboration_patterns = AsyncMock(return_value={"total_unique_authors": 5})
        self.mock_trend_analyzer.identify_emerging_topics = AsyncMock(return_value={"ai_emerging_analysis": "Emerging topics insights"})

        self.report_generator = ReportGenerator(
            llm_manager=self.mock_llm_manager,
            summarizer=self.mock_summarizer,
            trend_analyzer=self.mock_trend_analyzer
        )

        # Sample paper for testing
        self.sample_paper = LiteratureItem(
            id="test_id_1",
            title="Test Paper Title",
            authors=["Author A", "Author B"],
            abstract="This is a test abstract.",
            publication_date=datetime(2023, 1, 1),
            url="http://example.com/test_paper",
            venue="Test Journal",
            keywords=["test", "keyword"],
            categories=["cs.AI"]
        )
        self.sample_papers = [self.sample_paper]

    def test_initialization(self):
        self.assertIsNotNone(self.report_generator)
        self.assertEqual(self.report_generator.llm_manager, self.mock_llm_manager)
        self.assertEqual(self.report_generator.summarizer, self.mock_summarizer)
        self.assertEqual(self.report_generator.trend_analyzer, self.mock_trend_analyzer)

    def test_generate_comprehensive_report_no_papers(self):
        report = asyncio.run(self.report_generator.generate_comprehensive_report([], "test_topic"))
        self.assertIn("error", report)
        self.assertEqual(report["error"], "No papers to analyze")

    def test_generate_comprehensive_report_markdown(self):
        # Configure internal mock calls for _generate_executive_summary etc.
        self.report_generator._generate_executive_summary = AsyncMock(return_value="Mocked exec summary")
        self.report_generator._generate_literature_overview = AsyncMock(return_value="Mocked lit overview")

        report_data = asyncio.run(
            self.report_generator.generate_comprehensive_report(
                self.sample_papers, "Sample Topic", "markdown"
            )
        )
        
        self.assertIn("content", report_data)
        self.assertIn("metadata", report_data)
        self.assertIn("sections", report_data)
        self.assertIsInstance(report_data["content"], str)
        self.assertIn("# Literature Review: Sample Topic", report_data["content"])
        self.assertIn("## Executive Summary", report_data["content"])
        self.assertIn("Mocked exec summary", report_data["content"])

        # Check if mocked methods were called
        self.report_generator._generate_executive_summary.assert_called_once()
        self.mock_summarizer.generate_key_findings_summary.assert_called_once()
        self.mock_trend_analyzer.analyze_temporal_trends.assert_called_once()

    def test_generate_citation_report_apa(self):
        report = asyncio.run(self.report_generator.generate_citation_report(self.sample_papers, "apa"))
        self.assertIn("# References (APA Style)", report)
        self.assertIn("Author A, Author B (2023). Test Paper Title. Test Journal.", report)

    def test_format_apa_citation(self):
        citation = self.report_generator._format_apa_citation(self.sample_paper)
        expected = "Author A, Author B (2023). Test Paper Title. Test Journal."
        self.assertEqual(citation, expected)

    def test_compile_markdown_report(self):
        mock_sections = {
            "executive_summary": "Test Executive Summary.",
            "literature_overview": "Test Literature Overview.",
            "temporal_analysis": {"ai_insights": "Temporal insights here.", "yearly_summary": {2023: 1}},
            "keyword_analysis": {"top_keywords": [("test", 1)], "keyword_cooccurrence": [(("test", "ai"), 1)]},
            "key_findings": ["Finding Alpha."],
            "methodology_analysis": {"ai_methodology_analysis": "Methodology insights here."},
            "emerging_topics": {"ai_emerging_analysis": "Emerging topics here."},
            "collaboration_analysis": {"total_unique_authors": 2, "average_team_size": 2.0, "most_productive_authors": [("Author A", 1)]}
        }
        report_content = self.report_generator._compile_markdown_report(mock_sections, "Test Topic", self.sample_papers)
        
        self.assertIn("# Literature Review: Test Topic", report_content)
        self.assertIn("## Executive Summary", report_content)
        self.assertIn("Test Executive Summary.", report_content)
        self.assertIn("- 2023: 1 papers", report_content) # Check temporal_analysis output
        self.assertIn("1. **test** (1 occurrences)", report_content) # Check keyword_analysis output

    # You can add more tests for HTML and LaTeX compilation if needed,
    # and for specific private methods like _generate_executive_summary by making them temporarily public
    # or by more intricate mocking if they remain private.

if __name__ == '__main__':
    unittest.main() 