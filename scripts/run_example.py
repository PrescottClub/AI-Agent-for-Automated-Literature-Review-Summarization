#!/usr/bin/env python3
"""Example script demonstrating how to use the Literature Review Agent."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lit_review_agent.agent import LiteratureAgent
from lit_review_agent.utils.config import Config


async def run_example():
    """Run an example literature review."""
    
    print("🔬 Literature Review Agent - Example")
    print("=" * 50)
    
    try:
        # Initialize the agent
        print("📥 Initializing agent...")
        config = Config()
        agent = LiteratureAgent(config)
        
        # Example topic
        topic = "machine learning for drug discovery"
        print(f"📚 Topic: {topic}")
        print(f"📄 Max papers: 10")
        
        # Conduct literature review
        print("\n🔍 Conducting literature review...")
        results = await agent.conduct_literature_review(
            research_topic=topic,
            max_papers=10,
            include_full_text=False  # Set to True to download PDFs (slower)
        )
        
        if "error" in results:
            print(f"❌ Error: {results['error']}")
            return
        
        # Display results
        print(f"\n📊 Results Summary:")
        print(f"   Papers found: {len(results.get('papers', []))}")
        
        # Executive Summary
        if results.get("summary"):
            print(f"\n📋 Executive Summary:")
            print(f"   {results['summary'][:200]}...")
        
        # Key Insights
        if results.get("key_insights"):
            print(f"\n💡 Key Insights:")
            for i, insight in enumerate(results["key_insights"][:3], 1):
                print(f"   {i}. {insight}")
        
        # Research Gaps
        if results.get("research_gaps"):
            print(f"\n🔍 Research Gaps:")
            for i, gap in enumerate(results["research_gaps"][:2], 1):
                print(f"   {i}. {gap}")
        
        # Export results
        print(f"\n💾 Exporting results...")
        success = await agent.export_results(
            results,
            output_format="markdown",
            output_file="example_review.md"
        )
        
        if success:
            print(f"   ✅ Results exported to example_review.md")
        else:
            print(f"   ❌ Failed to export results")
        
        # Example similarity search
        print(f"\n🔍 Testing similarity search...")
        similar_papers = await agent.search_similar_papers(
            query="drug discovery artificial intelligence",
            n_results=5
        )
        
        print(f"   Found {len(similar_papers)} similar papers")
        for i, paper in enumerate(similar_papers[:3], 1):
            title = paper.get("metadata", {}).get("title", "Unknown")
            distance = paper.get("distance", 0)
            print(f"   {i}. {title[:60]}... (distance: {distance:.3f})")
        
        # Agent statistics
        print(f"\n📈 Agent Statistics:")
        stats = agent.get_statistics()
        print(f"   Vector store items: {stats.get('vector_store', {}).get('total_items', 0)}")
        print(f"   LLM requests: {stats.get('llm_requests', 0)}")
        
        print(f"\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running example: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function."""
    
    # Check if configuration is set up
    try:
        config = Config()
        if not config.openai_api_key:
            print("❌ OpenAI API key not configured!")
            print("Please set up your configuration using:")
            print("   python -m lit_review_agent.cli setup")
            print("Or set the OPENAI_API_KEY environment variable.")
            return
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please run setup: python -m lit_review_agent.cli setup")
        return
    
    # Run the example
    asyncio.run(run_example())


if __name__ == "__main__":
    main() 