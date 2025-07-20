"""
Thermal Scout CLI - A thermal-aware Hugging Face model search tool

Created with ❤️ by Claude and Tyler
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from .search import thermal_search

app = typer.Typer(
    name="thermal-scout",
    help="🔥 A thermal-aware Hugging Face model search CLI",
    no_args_is_help=True,
)
console = Console()


def get_thermal_emoji(thermal_cost: str) -> str:
    """Convert thermal cost to emoji representation"""
    return {
        "Low": "🟢",
        "Medium": "🟡", 
        "High": "🔴"
    }.get(thermal_cost, "⚪")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query for models"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results to show"),
    model_type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by model type/task"),
    no_thermal: bool = typer.Option(False, "--no-thermal", help="Disable thermal-aware sorting"),
):
    """
    Search Hugging Face Hub for models with thermal awareness
    
    Examples:
        thermal-scout search "sentiment analysis" --limit 5
        thermal-scout search "text generation" --type text-generation
        thermal-scout search "llama" --no-thermal
    """
    console.print(f"\n🔍 Searching for: [bold cyan]{query}[/bold cyan]\n")
    
    # Perform search
    results = thermal_search(
        query=query,
        limit=limit,
        model_type=model_type,
        thermal_aware=not no_thermal
    )
    
    if not results:
        console.print("[red]No models found matching your search.[/red]")
        return
    
    # Create results table
    table = Table(
        title=f"Found {len(results)} models",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Model ID", style="cyan", no_wrap=True)
    table.add_column("Thermal", justify="center")
    table.add_column("Downloads", justify="right")
    table.add_column("Likes", justify="right")
    table.add_column("Type", style="dim")
    
    for model in results:
        thermal_emoji = get_thermal_emoji(model.get("thermal_cost", "Unknown"))
        
        table.add_row(
            model["modelId"],
            f"{thermal_emoji} {model.get('thermal_cost', 'Unknown')}",
            f"{model.get('downloads', 0):,}",
            f"{model.get('likes', 0):,}",
            model.get("pipeline_tag", "n/a") or "n/a"
        )
    
    console.print(table)
    
    if not no_thermal:
        console.print("\n💡 [dim]Results sorted by thermal efficiency (🟢 Low → 🔴 High)[/dim]")


@app.command()
def about():
    """Show information about Thermal Scout"""
    about_text = """
[bold cyan]Thermal Scout[/bold cyan] 🔥
    
A thermal-aware model search tool for Hugging Face Hub.

[green]Features:[/green]
• Search models with thermal cost awareness
• Sort results by computational efficiency
• Filter by model type/task
• Beautiful CLI output with Rich

[yellow]Thermal Cost Indicators:[/yellow]
🟢 Low - Small, efficient models (<1B params)
🟡 Medium - Moderate size models (1-3B params)
🔴 High - Large models requiring significant compute (3B+ params)

Made with ❤️ by CircuitryLabs
    """
    
    console.print(Panel(about_text, box=box.ROUNDED, border_style="cyan"))


if __name__ == "__main__":
    app()