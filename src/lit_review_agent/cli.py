"""Command Line Interface for the Literature Review Agent."""

import asyncio
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.prompt import Prompt

from .agent import LiteratureAgent
from .utils.config import Config
from .utils.logger import get_logger, setup_logger
from .__init__ import __version__ as agent_version

# Setup initial logger for CLI specific messages before agent might reconfigure
setup_logger(log_level="INFO")  # Default to INFO for CLI startup
logger = get_logger(__name__)

app = typer.Typer(
    name="lit-review-agent",
    help="🤖 AI Agent for Automated Literature Review & Summarization",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", "-v", help="Show application version and exit."
    ),
):
    """
    AI Literature Review Agent CLI
    """
    if version:
        console.print(
            f"[bold green]AI Literature Review Agent[/bold green] version: [yellow]{agent_version}[/yellow]"
        )
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        # console.print("Welcome to the AI Literature Review Agent! Use --help for options.")
        pass  # Typer will show help by default if no_args_is_help=True


@app.command()
def setup():
    """
    Guides you through the initial setup and configuration of the agent.
    """
    console.print("[bold cyan]🚀 AI Literature Review Agent Setup Wizard[/bold cyan]")
    console.print(
        "This wizard will help you configure your API keys and preferences.\n"
    )

    try:
        config = Config()

        # Check current configuration
        console.print("[bold yellow]Current Configuration Status:[/bold yellow]")

        # Check LLM Provider
        console.print(f"LLM Provider: [cyan]{config.llm_provider}[/cyan]")

        # Check API Keys
        if config.llm_provider == "deepseek":
            if config.deepseek_api_key:
                console.print("✅ DeepSeek API Key: Configured")
            else:
                console.print("❌ DeepSeek API Key: Not configured")
                console.print(
                    "   Get your key from: https://platform.deepseek.com/api_keys"
                )

        if config.openai_api_key:
            console.print("✅ OpenAI API Key: Configured (for embeddings)")
        else:
            console.print("❌ OpenAI API Key: Not configured (needed for embeddings)")
            console.print("   Get your key from: https://platform.openai.com/api-keys")

        if config.semantic_scholar_api_key:
            console.print("✅ Semantic Scholar API Key: Configured")
        else:
            console.print("⚠️  Semantic Scholar API Key: Not configured (optional)")
            console.print(
                "   Get your key from: https://www.semanticscholar.org/product/api"
            )

        console.print(f"\n[bold green]Setup Instructions:[/bold green]")
        console.print("1. Copy config/config.example.env to .env")
        console.print("2. Edit .env file with your API keys")
        console.print("3. Install spaCy model: python -m spacy download en_core_web_sm")
        console.print(
            "4. Run: python -m src.lit_review_agent.cli config-info to verify"
        )

    except Exception as e:
        logger.error(f"Error during setup: {e}", exc_info=True)
        console.print(f"[bold red]Setup error:[/bold red] {e}")


@app.command()
def config_info():
    """
    Displays the current configuration of the agent.
    """
    console.print("[bold cyan]📋 Current Agent Configuration:[/bold cyan]")
    try:
        config = Config()
        table = Table(
            title="Configuration Details", show_header=True, header_style="bold magenta"
        )
        table.add_column("Setting", style="dim", width=30)
        table.add_column("Value")

        config_dict = config.model_dump()
        for key, value in config_dict.items():
            display_value = str(value)
            if "api_key" in key and value:  # Mask API keys
                display_value = "********" + str(value)[-4:]
            if value is None:
                display_value = "[italic gray]Not set[/italic gray]"
            table.add_row(key, display_value)

        console.print(table)
        console.print(
            f"\nConfig loaded from: [yellow]{config.env_file_location()}[/yellow]"
        )

    except Exception as e:
        logger.error(f"Error loading or displaying configuration: {e}", exc_info=True)
        console.print(f"[bold red]Error loading configuration:[/bold red] {e}")


