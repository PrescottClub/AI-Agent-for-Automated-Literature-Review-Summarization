"""Literature summarizer for generating academic summaries."""

import asyncio
from typing import Any, Dict, List, Optional

from .llm_manager import LLMManager
from ..processing.text_processor import TextProcessor
from ..utils.logger import LoggerMixin


class LiteratureSummarizer(LoggerMixin):
    """Specialized summarizer for academic literature."""
    
    def __init__(self, llm_manager: LLMManager, text_processor: TextProcessor):
        """
        Initialize the literature summarizer.
        
        Args:
            llm_manager: LLM manager for generating summaries
            text_processor: Text processor for text analysis
        """
        self.llm_manager = llm_manager
        self.text_processor = text_processor
        self.logger.info("Initialized Literature Summarizer")
    
    async def generate_abstract_summary(self, 
                                      text: str,
                                      max_words: int = 250) -> Optional[str]:
        """
        Generate an academic abstract-style summary.
        
        Args:
            text: Input text to summarize
            max_words: Maximum words in summary
            
        Returns:
            Generated abstract summary
        """
        system_prompt = (
            "You are an expert academic writer. Create a structured abstract "
            "that includes: background/motivation, methods, key findings, and "
            "implications. Use formal academic language and present tense for "
            "established facts, past tense for specific study findings."
        )
        
        user_prompt = (
            f"Create an academic abstract (max {max_words} words) for this research content. "
            f"Structure it with clear sections covering background, methods, findings, and implications:\n\n{text}"
        )
        
        return await self.llm_manager.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
    
    async def generate_executive_summary(self, 
                                       text: str,
                                       max_words: int = 500) -> Optional[str]:
        """
        Generate an executive summary for research literature.
        
        Args:
            text: Input text to summarize
            max_words: Maximum words in summary
            
        Returns:
            Generated executive summary
        """
        system_prompt = (
            "You are an expert research analyst creating executive summaries "
            "for academic literature. Focus on practical implications, key insights, "
            "and actionable findings. Write for an educated but non-specialist audience."
        )
        
        user_prompt = (
            f"Create an executive summary (max {max_words} words) that highlights "
            f"the most important findings and their practical implications:\n\n{text}"
        )
        
        return await self.llm_manager.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.4
        )
    
    async def generate_literature_review_summary(self, 
                                               texts: List[str],
                                               topic: str,
                                               max_words: int = 1000) -> Optional[str]:
        """
        Generate a comprehensive literature review summary.
        
        Args:
            texts: List of literature texts to summarize
            topic: Research topic/theme
            max_words: Maximum words in summary
            
        Returns:
            Generated literature review summary
        """
        # Combine texts with clear separators
        combined_text = "\n\n---PAPER SEPARATOR---\n\n".join(texts)
        
        system_prompt = (
            "You are an expert academic researcher conducting a literature review. "
            "Synthesize multiple research papers into a coherent review that identifies "
            "common themes, conflicting findings, methodological approaches, and "
            "knowledge gaps. Organize by themes rather than paper-by-paper."
        )
        
        user_prompt = (
            f"Create a literature review summary (max {max_words} words) on '{topic}' "
            f"based on these research papers. Organize by themes and highlight "
            f"consensus, debates, and gaps in the literature:\n\n{combined_text}"
        )
        
        return await self.llm_manager.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.4
        )
    
    async def generate_key_findings_summary(self, 
                                          texts: List[str],
                                          max_findings: int = 10) -> Optional[List[str]]:
        """
        Extract and summarize key findings from literature.
        
        Args:
            texts: List of literature texts
            max_findings: Maximum number of findings to extract
            
        Returns:
            List of key findings
        """
        combined_text = "\n\n---PAPER SEPARATOR---\n\n".join(texts[:5])  # Limit for token constraints
        
        system_prompt = (
            "You are an expert research analyst. Extract the most significant "
            "and novel findings from academic literature. Focus on empirical "
            "results, theoretical contributions, and practical implications. "
            "Present each finding as a clear, standalone statement."
        )
        
        user_prompt = (
            f"Extract the {max_findings} most important findings from these research papers. "
            f"Each finding should be a clear, concise statement (1-2 sentences):\n\n{combined_text}"
        )
        
        result = await self.llm_manager.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        if result:
            # Parse findings from the result
            lines = [line.strip() for line in result.split('\n') if line.strip()]
            findings = []
            
            for line in lines:
                # Remove numbering if present
                clean_line = line.lstrip('0123456789.-• ').strip()
                if len(clean_line) > 20:  # Filter out very short lines
                    findings.append(clean_line)
            
            return findings[:max_findings]
        
        return None
    
    async def generate_methodology_summary(self, 
                                         texts: List[str],
                                         max_words: int = 400) -> Optional[str]:
        """
        Summarize research methodologies used in the literature.
        
        Args:
            texts: List of literature texts
            max_words: Maximum words in summary
            
        Returns:
            Methodology summary
        """
        combined_text = "\n\n---PAPER SEPARATOR---\n\n".join(texts[:3])
        
        system_prompt = (
            "You are a methodology expert analyzing research approaches. "
            "Summarize the research methods, data collection techniques, "
            "analytical approaches, and experimental designs used across "
            "multiple studies. Highlight common patterns and methodological diversity."
        )
        
        user_prompt = (
            f"Create a methodology summary (max {max_words} words) describing "
            f"the research approaches used in these papers:\n\n{combined_text}"
        )
        
        return await self.llm_manager.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
    
    async def generate_multi_level_summary(self, 
                                         text: str) -> Dict[str, Optional[str]]:
        """
        Generate summaries at multiple levels of detail.
        
        Args:
            text: Input text to summarize
            
        Returns:
            Dictionary with different summary levels
        """
        tasks = [
            ("brief", self._generate_brief_summary(text, 100)),
            ("standard", self._generate_standard_summary(text, 250)),
            ("detailed", self._generate_detailed_summary(text, 500))
        ]
        
        results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
        
        summaries = {}
        for i, (level, _) in enumerate(tasks):
            if isinstance(results[i], str):
                summaries[level] = results[i]
            else:
                summaries[level] = None
                self.logger.error(f"Error generating {level} summary: {results[i]}")
        
        return summaries
    
    async def _generate_brief_summary(self, text: str, max_words: int) -> Optional[str]:
        """Generate a brief summary."""
        system_prompt = "Create a very concise summary focusing only on the main finding or contribution."
        user_prompt = f"Summarize in {max_words} words or less:\n\n{text}"
        
        return await self.llm_manager.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.2
        )
    
    async def _generate_standard_summary(self, text: str, max_words: int) -> Optional[str]:
        """Generate a standard summary."""
        system_prompt = "Create a balanced summary covering main points, methods, and conclusions."
        user_prompt = f"Summarize in {max_words} words or less:\n\n{text}"
        
        return await self.llm_manager.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
    
    async def _generate_detailed_summary(self, text: str, max_words: int) -> Optional[str]:
        """Generate a detailed summary."""
        system_prompt = "Create a comprehensive summary including background, methods, results, and implications."
        user_prompt = f"Summarize in {max_words} words or less:\n\n{text}"
        
        return await self.llm_manager.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.4
        ) 