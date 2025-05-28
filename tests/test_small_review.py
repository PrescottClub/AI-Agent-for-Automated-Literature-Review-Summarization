"""Small-scale literature review test to verify enhanced CLI functionality."""

import asyncio
import sys
import os

# Add src to path
sys.path.append('src')

from src.lit_review_agent.agent import LiteratureAgent
from src.lit_review_agent.utils.config import Config
from src.lit_review_agent.utils.logger import setup_logger
from src.lit_review_agent.utils.display import display, print_status, print_success, print_error

async def test_small_review():
    """Test enhanced display with a small literature review."""
    
    try:
        # Setup
        display.print_header(
            "Literature Review Agent - Small Test",
            "Testing Enhanced CLI with Real Data"
        )
        
        print_status("Initializing agent with enhanced display...")
        
        custom_config = Config(
            arxiv_api_url="http://export.arxiv.org/api/", 
            spacy_model_name="en_core_web_sm",
            log_level="INFO", 
        )
        setup_logger(log_level=custom_config.log_level.upper(), use_rich=True)
        agent = LiteratureAgent(config=custom_config)
        
        print_success("Agent initialized successfully!")
        
        # Conduct small review
        topic = "attention mechanism"
        print_status(f"Starting small literature review for: '{topic}'")
        
        review_results = await agent.conduct_literature_review(
            topic,
            max_papers=3,  # Very small test
            retrieve_full_text=False,
            sources=['arxiv'],  # Only arxiv for speed
            year_start=2023,
            year_end=2024 
        )
        
        # Display final results
        if review_results.get("processed_papers"):
            display.print_rule("Sample Paper Details")
            
            # Show first paper in detail
            first_paper = review_results["processed_papers"][0]
            display.print_paper_details(first_paper, 1)
        
        display.print_rule("Test Complete")
        print_success("Small literature review test completed successfully!")
        
        return True
        
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(test_small_review())
        if result:
            print_success("All tests passed!")
        else:
            print_error("Some tests failed!")
    except Exception as e:
        print_error(f"Critical error: {e}")
        raise 