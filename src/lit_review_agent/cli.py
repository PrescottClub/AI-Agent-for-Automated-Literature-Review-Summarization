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

from .agent import LiteratureAgent
from .utils.config import Config
from .retrieval.base_retriever import LiteratureItem

app = typer.Typer(
    name="lit-review",
    help="AI Agent for Automated Literature Review & Summarization"
)
console = Console()


@app.command()
def review(
    topic: str = typer.Argument(..., help="Research topic to review"),
    max_papers: int = typer.Option(20, "--max-papers", "-n", help="Maximum number of papers to retrieve"),
    full_text: bool = typer.Option(False, "--full-text", "-f", help="Extract full text from PDFs"),
    output_format: str = typer.Option("markdown", "--format", "-o", help="Output format (markdown, json, txt)"),
    output_file: Optional[str] = typer.Option(None, "--output", help="Output file path"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Configuration file path")
):
    """Conduct a comprehensive literature review on a research topic."""
    
    console.print(Panel.fit(
        f"🔬 Literature Review Agent\n\n"
        f"Topic: {topic}\n"
        f"Max Papers: {max_papers}\n"
        f"Full Text: {'Yes' if full_text else 'No'}\n"
        f"Output Format: {output_format}",
        title="Starting Literature Review",
        border_style="blue"
    ))
    
    try:
        # Load configuration
        if config_file and Path(config_file).exists():
            # Load from custom config file
            import os
            os.environ["CONFIG_FILE"] = config_file
        
        config = Config()
        
        # Initialize agent
        agent = LiteratureAgent(config)
        
        # Run literature review
        with console.status("[bold blue]Conducting literature review..."):
            results = asyncio.run(
                agent.conduct_literature_review(
                    research_topic=topic,
                    max_papers=max_papers,
                    include_full_text=full_text
                )
            )
        
        if "error" in results:
            console.print(f"[red]Error: {results['error']}[/red]")
            raise typer.Exit(1)
        
        # Display results summary
        display_results_summary(results)
        
        # Export results
        if asyncio.run(agent.export_results(results, output_format, output_file)):
            console.print(f"[green]✅ Results exported successfully![/green]")
        else:
            console.print(f"[red]❌ Failed to export results[/red]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    max_results: int = typer.Option(10, "--max-results", "-n", help="Maximum number of results"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Configuration file path")
):
    """Search for similar papers in the vector store."""
    
    console.print(f"🔍 Searching for papers similar to: [bold]{query}[/bold]")
    
    try:
        # Load configuration
        if config_file and Path(config_file).exists():
            import os
            os.environ["CONFIG_FILE"] = config_file
        
        config = Config()
        agent = LiteratureAgent(config)
        
        # Search for similar papers
        with console.status("[bold blue]Searching vector store..."):
            results = asyncio.run(
                agent.search_similar_papers(query, max_results)
            )
        
        if not results:
            console.print("[yellow]No similar papers found in the vector store.[/yellow]")
            return
        
        # Display results
        display_search_results(results)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def stats(
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Configuration file path")
):
    """Display agent statistics."""
    
    try:
        # Load configuration
        if config_file and Path(config_file).exists():
            import os
            os.environ["CONFIG_FILE"] = config_file
        
        config = Config()
        agent = LiteratureAgent(config)
        
        # Get statistics
        stats = agent.get_statistics()
        
        # Display statistics
        display_statistics(stats)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def config_info(
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Configuration file path")
):
    """Display current configuration."""
    
    try:
        # Load configuration
        if config_file and Path(config_file).exists():
            import os
            os.environ["CONFIG_FILE"] = config_file
        
        config = Config()
        
        # Display configuration
        display_configuration(config)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def setup():
    """Interactive setup for configuration."""
    
    console.print(Panel.fit(
        "🚀 Literature Review Agent Setup\n\n"
        "This will help you configure the agent with your API keys and preferences.",
        title="Setup",
        border_style="green"
    ))
    
    # Check if .env file exists
    env_file = Path(".env")
    config_env = Path("config/.env")
    
    if env_file.exists() or config_env.exists():
        overwrite = typer.confirm("Configuration file already exists. Overwrite?")
        if not overwrite:
            console.print("[yellow]Setup cancelled.[/yellow]")
            return
    
    # Collect configuration
    config_data = {}
    
    # OpenAI API Key
    console.print("\n[bold blue]OpenAI Configuration[/bold blue]")
    openai_key = typer.prompt("OpenAI API Key (leave blank if using another provider)", default="", show_default=False)
    if openai_key:
        config_data["OPENAI_API_KEY"] = openai_key
    
    openai_model = typer.prompt("OpenAI Model (if using OpenAI)", default="gpt-4-turbo-preview", type=str)
    if openai_key: # Only ask for model if key is provided
        config_data["OPENAI_MODEL"] = openai_model
    openai_api_base = typer.prompt("OpenAI API Base URL (optional, for custom OpenAI-compatible APIs)", default="", show_default=False)
    if openai_api_base:
        config_data["OPENAI_API_BASE"] = openai_api_base

    # DeepSeek API Key
    console.print("\n[bold magenta]DeepSeek Configuration[/bold magenta]")
    deepseek_key = typer.prompt("DeepSeek API Key (leave blank if not using)", default="", show_default=False)
    if deepseek_key:
        config_data["DEEPSEEK_API_KEY"] = deepseek_key

    deepseek_model = typer.prompt("DeepSeek Model (if using DeepSeek)", default="deepseek-chat", type=str)
    if deepseek_key:
        config_data["DEEPSEEK_MODEL"] = deepseek_model
    deepseek_api_base = typer.prompt("DeepSeek API Base URL (optional)", default="https://api.deepseek.com", show_default=True)
    if deepseek_key: # Only save if Deepseek is being configured
      config_data["DEEPSEEK_API_BASE"] = deepseek_api_base

    # LLM Provider Choice
    console.print("\n[bold green]LLM Provider Choice[/bold green]")
    llm_provider_choices = ["openai", "deepseek"]
    default_provider = "openai"
    if deepseek_key and not openai_key:
        default_provider = "deepseek"
    elif openai_key and not deepseek_key:
        default_provider = "openai"
    
    llm_provider = typer.prompt(
        f"Choose LLM Provider ({', '.join(llm_provider_choices)})", 
        default=default_provider, 
        type=str
    )
    if llm_provider not in llm_provider_choices:
        console.print(f"[red]Invalid provider. Defaulting to '{default_provider}'.[/red]")
        llm_provider = default_provider
    config_data["LLM_PROVIDER"] = llm_provider

    # Other settings
    console.print("\n[bold blue]Application Settings[/bold blue]")
    max_papers = typer.prompt("Default max papers", default=100, type=int)
    config_data["ARXIV_MAX_RESULTS"] = str(max_papers)
    
    log_level = typer.prompt("Log level", default="INFO", type=str)
    config_data["LOG_LEVEL"] = log_level
    
    # Write configuration
    config_content = "\n".join([f"{key}={value}" for key, value in config_data.items()])
    
    try:
        # Create config directory if it doesn't exist
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        
        # Write to config/.env
        with open(config_dir / ".env", "w") as f:
            f.write(config_content)
        
        console.print(f"[green]✅ Configuration saved to {config_dir / '.env'}[/green]")
        console.print("\n[yellow]You can now run literature reviews![/yellow]")
        console.print("Example: [bold]lit-review review 'machine learning in healthcare'[/bold]")
        
    except Exception as e:
        console.print(f"[red]Error saving configuration: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def generate_report(
    topic: str = typer.Argument(..., help="Research topic for the report"),
    input_file: str = typer.Option(..., "--input", "-i", help="Path to JSON file containing literature items from a previous review"),
    output_format: str = typer.Option("markdown", "--format", "-f", help="Output format for the report (markdown, html, latex)"),
    output_file: str = typer.Option(..., "--output", "-o", help="File path to save the generated report"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Configuration file path")
):
    """Generate a comprehensive report from a list of literature items."""
    console.print(Panel.fit(
        f"📚 Generating Literature Report\n\n"
        f"Topic: {topic}\n"
        f"Input File: {input_file}\n"
        f"Output Format: {output_format}\n"
        f"Output File: {output_file}",
        title="Report Generation",
        border_style="green"
    ))

    try:
        # Load configuration
        if config_file and Path(config_file).exists():
            import os
            os.environ["CONFIG_FILE"] = config_file
        
        config_instance = Config()
        agent = LiteratureAgent(config_instance)

        # Load literature items from input file
        console.print(f"[cyan]Loading literature items from {input_file}...[/cyan]")
        if not Path(input_file).exists():
            console.print(f"[red]Error: Input file '{input_file}' not found.[/red]")
            raise typer.Exit(1)
        
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Assuming the papers are stored under a key like 'papers' 
            # and need to be converted to LiteratureItem objects
            paper_dicts = data.get('papers', []) 
            if not paper_dicts and isinstance(data, list): # if the root is a list of papers
                paper_dicts = data
            elif not paper_dicts and isinstance(data.get('results', {}).get('papers'), list):
                 paper_dicts = data.get('results', {}).get('papers', [])

        if not paper_dicts:
            console.print(f"[red]Error: No papers found in input file '{input_file}'. Expected a JSON list of papers or a JSON object with a 'papers' key.[/red]")
            raise typer.Exit(1)

        papers = []
        for p_dict in paper_dicts:
            # Minimal conversion, assuming p_dict has the necessary fields for LiteratureItem
            # This might need adjustment based on the actual structure of review output
            item = LiteratureItem(
                id=p_dict.get('id', p_dict.get('entry_id', 'unknown')),
                title=p_dict.get('title', 'N/A'),
                authors=p_dict.get('authors', []),
                abstract=p_dict.get('abstract', p_dict.get('summary')),
                publication_date=datetime.fromisoformat(p_dict['publication_date']) if p_dict.get('publication_date') else None,
                url=p_dict.get('url', p_dict.get('pdf_url')),
                venue=p_dict.get('journal', p_dict.get('journal_ref')),
                keywords=p_dict.get('keywords', []), # Ensure keywords are present
                categories=p_dict.get('categories', []) # Ensure categories are present
            )
            papers.append(item)
        
        console.print(f"[cyan]Loaded {len(papers)} literature items.[/cyan]")

        # Generate report
        with console.status("[bold green]Generating report..."):
            report_data = asyncio.run(
                agent.generate_full_report(
                    papers=papers,
                    topic=topic,
                    output_format=output_format
                )
            )

        if "error" in report_data:
            console.print(f"[red]Error generating report: {report_data['error']}[/red]")
            raise typer.Exit(1)

        # Save report to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_data["content"])
        
        console.print(f"[green]✅ Report generated and saved to {output_path}[/green]")

    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {str(e)}[/red]")
        import traceback
        console.print(traceback.format_exc())
        raise typer.Exit(1)


def display_results_summary(results: dict):
    """Display a summary of literature review results."""
    
    console.print("\n" + "="*80)
    console.print(f"[bold green]📊 Literature Review Results[/bold green]")
    console.print("="*80)
    
    # Basic info
    console.print(f"[bold]Topic:[/bold] {results.get('topic', 'Unknown')}")
    console.print(f"[bold]Papers Found:[/bold] {len(results.get('papers', []))}")
    
    # Statistics
    if results.get("statistics"):
        stats = results["statistics"]
        console.print(f"[bold]Date Range:[/bold] {stats.get('date_range', {}).get('earliest', 'Unknown')} - {stats.get('date_range', {}).get('latest', 'Unknown')}")
    
    # Executive Summary
    if results.get("summary"):
        console.print(f"\n[bold blue]📋 Executive Summary[/bold blue]")
        console.print(Panel(results["summary"], border_style="blue"))
    
    # Key Insights
    if results.get("key_insights"):
        console.print(f"\n[bold green]💡 Key Insights[/bold green]")
        for i, insight in enumerate(results["key_insights"][:5], 1):
            console.print(f"{i}. {insight}")
    
    # Research Gaps
    if results.get("research_gaps"):
        console.print(f"\n[bold yellow]🔍 Research Gaps[/bold yellow]")
        for i, gap in enumerate(results["research_gaps"][:3], 1):
            console.print(f"{i}. {gap}")
    
    # Top Categories
    if results.get("statistics", {}).get("top_categories"):
        console.print(f"\n[bold magenta]📈 Top Categories[/bold magenta]")
        for category, count in results["statistics"]["top_categories"][:5]:
            console.print(f"• {category}: {count} papers")


def display_search_results(results: list):
    """Display search results in a table."""
    
    table = Table(title="Similar Papers")
    table.add_column("Rank", style="cyan", width=6)
    table.add_column("Title", style="green")
    table.add_column("Distance", style="yellow", width=10)
    table.add_column("Source", style="blue", width=10)
    
    for i, result in enumerate(results, 1):
        metadata = result.get("metadata", {})
        title = metadata.get("title", "Unknown Title")
        distance = f"{result.get('distance', 0):.3f}" if result.get('distance') else "N/A"
        source = metadata.get("source", "Unknown")
        
        # Truncate long titles
        if len(title) > 60:
            title = title[:57] + "..."
        
        table.add_row(str(i), title, distance, source)
    
    console.print(table)


def display_statistics(stats: dict):
    """Display agent statistics."""
    
    console.print(Panel.fit(
        f"📊 Agent Statistics\n\n"
        f"Vector Store Items: {stats.get('vector_store', {}).get('total_items', 0)}\n"
        f"LLM Requests Made: {stats.get('llm_requests', 0)}\n"
        f"Current Model: {stats.get('config', {}).get('model', 'Unknown')}\n"
        f"Max Papers Setting: {stats.get('config', {}).get('max_papers', 'Unknown')}",
        title="Statistics",
        border_style="cyan"
    ))


def display_configuration(config: Config):
    """Display current configuration."""
    
    # Create a table for configuration
    table = Table(title="Current Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    # Add configuration items (hide sensitive data)
    config_items = [
        ("OpenAI Model", config.openai_model),
        ("Max Tokens/Request", str(config.max_tokens_per_request)),
        ("Max Requests/Minute", str(config.max_requests_per_minute)),
        ("ArXiv Max Results", str(config.arxiv_max_results)),
        ("Log Level", config.log_level),
        ("Output Directory", config.output_dir),
        ("Vector DB Directory", config.chroma_persist_directory),
        ("API Key", "***" + config.openai_api_key[-4:] if len(config.openai_api_key) > 4 else "Not Set"),
    ]
    
    for setting, value in config_items:
        table.add_row(setting, str(value))
    
    console.print(table)


if __name__ == "__main__":
    app() 