"""Report generator for creating structured literature review reports."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .llm_manager import LLMManager
from .summarizer import Summarizer
from .trend_analyzer import TrendAnalyzer
from ..retrieval.base_retriever import LiteratureItem
from ..utils.logger import LoggerMixin


class ReportGenerator(LoggerMixin):
    """Generator for comprehensive literature review reports."""

    def __init__(
        self,
        llm_manager: LLMManager,
        summarizer: Summarizer,
        trend_analyzer: TrendAnalyzer,
    ):
        """
        Initialize the report generator.

        Args:
            llm_manager: LLM manager for generating content
            summarizer: Literature summarizer for creating summaries
            trend_analyzer: Trend analyzer for identifying patterns
        """
        self.llm_manager = llm_manager
        self.summarizer = summarizer
        self.trend_analyzer = trend_analyzer
        self.logger.info("Initialized Report Generator")

    async def generate_comprehensive_report(
        self, papers: List[LiteratureItem], topic: str, output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive literature review report.

        Args:
            papers: List of literature items
            topic: Research topic/theme
            output_format: Output format (markdown, html, latex)

        Returns:
            Dictionary containing the generated report and metadata
        """
        if not papers:
            self.logger.warning("No papers provided for report generation")
            return {"error": "No papers to analyze"}

        self.logger.info(
            f"Generating comprehensive report for {len(papers)} papers on topic: {topic}"
        )

        # Generate all report sections concurrently
        tasks = [
            ("executive_summary", self._generate_executive_summary(papers, topic)),
            ("literature_overview", self._generate_literature_overview(papers)),
            ("temporal_analysis", self.trend_analyzer.analyze_temporal_trends(papers)),
            ("keyword_analysis", self.trend_analyzer.analyze_keyword_trends(papers)),
            (
                "methodology_analysis",
                self.trend_analyzer.analyze_methodological_trends(papers),
            ),
            (
                "collaboration_analysis",
                self.trend_analyzer.analyze_collaboration_patterns(papers),
            ),
            ("emerging_topics", self.trend_analyzer.identify_emerging_topics(papers)),
            (
                "key_findings",
                self.summarizer.generate_key_findings_summary(
                    [
                        p.abstract or p.full_text[:1000]
                        for p in papers
                        if p.abstract or p.full_text
                    ]
                ),
            ),
        ]

        # Execute tasks concurrently
        results = await asyncio.gather(
            *[task[1] for task in tasks], return_exceptions=True
        )

        # Compile results
        report_sections = {}
        for i, (section_name, _) in enumerate(tasks):
            if isinstance(results[i], Exception):
                self.logger.error(f"Error generating {section_name}: {results[i]}")
                report_sections[section_name] = None
            else:
                report_sections[section_name] = results[i]

        # Generate the final report
        report_content = await self._compile_report(
            report_sections, topic, papers, output_format
        )

        return {
            "content": report_content,
            "metadata": {
                "topic": topic,
                "paper_count": len(papers),
                "generation_date": datetime.now().isoformat(),
                "format": output_format,
                "sections": list(report_sections.keys()),
            },
            "sections": report_sections,
        }

    async def generate_section_report(
        self, papers: List[LiteratureItem], section_type: str, topic: str
    ) -> Optional[str]:
        """
        Generate a specific section of the report.

        Args:
            papers: List of literature items
            section_type: Type of section to generate
            topic: Research topic

        Returns:
            Generated section content
        """
        section_generators = {
            "executive_summary": lambda: self._generate_executive_summary(
                papers, topic
            ),
            "literature_overview": lambda: self._generate_literature_overview(papers),
            "methodology_summary": lambda: self.summarizer.generate_methodology_summary(
                [p.abstract or "" for p in papers]
            ),
            "key_findings": lambda: self.summarizer.generate_key_findings_summary(
                [p.abstract or "" for p in papers]
            ),
            "trend_analysis": lambda: self._generate_trend_summary(papers),
            "recommendations": lambda: self._generate_recommendations(papers, topic),
        }

        if section_type not in section_generators:
            self.logger.error(f"Unknown section type: {section_type}")
            return None

        try:
            return await section_generators[section_type]()
        except Exception as e:
            self.logger.error(f"Error generating {section_type}: {e}")
            return None

    async def generate_citation_report(
        self, papers: List[LiteratureItem], citation_style: str = "apa"
    ) -> str:
        """
        Generate a formatted citation list.

        Args:
            papers: List of literature items
            citation_style: Citation style (apa, mla, chicago, ieee)

        Returns:
            Formatted citation list
        """
        citations = []

        for i, paper in enumerate(papers, 1):
            citation = self._format_citation(paper, citation_style)
            citations.append(f"{i}. {citation}")

        citation_header = f"# References ({citation_style.upper()} Style)\n\n"
        return citation_header + "\n".join(citations)

    async def _generate_executive_summary(
        self, papers: List[LiteratureItem], topic: str
    ) -> Optional[str]:
        """Generate executive summary section."""
        # Combine abstracts for analysis
        abstracts = [paper.abstract for paper in papers if paper.abstract]
        if not abstracts:
            return "No abstracts available for executive summary generation."

        combined_abstracts = "\n\n---\n\n".join(
            abstracts[:10]
        )  # Limit for token constraints

        system_prompt = (
            "You are an expert research analyst creating an executive summary "
            "for a literature review. Provide a high-level overview that captures "
            "the essence of the research domain, key themes, and overall insights."
        )

        user_prompt = (
            f"Create an executive summary for a literature review on '{topic}' "
            f"based on {len(papers)} research papers. Highlight the main research "
            f"themes, significant findings, and the current state of the field:\n\n{combined_abstracts}"
        )

        return await self.llm_manager.generate_completion(
            prompt=user_prompt, system_prompt=system_prompt, temperature=0.4
        )

    async def _generate_literature_overview(
        self, papers: List[LiteratureItem]
    ) -> Optional[str]:
        """Generate literature overview section."""
        # Prepare paper statistics
        total_papers = len(papers)
        years = [p.publication_date.year for p in papers if p.publication_date]
        year_range = f"{min(years)}-{max(years)}" if years else "Unknown"

        # Top venues/journals
        venues = [p.venue for p in papers if p.venue]
        venue_counts = {}
        for venue in venues:
            venue_counts[venue] = venue_counts.get(venue, 0) + 1
        top_venues = sorted(venue_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        # Author information
        all_authors = []
        for paper in papers:
            if paper.authors:
                all_authors.extend(paper.authors)
        unique_authors = len(set(all_authors))

        # Create overview text
        overview_parts = [
            f"This literature review encompasses {total_papers} research papers published between {year_range}.",
            f"The analysis includes work from {unique_authors} unique authors across various venues and journals.",
        ]

        if top_venues:
            venue_text = "The most prominent publication venues include: " + ", ".join(
                [f"{venue} ({count} papers)" for venue, count in top_venues[:3]]
            )
            overview_parts.append(venue_text)

        # Add paper abstracts for AI analysis
        abstracts = [paper.abstract for paper in papers[:5] if paper.abstract]
        if abstracts:
            sample_text = "\n\n".join(abstracts)

            system_prompt = (
                "You are a research analyst. Based on the provided sample of research abstracts, "
                "describe the scope and nature of the research domain, methodological approaches, "
                "and key research directions represented in this literature collection."
            )

            user_prompt = (
                f"Based on these sample abstracts, provide an overview of the research domain "
                f"and methodological approaches:\n\n{sample_text}"
            )

            ai_overview = await self.llm_manager.generate_completion(
                prompt=user_prompt, system_prompt=system_prompt, temperature=0.3
            )

            if ai_overview:
                overview_parts.append(ai_overview)

        return "\n\n".join(overview_parts)

    async def _generate_trend_summary(
        self, papers: List[LiteratureItem]
    ) -> Optional[str]:
        """Generate trend analysis summary."""
        temporal_trends = await self.trend_analyzer.analyze_temporal_trends(papers)
        keyword_trends = await self.trend_analyzer.analyze_keyword_trends(papers)
        emerging_topics = await self.trend_analyzer.identify_emerging_topics(papers)

        trend_parts = []

        # Temporal trends
        if temporal_trends.get("publication_growth"):
            growth_data = temporal_trends["publication_growth"]
            growth_rate = growth_data.get("average_growth_rate", 0)
            trend_parts.append(
                f"Publication activity shows an average growth rate of {growth_rate:.1f}% per year."
            )

        # Top keywords
        if keyword_trends.get("top_keywords"):
            top_kw = keyword_trends["top_keywords"][:5]
            kw_text = "The most frequent research keywords are: " + ", ".join(
                [f"{kw} ({count})" for kw, count in top_kw]
            )
            trend_parts.append(kw_text)

        # Emerging topics
        if emerging_topics.get("ai_emerging_analysis"):
            trend_parts.append("Emerging Research Directions:")
            trend_parts.append(emerging_topics["ai_emerging_analysis"])

        return (
            "\n\n".join(trend_parts)
            if trend_parts
            else "No significant trends identified."
        )

    async def _generate_recommendations(
        self, papers: List[LiteratureItem], topic: str
    ) -> Optional[str]:
        """Generate research recommendations and future directions."""
        # Analyze recent papers for gaps and opportunities
        recent_papers = [
            p for p in papers if p.publication_date and p.publication_date.year >= 2022
        ]

        if not recent_papers:
            recent_papers = papers[-10:]  # Use most recent 10 papers

        abstracts = [paper.abstract for paper in recent_papers if paper.abstract]
        if not abstracts:
            return "Insufficient data for generating recommendations."

        combined_text = "\n\n---\n\n".join(abstracts[:8])

        system_prompt = (
            "You are a senior research advisor. Based on recent literature, "
            "identify research gaps, methodological limitations, and promising "
            "future research directions. Provide actionable recommendations for researchers."
        )

        user_prompt = (
            f"Based on this recent literature on '{topic}', identify research gaps "
            f"and recommend future research directions:\n\n{combined_text}"
        )

        return await self.llm_manager.generate_completion(
            prompt=user_prompt, system_prompt=system_prompt, temperature=0.5
        )

    async def _compile_report(
        self,
        sections: Dict[str, Any],
        topic: str,
        papers: List[LiteratureItem],
        output_format: str,
    ) -> str:
        """Compile all sections into a final report."""
        if output_format.lower() == "markdown":
            return self._compile_markdown_report(sections, topic, papers)
        elif output_format.lower() == "html":
            return self._compile_html_report(sections, topic, papers)
        elif output_format.lower() == "latex":
            return self._compile_latex_report(sections, topic, papers)
        else:
            return self._compile_markdown_report(sections, topic, papers)

    def _compile_markdown_report(
        self, sections: Dict[str, Any], topic: str, papers: List[LiteratureItem]
    ) -> str:
        """Compile report in Markdown format."""
        report_parts = [
            f"# Literature Review: {topic}",
            f"",
            f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Papers Analyzed:** {len(papers)}",
            f"",
            "---",
            "",
        ]

        # Executive Summary
        if sections.get("executive_summary"):
            report_parts.extend(
                [
                    "## Executive Summary",
                    "",
                    sections["executive_summary"],
                    "",
                    "---",
                    "",
                ]
            )

        # Literature Overview
        if sections.get("literature_overview"):
            report_parts.extend(
                [
                    "## Literature Overview",
                    "",
                    sections["literature_overview"],
                    "",
                    "---",
                    "",
                ]
            )

        # Temporal Analysis
        if sections.get("temporal_analysis"):
            temporal = sections["temporal_analysis"]
            report_parts.extend(
                ["## Temporal Analysis", "", "### Publication Trends", ""]
            )

            if temporal.get("yearly_summary"):
                report_parts.append("**Publications by Year:**")
                for year, count in sorted(temporal["yearly_summary"].items()):
                    report_parts.append(f"- {year}: {count} papers")
                report_parts.append("")

            if temporal.get("ai_insights"):
                report_parts.extend(
                    ["### Trend Insights", "", temporal["ai_insights"], ""]
                )

            report_parts.extend(["---", ""])

        # Keyword Analysis
        if sections.get("keyword_analysis"):
            keywords = sections["keyword_analysis"]
            report_parts.extend(
                ["## Keyword Analysis", "", "### Most Frequent Keywords", ""]
            )

            if keywords.get("top_keywords"):
                for i, (keyword, count) in enumerate(keywords["top_keywords"][:10], 1):
                    report_parts.append(f"{i}. **{keyword}** ({count} occurrences)")
                report_parts.append("")

            if keywords.get("keyword_cooccurrence"):
                report_parts.extend(["### Frequently Co-occurring Keywords", ""])
                for i, ((kw1, kw2), count) in enumerate(
                    keywords["keyword_cooccurrence"][:5], 1
                ):
                    report_parts.append(f"{i}. {kw1} + {kw2} ({count} times)")
                report_parts.append("")

            report_parts.extend(["---", ""])

        # Key Findings
        if sections.get("key_findings"):
            findings = sections["key_findings"]
            if findings:
                report_parts.extend(["## Key Findings", ""])

                for i, finding in enumerate(findings, 1):
                    report_parts.append(f"{i}. {finding}")

                report_parts.extend(["", "---", ""])

        # Methodology Analysis
        if sections.get("methodology_analysis"):
            methodology = sections["methodology_analysis"]
            if methodology.get("ai_methodology_analysis"):
                report_parts.extend(
                    [
                        "## Methodological Trends",
                        "",
                        methodology["ai_methodology_analysis"],
                        "",
                        "---",
                        "",
                    ]
                )

        # Emerging Topics
        if sections.get("emerging_topics"):
            emerging = sections["emerging_topics"]
            if emerging.get("ai_emerging_analysis"):
                report_parts.extend(
                    [
                        "## Emerging Topics and Future Directions",
                        "",
                        emerging["ai_emerging_analysis"],
                        "",
                        "---",
                        "",
                    ]
                )

        # Collaboration Analysis
        if sections.get("collaboration_analysis"):
            collab = sections["collaboration_analysis"]
            report_parts.extend(
                [
                    "## Collaboration Patterns",
                    "",
                    f"**Total Unique Authors:** {collab.get('total_unique_authors', 0)}",
                    f"**Average Team Size:** {collab.get('average_team_size', 0)} authors per paper",
                    "",
                ]
            )

            if collab.get("most_productive_authors"):
                report_parts.extend(["### Most Productive Authors", ""])
                for i, (author, count) in enumerate(
                    collab["most_productive_authors"][:5], 1
                ):
                    report_parts.append(f"{i}. {author} ({count} papers)")
                report_parts.append("")

            report_parts.extend(["---", ""])

        # Footer
        report_parts.extend(
            [
                "## Report Generation Details",
                "",
                f"- **Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"- **Papers Analyzed:** {len(papers)}",
                f"- **Topic:** {topic}",
                f"- **Generator:** AI Literature Review Agent",
                "",
            ]
        )

        return "\n".join(report_parts)

    def _compile_html_report(
        self, sections: Dict[str, Any], topic: str, papers: List[LiteratureItem]
    ) -> str:
        """Compile report in HTML format."""
        # Convert markdown to HTML (simplified version)
        markdown_content = self._compile_markdown_report(sections, topic, papers)

        # Basic HTML wrapper
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Literature Review: {topic}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        h1 {{ border-bottom: 2px solid #333; }}
        h2 {{ border-bottom: 1px solid #666; }}
        hr {{ margin: 20px 0; }}
        .metadata {{ background: #f5f5f5; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="metadata">
        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        <strong>Papers:</strong> {len(papers)}<br>
        <strong>Topic:</strong> {topic}
    </div>
    <pre>{markdown_content}</pre>
</body>
</html>
"""
        return html_content

    def _compile_latex_report(
        self, sections: Dict[str, Any], topic: str, papers: List[LiteratureItem]
    ) -> str:
        """Compile report in LaTeX format."""
        # Basic LaTeX template
        latex_content = f"""
\\documentclass{{article}}
\\usepackage{{geometry}}
\\usepackage{{hyperref}}
\\usepackage{{enumitem}}
\\geometry{{margin=1in}}

\\title{{Literature Review: {topic}}}
\\author{{AI Literature Review Agent}}
\\date{{{datetime.now().strftime('%B %d, %Y')}}}

\\begin{{document}}
\\maketitle

\\section{{Metadata}}
Total Papers Analyzed: {len(papers)} \\\\
Generation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

% Content sections would be added here with proper LaTeX formatting
% This is a simplified template

\\end{{document}}
"""
        return latex_content

    def _format_citation(self, paper: LiteratureItem, style: str) -> str:
        """Format a citation according to the specified style."""
        if style.lower() == "apa":
            return self._format_apa_citation(paper)
        elif style.lower() == "mla":
            return self._format_mla_citation(paper)
        elif style.lower() == "chicago":
            return self._format_chicago_citation(paper)
        elif style.lower() == "ieee":
            return self._format_ieee_citation(paper)
        else:
            return self._format_apa_citation(paper)

    def _format_apa_citation(self, paper: LiteratureItem) -> str:
        """Format citation in APA style."""
        authors = ", ".join(paper.authors[:3]) if paper.authors else "Unknown Author"
        if len(paper.authors or []) > 3:
            authors += ", et al."

        year = paper.publication_date.year if paper.publication_date else "n.d."
        title = paper.title or "Untitled"
        venue = paper.venue or "Unknown Venue"

        return f"{authors} ({year}). {title}. {venue}."

    def _format_mla_citation(self, paper: LiteratureItem) -> str:
        """Format citation in MLA style."""
        authors = ", ".join(paper.authors[:2]) if paper.authors else "Unknown Author"
        title = f'"{paper.title}"' if paper.title else '"Untitled"'
        venue = paper.venue or "Unknown Venue"
        year = paper.publication_date.year if paper.publication_date else "n.d."

        return f"{authors}. {title} {venue}, {year}."

    def _format_chicago_citation(self, paper: LiteratureItem) -> str:
        """Format citation in Chicago style."""
        return self._format_apa_citation(paper)  # Simplified

    def _format_ieee_citation(self, paper: LiteratureItem) -> str:
        """Format citation in IEEE style."""
        authors = ", ".join(paper.authors[:6]) if paper.authors else "Unknown Author"
        title = f'"{paper.title}"' if paper.title else '"Untitled"'
        venue = paper.venue or "Unknown Venue"
        year = paper.publication_date.year if paper.publication_date else "n.d."

        return f"{authors}, {title}, {venue}, {year}."
