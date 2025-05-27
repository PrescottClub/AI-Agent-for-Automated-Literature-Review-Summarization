"""Literature summarizer for generating academic summaries."""

import asyncio
from typing import Any, Dict, List, Optional

from .llm_manager import LLMManager, LLMManagerError
from ..processing.text_processor import TextProcessor
from ..utils.logger import get_logger, LoggerMixin
from ..utils.config import Config

logger = get_logger(__name__)

class SummarizerError(Exception):
    """Custom exception for Summarizer errors."""
    pass

class Summarizer(LoggerMixin):
    """
    Handles text summarization tasks using an LLMManager.
    Provides methods for different types of summaries (e.g., abstractive, extractive, keyword-focused).
    """
    def __init__(self, llm_manager: LLMManager, config: Config):
        super().__init__()
        self.llm_manager = llm_manager
        self.config = config
        self.logger.info("Summarizer initialized.")

    async def summarize_text(
        self,
        text: str,
        summary_type: str = "general", # e.g., "general", "key_findings", "abstract_enhancement"
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        prompt_template: Optional[str] = None,
        context: Optional[str] = None # Optional context like research topic
    ) -> str:
        """
        Generates a summary for the given text using the configured LLM.

        Args:
            text: The text to summarize.
            summary_type: A hint for the type of summary to generate, influencing the prompt.
            max_tokens: Maximum tokens for the summary. Uses provider default from config if None.
            temperature: Temperature for generation. Uses provider default from config if None.
            prompt_template: A custom f-string template for the user prompt. 
                             Must include '{text_to_summarize}' and optionally '{context}'.
            context: Optional contextual information (e.g., research topic) for the prompt.

        Returns:
            The generated summary string.

        Raises:
            SummarizerError: If summarization fails.
        """
        if not text.strip():
            self.logger.warning("Attempted to summarize empty text.")
            return ""

        provider_defaults = self.config.default_llm_completion_config.get(self.llm_manager.provider, {})
        
        final_max_tokens = max_tokens if max_tokens is not None else provider_defaults.get("max_tokens", 200)
        final_temperature = temperature if temperature is not None else provider_defaults.get("temperature", 0.5)
        
        # Ensure max_tokens is an int if provided as string from config
        if isinstance(final_max_tokens, str) and final_max_tokens.isdigit():
            final_max_tokens = int(final_max_tokens)
        elif not isinstance(final_max_tokens, int):
            final_max_tokens = 200 # Fallback default

        system_prompt = "You are an expert academic assistant specializing in concise and informative text summarization."
        user_prompt = f"Please summarize the following text in a few sentences: \n\n{{text_to_summarize}}"

        if prompt_template:
            try:
                user_prompt = prompt_template.format(text_to_summarize=text, context=context or "")
            except KeyError as e:
                raise SummarizerError(f"Prompt template missing required key: {e}. Template: '{prompt_template}'")
        else:
            if summary_type == "key_findings":
                system_prompt = "You are an expert research analyst. Your task is to extract and summarize the key findings from the provided text."
                user_prompt = f"Identify and summarize the key findings from this text in 2-4 bullet points or a short paragraph:\n\n{{text_to_summarize}}"
            elif summary_type == "abstract_enhancement":
                system_prompt = "You are an AI assistant that refines and enhances academic abstracts to be more impactful and clear, focusing on core contributions and significance."
                user_prompt = f"Enhance the following abstract. Make it concise (2-3 sentences), clear, and highlight its core contributions and significance. Abstract:\n\n{{text_to_summarize}}"
            # Default/general prompt is already set
        
        # Fill the text_to_summarize placeholder if not using a custom template that already did
        if "{text_to_summarize}" in user_prompt:
            user_prompt = user_prompt.format(text_to_summarize=text)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        self.logger.debug(f"Requesting summary. Type: '{summary_type}'. Max tokens: {final_max_tokens}. Temp: {final_temperature}.")
        self.logger.debug(f"System Prompt: {system_prompt}")
        self.logger.debug(f"User Prompt: {user_prompt[:200]}...") # Log beginning of prompt

        try:
            response = await self.llm_manager.generate_chat_completion(
                messages=messages,
                max_tokens=final_max_tokens,
                temperature=final_temperature
            )

            if response and response.get("choices") and response["choices"][0].get("message"):
                summary = response["choices"][0]["message"].get("content", "").strip()
                if not summary:
                    self.logger.warning("LLM returned an empty summary.")
                    return "Summary generation resulted in empty content."
                self.logger.info(f"Successfully generated summary. Length: {len(summary)} chars.")
                return summary
            else:
                self.logger.error(f"Failed to generate summary. Invalid LLM response format: {response}")
                raise SummarizerError(f"Invalid LLM response format during summarization.")
        except LLMManagerError as e:
            self.logger.error(f"LLMManager error during summarization: {e}", exc_info=True)
            raise SummarizerError(f"LLM interaction failed: {e}") from e
        except Exception as e:
            self.logger.error(f"Unexpected error during summarization: {e}", exc_info=True)
            raise SummarizerError(f"An unexpected error occurred: {e}") from e

