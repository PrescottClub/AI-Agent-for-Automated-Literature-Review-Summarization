"""LLM manager for handling OpenAI API interactions."""

import asyncio
import re
import time
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from ..utils.logger import LoggerMixin
from ..utils.helpers import estimate_tokens, truncate_text
from ..utils.config import Config


class LLMManager(LoggerMixin):
    """Manager for Large Language Model interactions."""
    
    def __init__(self, 
                 config: Config,
                 max_tokens_per_request: Optional[int] = None,
                 max_requests_per_minute: Optional[int] = None):
        """
        Initialize the LLM manager.
        
        Args:
            config: Configuration object containing API keys and provider info.
            max_tokens_per_request: Maximum tokens per request (overrides config if set)
            max_requests_per_minute: Rate limit for requests (overrides config if set)
        """
        self.config = config
        self.provider = config.llm_provider.lower()
        
        self.max_tokens = max_tokens_per_request or config.max_tokens_per_request
        self.max_requests_per_minute = max_requests_per_minute or config.max_requests_per_minute
        
        if self.provider == "openai":
            if not config.openai_api_key:
                raise ValueError("OpenAI API key is required for OpenAI provider.")
            self.client = OpenAI(
                api_key=config.openai_api_key,
                base_url=config.openai_api_base
            )
            self.model = config.openai_model
            self.logger.info(f"Initialized LLM manager with OpenAI provider, model: {self.model}")
        elif self.provider == "deepseek":
            if not config.deepseek_api_key:
                raise ValueError("DeepSeek API key is required for DeepSeek provider.")
            self.client = OpenAI(
                api_key=config.deepseek_api_key,
                base_url=config.deepseek_api_base
            )
            self.model = config.deepseek_model
            self.logger.info(f"Initialized LLM manager with DeepSeek provider, model: {self.model}")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}. Choose 'openai' or 'deepseek'.")
        
        # Rate limiting
        self.last_request_time = 0
        self.request_count = 0
        self.request_times = []
    
    async def generate_completion(self,
                                prompt: str,
                                max_tokens: Optional[int] = None,
                                temperature: float = 0.7,
                                system_prompt: Optional[str] = None) -> Optional[str]:
        """
        Generate a completion for the given prompt.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            system_prompt: Optional system prompt
            
        Returns:
            Generated completion or None if failed
        """
        try:
            # Rate limiting
            await self._wait_for_rate_limit()
            
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Estimate token usage and truncate if necessary
            total_tokens = sum(estimate_tokens(msg["content"]) for msg in messages)
            response_tokens = max_tokens or (self.max_tokens // 2)
            
            if total_tokens + response_tokens > self.max_tokens:
                # Truncate the user prompt
                available_tokens = self.max_tokens - response_tokens
                if system_prompt:
                    available_tokens -= estimate_tokens(system_prompt)
                
                truncated_prompt = truncate_text(prompt, available_tokens)
                messages[-1]["content"] = truncated_prompt
                self.logger.warning(f"Truncated prompt to fit token limit")
            
            # Make API call
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens or (self.max_tokens // 2),
                    temperature=temperature
                )
            )
            
            # Track request
            self._track_request()
            
            # Extract and return content
            if response.choices and response.choices[0].message:
                content = response.choices[0].message.content
                self.logger.info(f"Generated completion: {len(content)} characters")
                return content
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error generating completion: {e}")
            return None
    
    async def generate_summary(self,
                             text: str,
                             summary_type: str = "abstract",
                             max_length: int = 500) -> Optional[str]:
        """
        Generate a summary of the given text.
        
        Args:
            text: Text to summarize
            summary_type: Type of summary (abstract, executive, bullet)
            max_length: Maximum length of summary
            
        Returns:
            Generated summary or None if failed
        """
        # Prepare system prompt based on summary type
        if summary_type == "abstract":
            system_prompt = (
                "You are an expert academic summarizer. Create a concise, "
                "informative abstract that captures the key findings, methods, "
                "and implications of the research."
            )
            user_prompt = f"Summarize this research paper in {max_length} words or less:\n\n{text}"
        
        elif summary_type == "executive":
            system_prompt = (
                "You are a professional executive summarizer. Create a "
                "high-level summary focusing on key insights, implications, "
                "and actionable information."
            )
            user_prompt = f"Create an executive summary of this research in {max_length} words or less:\n\n{text}"
        
        elif summary_type == "bullet":
            system_prompt = (
                "You are a content organizer. Create a bullet-point summary "
                "that highlights the main points in an easy-to-read format."
            )
            user_prompt = f"Create a bullet-point summary of this research:\n\n{text}"
        
        else:
            system_prompt = "You are a helpful AI assistant that creates clear, concise summaries."
            user_prompt = f"Summarize this text in {max_length} words or less:\n\n{text}"
        
        return await self.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3  # Lower temperature for summaries
        )
    
    async def extract_key_insights(self, text: str) -> Optional[List[str]]:
        """
        Extract key insights from text.
        
        Args:
            text: Input text
            
        Returns:
            List of key insights or None if failed
        """
        system_prompt = (
            "You are an expert research analyst. Extract the most important "
            "insights, findings, and contributions from the given text. "
            "Return each insight as a separate line."
        )
        
        user_prompt = f"Extract the key insights from this research:\n\n{text}"
        
        result = await self.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        if result:
            # Split into individual insights
            insights = [line.strip() for line in result.split('\n') if line.strip()]
            # Remove numbered prefixes if present
            insights = [re.sub(r'^\d+\.\s*', '', insight) for insight in insights]
            return [insight for insight in insights if len(insight) > 10]
        
        return None
    
    async def identify_research_gaps(self, texts: List[str]) -> Optional[List[str]]:
        """
        Identify research gaps from multiple texts.
        
        Args:
            texts: List of research texts
            
        Returns:
            List of identified research gaps or None if failed
        """
        # Combine texts with separators
        combined_text = "\n\n---\n\n".join(texts)
        
        system_prompt = (
            "You are an expert research analyst specializing in identifying "
            "research gaps and future opportunities. Analyze the provided "
            "research papers and identify areas that need further investigation."
        )
        
        user_prompt = (
            "Based on these research papers, identify the main research gaps "
            "and opportunities for future work. Focus on limitations mentioned "
            "by authors and areas that are underexplored:\n\n" + combined_text
        )
        
        result = await self.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.4
        )
        
        if result:
            # Split into individual gaps
            gaps = [line.strip() for line in result.split('\n') if line.strip()]
            # Remove numbered prefixes if present
            gaps = [re.sub(r'^\d+\.\s*', '', gap) for gap in gaps]
            return [gap for gap in gaps if len(gap) > 20]
        
        return None
    
    async def analyze_trends(self, texts: List[str]) -> Optional[Dict[str, Any]]:
        """
        Analyze trends from multiple research texts.
        
        Args:
            texts: List of research texts
            
        Returns:
            Dictionary with trend analysis or None if failed
        """
        combined_text = "\n\n---\n\n".join(texts)
        
        system_prompt = (
            "You are an expert research trend analyst. Identify emerging "
            "themes, methodological trends, and technological developments "
            "from the provided research papers."
        )
        
        user_prompt = (
            "Analyze these research papers and identify:\n"
            "1. Emerging themes and topics\n"
            "2. Popular methodologies and approaches\n"
            "3. Technology trends\n"
            "4. Collaboration patterns\n\n" + combined_text
        )
        
        result = await self.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.4
        )
        
        if result:
            return {"analysis": result}
        
        return None
    
    async def _wait_for_rate_limit(self):
        """Wait if necessary to respect rate limits."""
        current_time = time.time()
        
        # Clean old request times (older than 1 minute)
        self.request_times = [
            t for t in self.request_times 
            if current_time - t < 60
        ]
        
        # Check if we need to wait
        if len(self.request_times) >= self.max_requests_per_minute:
            wait_time = 60 - (current_time - self.request_times[0])
            if wait_time > 0:
                self.logger.info(f"Rate limit reached, waiting {wait_time:.1f} seconds")
                await asyncio.sleep(wait_time)
    
    def _track_request(self):
        """Track a request for rate limiting."""
        self.request_times.append(time.time())
        self.request_count += 1 