@app.command()
def review(
    ctx: typer.Context,
    research_topic: str = typer.Argument(..., help="The research topic to review."),
    max_papers: int = typer.Option(
        10, "--max-papers", "-n", help="Maximum number of papers to retrieve."
    ),
    sources: Optional[str] = typer.Option(
        None,
        "--sources",
        "-s",
        help="Comma-separated list of sources (e.g., arxiv,semantic_scholar). Defaults to config.",
    ),
    retrieve_full_text: bool = typer.Option(
        False, "--full-text", "-f", help="Attempt to retrieve full text of papers."
    ),
    year_start: Optional[int] = typer.Option(
        None,
        "--year-start",
        "--ys",
        help="Filter papers published FROM this year (inclusive).",
    ),
    year_end: Optional[int] = typer.Option(
        None,
        "--year-end",
        "--ye",
        help="Filter papers published UP TO this year (inclusive).",
    ),
    output_format: str = typer.Option(
        "json", "--format", help="Output format for the results (json, markdown)."
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o", help="File path to save the review results."
    ),
):
    """
    Conducts a literature review for a specified topic.
    """
    console.print(
        f"[bold cyan]📚 Starting Literature Review for:[/bold cyan] '{research_topic}'"
    )
    logger.info(f"CLI review command called for topic: {research_topic}")

    try:
        # Initialize agent
        agent_config = Config()
        agent = LiteratureAgent(config=agent_config)

        source_list = (
            sources.split(",") if sources else agent_config.default_retrieval_sources
        )

        console.print(
            f"Retrieving up to {max_papers} papers from sources: {source_list}..."
        )

        # Run the literature review
        review_results = asyncio.run(
            agent.conduct_literature_review(
                research_topic=research_topic,
                max_papers=max_papers,
                sources=source_list,
                retrieve_full_text=retrieve_full_text,
                year_start=year_start,
                year_end=year_end,
            )
        )

        console.print("\n[bold green]✅ Review Process Completed.[/bold green]")

        if review_results and review_results.get("papers"):
            console.print(
                f"Successfully processed [bold]{review_results['num_papers_processed']}[/bold] papers."
            )

            # Display results table
            table = Table(
                title=f"Retrieved Papers for '{research_topic}'", show_lines=True
            )
            table.add_column("Title", style="cyan", min_width=40, overflow="fold")
            table.add_column("Authors", style="green", min_width=20, overflow="fold")
            table.add_column("Published", style="magenta", width=12)
            table.add_column("Source", style="blue", width=10)

            for paper in review_results["papers"]:
                authors_str = ", ".join(paper.get("authors", []))
                table.add_row(
                    paper.get("title", "N/A"),
                    authors_str,
                    (
                        paper.get("published_date", "N/A")[:10]
                        if paper.get("published_date")
                        else "N/A"
                    ),
                    paper.get("source", "N/A"),
                )
            console.print(table)

            # Save results if output file specified
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                if output_format.lower() == "json":
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(review_results, f, indent=2, ensure_ascii=False)
                elif output_format.lower() == "markdown":
                    # Generate markdown report
                    report = asyncio.run(
                        agent.generate_full_report(
                            papers=review_results["papers"],
                            topic=research_topic,
                            output_format="markdown",
                        )
                    )
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(report.get("content", ""))

                console.print(f"Results saved to: [yellow]{output_path}[/yellow]")
        else:
            console.print("[yellow]No papers were processed or found.[/yellow]")

    except Exception as e:
        logger.error(f"Error during literature review command: {e}", exc_info=True)
        console.print(f"[bold red]An error occurred during the review:[/bold red] {e}")
        console.print("Check the logs for more details.")


@app.command()
def generate_report(
    title: str = typer.Argument(..., help="Title for the report"),
    input_file: str = typer.Option(
        ..., "--input", "-i", help="Input JSON file with review results"
    ),
    output_file: str = typer.Option(
        ..., "--output", "-o", help="Output file path for the report"
    ),
    format: str = typer.Option(
        "markdown", "--format", "-f", help="Report format (markdown, html, latex)"
    ),
):
    """
    Generate a comprehensive report from literature review results.
    """
    console.print(f"[bold cyan]📄 Generating Report:[/bold cyan] '{title}'")

    try:
        # Load input data
        input_path = Path(input_file)
        if not input_path.exists():
            console.print(
                f"[bold red]Error:[/bold red] Input file not found: {input_file}"
            )
            raise typer.Exit(1)

        with open(input_path, "r", encoding="utf-8") as f:
            review_data = json.load(f)

        # Initialize agent
        agent_config = Config()
        agent = LiteratureAgent(config=agent_config)

        # Generate report
        report = asyncio.run(
            agent.generate_full_report(
                papers=review_data.get("papers", []), topic=title, output_format=format
            )
        )

        # Save report
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report.get("content", ""))

        console.print(f"[bold green]✅ Report generated successfully![/bold green]")
        console.print(f"Report saved to: [yellow]{output_path}[/yellow]")

    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        console.print(f"[bold red]Error generating report:[/bold red] {e}")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query for the knowledge base"),
    n_results: int = typer.Option(
        10, "--results", "-n", help="Number of results to return"
    ),
):
    """
    Search the existing knowledge base for similar papers.
    """
    console.print(f"[bold cyan]🔍 Searching knowledge base for:[/bold cyan] '{query}'")

    try:
        # Initialize agent
        agent_config = Config()
        agent = LiteratureAgent(config=agent_config)

        # Search
        results = asyncio.run(agent.search_similar_papers(query, n_results))

        if results:
            console.print(
                f"[bold green]Found {len(results)} similar papers:[/bold green]"
            )

            table = Table(title="Search Results", show_lines=True)
            table.add_column("Title", style="cyan", min_width=40)
            table.add_column("Similarity", style="yellow", width=10)
            table.add_column("Authors", style="green", min_width=20)

            for result in results:
                table.add_row(
                    result.get("title", "N/A"),
                    f"{result.get('similarity', 0):.3f}",
                    ", ".join(result.get("authors", [])),
                )

            console.print(table)
        else:
            console.print(
                "[yellow]No similar papers found in the knowledge base.[/yellow]"
            )

    except Exception as e:
        logger.error(f"Error during search: {e}", exc_info=True)
        console.print(f"[bold red]Error during search:[/bold red] {e}")


@app.command()
def stats():
    """
    Display system statistics and status.
    """
    console.print("[bold cyan]📊 System Statistics[/bold cyan]")

    try:
        # Initialize agent
        agent_config = Config()
        agent = LiteratureAgent(config=agent_config)

        # Get statistics
        stats = agent.get_statistics()

        table = Table(
            title="Agent Statistics", show_header=True, header_style="bold magenta"
        )
        table.add_column("Metric", style="dim", width=30)
        table.add_column("Value")

        for key, value in stats.items():
            table.add_row(key.replace("_", " ").title(), str(value))

        console.print(table)

    except Exception as e:
        logger.error(f"Error getting statistics: {e}", exc_info=True)
        console.print(f"[bold red]Error getting statistics:[/bold red] {e}")


if __name__ == "__main__":
    # This allows running the CLI directly with `python -m src.lit_review_agent.cli`
    # or just `python src/lit_review_agent/cli.py`
    app()