if __name__ == '__main__':
    # Test for Summarizer
    import asyncio

    async def test_summarizer():
        print("Testing Summarizer...")
        # Requires a Config instance and an LLMManager (mocked for this test)
        test_config = Config(llm_provider="mock") 
        llm_manager = LLMManager(config=test_config)
        summarizer = Summarizer(llm_manager=llm_manager, config=test_config)

        sample_text = (
            "Large language models (LLMs) have demonstrated remarkable capabilities in natural language understanding and generation. "
            "Their applications span various domains, including machine translation, text summarization, and question answering. "
            "Despite their success, challenges remain in areas such as factual accuracy, bias mitigation, and computational efficiency. "
            "Future research aims to address these limitations and explore novel architectures for more robust and versatile LLMs."
        )

        print(f"\nOriginal Text:\n{sample_text}")

        # Test general summary
        print("\n--- Testing General Summary ---")
        general_summary = await summarizer.summarize_text(sample_text, summary_type="general")
        print(f"General Summary: {general_summary}")

        # Test key findings summary
        print("\n--- Testing Key Findings Summary ---")
        key_findings_summary = await summarizer.summarize_text(sample_text, summary_type="key_findings", max_tokens=100)
        print(f"Key Findings Summary: {key_findings_summary}")
        
        # Test abstract enhancement summary
        print("\n--- Testing Abstract Enhancement Summary ---")
        abstract_enhancement_summary = await summarizer.summarize_text(sample_text, summary_type="abstract_enhancement", temperature=0.3)
        print(f"Abstract Enhancement Summary: {abstract_enhancement_summary}")

        # Test with custom prompt
        print("\n--- Testing Custom Prompt Summary ---")
        custom_prompt = "Extract the main challenge mentioned in the following text: {text_to_summarize}"
        custom_summary = await summarizer.summarize_text(sample_text, prompt_template=custom_prompt)
        print(f"Custom Prompt Summary (Challenge): {custom_summary}")
        
        # Test with context
        print("\n--- Testing Summary with Context ---")
        contextual_prompt = "Considering the research topic '{context}', summarize the relevance of this text: {text_to_summarize}"
        contextual_summary = await summarizer.summarize_text(
            sample_text, 
            prompt_template=contextual_prompt, 
            context="Future of AI models"
        )
        print(f"Contextual Summary (Relevance to 'Future of AI models'): {contextual_summary}")

        # Test empty text
        print("\n--- Testing Empty Text ---")
        empty_summary = await summarizer.summarize_text(" ")
        print(f"Summary of empty text: '{empty_summary}' (should be empty)")

        # Test potential error (e.g., if LLMManager was misconfigured, though mock prevents this)
        # print("\n--- Testing Error Scenario (Illustrative) ---")
        # try:
        #     error_config = Config(llm_provider="openai", openai_api_key="INVALID_KEY_FOR_TEST") # Force an error if not using mock
        #     error_llm_manager = LLMManager(config=error_config)
        #     error_summarizer = Summarizer(llm_manager=error_llm_manager, config=error_config)
        #     await error_summarizer.summarize_text("test")
        # except SummarizerError as e:
        #     print(f"Caught expected error: {e}")
        # except LLMManagerError as le: # If init itself fails for LLMManager
        #      print(f"Caught expected LLMManager init error: {le}")

    asyncio.run(test_summarizer()) 