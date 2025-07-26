"""Display utilities using Rich library for enhanced CLI experience."""

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich.rule import Rule
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich.logging import RichHandler

# Global console instance for consistent formatting
# Fix Windows Unicode encoding issues
import platform
if platform.system() == 'Windows':
    console = Console(force_terminal=True, legacy_windows=False)
else:
    console = Console()


class LiteratureReviewDisplay:
    """Enhanced display utilities for literature review operations."""

    def __init__(self):
        self.console = console
        self.current_progress: Optional[Progress] = None
        self.current_task: Optional[TaskID] = None

    def print_header(self, title: str, subtitle: Optional[str] = None) -> None:
        """Print a styled header with title and optional subtitle."""
        # Create main title
        title_text = Text(title, style="bold magenta")

        if subtitle:
            subtitle_text = Text(subtitle, style="italic cyan")
            header_content = f"{title}\n{subtitle}"
        else:
            header_content = title

        # Create panel with border - use safe characters for Windows
        title_emoji = "[blue]🔬[/blue]" if platform.system() != 'Windows' else "[blue]*[/blue]"
        panel = Panel(
            Align.center(header_content),
            title=f"{title_emoji} Literature Review Agent",
            title_align="center",
            border_style="bright_blue",
            padding=(1, 2),
        )

        self.console.print()
        self.console.print(panel)
        self.console.print()

    def print_status(self, message: str, style: str = "bold green") -> None:
        """Print a status message with styling."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(
            f"[dim]{timestamp}[/dim] [bold blue]→[/bold blue] [{style}]{message}[/{style}]"
        )

    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        warning_icon = "⚠️" if platform.system() != 'Windows' else "!"
        self.console.print(f"[bold yellow]{warning_icon} Warning:[/bold yellow] {message}")

    def print_error(self, message: str) -> None:
        """Print an error message."""
        error_icon = "❌" if platform.system() != 'Windows' else "X"
        self.console.print(f"[bold red]{error_icon} Error:[/bold red] {message}")

    def print_success(self, message: str) -> None:
        """Print a success message."""
        success_icon = "✅" if platform.system() != 'Windows' else "+"
        self.console.print(f"[bold green]{success_icon} Success:[/bold green] {message}")

    def create_progress_bar(
        self, description: str, total: Optional[int] = None
    ) -> Progress:
        """Create and return a progress bar."""
        # Stop any existing progress first
        if self.current_progress:
            self.current_progress.stop()

        # Use simpler progress bar for Windows to avoid Unicode issues
        if platform.system() == 'Windows':
            self.current_progress = Progress(
                TextColumn("[progress.description]{task.description}"),
                TextColumn("-"),
                TimeElapsedColumn(),
                console=self.console,
                transient=False,
            )
        else:
            self.current_progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40),
                MofNCompleteColumn(),
                TextColumn("•"),
                TimeElapsedColumn(),
                TextColumn("•"),
                TimeRemainingColumn(),
                console=self.console,
                transient=False,
            )

        if total:
            self.current_task = self.current_progress.add_task(description, total=total)
        else:
            self.current_task = self.current_progress.add_task(description)

        return self.current_progress

    def update_progress(
        self, advance: int = 1, description: Optional[str] = None
    ) -> None:
        """Update the current progress bar."""
        if self.current_progress and self.current_task is not None:
            if description:
                self.current_progress.update(
                    self.current_task, description=description, advance=advance
                )
            else:
                self.current_progress.advance(self.current_task, advance)

    def finish_progress(self) -> None:
        """Finish and clean up the current progress bar."""
        if self.current_progress:
            self.current_progress.stop()
            self.current_progress = None
            self.current_task = None

    def create_papers_table(self, papers: List[Dict[str, Any]]) -> Table:
        """Create a formatted table for displaying papers."""
        table = Table(
            title="📚 Retrieved Literature",
            title_style="bold magenta",
            show_header=True,
            header_style="bold cyan",
            border_style="bright_blue",
            row_styles=["", "dim"],
        )

        # Add columns
        table.add_column("#", style="bold", width=3, justify="center")
        table.add_column("Title", style="bold", min_width=30, max_width=50)
        table.add_column("Authors", style="cyan", min_width=15, max_width=25)
        table.add_column("Source", style="green", width=10, justify="center")
        table.add_column("Date", style="yellow", width=10, justify="center")
        table.add_column("Full Text", style="magenta", width=8, justify="center")
        table.add_column("Keywords", style="blue", min_width=20, max_width=30)

        # Add rows
        for i, paper in enumerate(papers[:20], 1):  # Limit to first 20 for display
            # Truncate title if too long
            title = paper.get("title", "N/A")
            if len(title) > 47:
                title = title[:44] + "..."

            # Format authors
            authors = paper.get("authors", [])
            if authors:
                if len(authors) <= 2:
                    authors_str = ", ".join(authors)
                else:
                    authors_str = f"{authors[0]}, et al."
                if len(authors_str) > 22:
                    authors_str = authors_str[:19] + "..."
            else:
                authors_str = "N/A"

            # Format date
            pub_date = paper.get("published_date", "N/A")
            if pub_date and pub_date != "N/A":
                try:
                    if "T" in pub_date:  # ISO format
                        date_part = pub_date.split("T")[0]
                    else:
                        date_part = pub_date
                    # Just show year for space
                    date_display = (
                        date_part.split("-")[0] if "-" in date_part else date_part
                    )
                except:
                    date_display = "N/A"
            else:
                date_display = "N/A"

            # Format keywords
            keywords = paper.get("keywords", [])
            if keywords:
                keywords_str = ", ".join(keywords[:3])  # Show only first 3
                if len(keywords) > 3:
                    keywords_str += f" (+{len(keywords) - 3})"
                if len(keywords_str) > 27:
                    keywords_str = keywords_str[:24] + "..."
            else:
                keywords_str = "N/A"

            # Full text indicator
            full_text_icon = "✅" if paper.get("full_text_retrieved", False) else "❌"

            table.add_row(
                str(i),
                title,
                authors_str,
                paper.get("source", "N/A"),
                date_display,
                full_text_icon,
                keywords_str,
            )

        return table

    def create_summary_panel(self, results: Dict[str, Any]) -> Panel:
        """Create a summary panel for the review results."""
        topic = results.get("research_topic", "Unknown Topic")
        num_papers = results.get("num_papers_processed", 0)

        # Create summary content
        summary_lines = [
            f"🎯 [bold]Research Topic:[/bold] {topic}",
            f"📊 [bold]Papers Processed:[/bold] {num_papers}",
            f"🕒 [bold]Review Completed:[/bold] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ]

        # Add source breakdown if available
        if "processed_papers" in results:
            sources = {}
            full_text_count = 0
            for paper in results["processed_papers"]:
                source = paper.get("source", "Unknown")
                sources[source] = sources.get(source, 0) + 1
                if paper.get("full_text_retrieved", False):
                    full_text_count += 1

            summary_lines.append("")
            summary_lines.append("📈 [bold]Source Breakdown:[/bold]")
            for source, count in sources.items():
                summary_lines.append(f"   • {source}: {count} papers")

            summary_lines.append(
                f"📄 [bold]Full Text Retrieved:[/bold] {full_text_count}/{num_papers} papers"
            )

        content = "\n".join(summary_lines)

        return Panel(
            content,
            title="📋 Review Summary",
            title_align="left",
            border_style="green",
            padding=(1, 2),
        )

    def print_paper_details(self, paper: Dict[str, Any], index: int) -> None:
        """Print detailed information for a single paper."""
        title = paper.get("title", "N/A")
        authors = paper.get("authors", [])

        # Create header
        self.console.print(f"\n[bold bright_blue]Paper #{index}:[/bold bright_blue]")
        self.console.print(Rule(style="dim"))

        # Title
        self.console.print(f"[bold green]Title:[/bold green] {title}")

        # Authors
        if authors:
            authors_str = ", ".join(authors)
            self.console.print(f"[bold cyan]Authors:[/bold cyan] {authors_str}")

        # Publication info
        pub_date = paper.get("published_date")
        if pub_date:
            self.console.print(f"[bold yellow]Published:[/bold yellow] {pub_date}")

        source = paper.get("source")
        if source:
            self.console.print(f"[bold magenta]Source:[/bold magenta] {source}")

        # URLs
        url = paper.get("url")
        if url:
            self.console.print(f"[bold blue]URL:[/bold blue] {url}")

        pdf_url = paper.get("pdf_url")
        if pdf_url:
            self.console.print(f"[bold blue]PDF:[/bold blue] {pdf_url}")

        # Keywords
        keywords = paper.get("keywords", [])
        if keywords:
            keywords_str = ", ".join(keywords)
            self.console.print(f"[bold dim]Keywords:[/bold dim] {keywords_str}")

        # AI Summary
        ai_summary = paper.get("ai_enhanced_summary")
        if ai_summary and ai_summary != "No text content available for summarization.":
            self.console.print(
                f"\n[bold bright_green]AI Enhanced Summary:[/bold bright_green]"
            )
            # Create a panel for the summary
            summary_panel = Panel(ai_summary, border_style="green", padding=(0, 1))
            self.console.print(summary_panel)

        # Full text info
        if paper.get("full_text_retrieved"):
            snippet = paper.get("full_text_snippet")
            if snippet:
                self.console.print(
                    f"\n[bold dim]Full Text Preview:[/bold dim] {snippet}"
                )

    def print_markdown_report(self, markdown_content: str) -> None:
        """Print markdown content with rich formatting."""
        md = Markdown(markdown_content)
        self.console.print(md)

    def print_rule(self, title: Optional[str] = None, style: str = "dim") -> None:
        """Print a horizontal rule."""
        if title:
            self.console.print(Rule(title, style=style))
        else:
            self.console.print(Rule(style=style))


# Global display instance
display = LiteratureReviewDisplay()


# Convenience functions for direct use
def print_status(message: str, style: str = "bold green") -> None:
    """Print a status message."""
    try:
        display.print_status(message, style)
    except UnicodeEncodeError:
        # Fallback to plain print for Windows encoding issues
        print(f"[STATUS] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    try:
        display.print_warning(message)
    except UnicodeEncodeError:
        print(f"[WARNING] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    try:
        display.print_error(message)
    except UnicodeEncodeError:
        print(f"[ERROR] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    try:
        display.print_success(message)
    except UnicodeEncodeError:
        print(f"[SUCCESS] {message}")


def get_rich_handler() -> RichHandler:
    """Get a RichHandler for logging integration."""
    return RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )
