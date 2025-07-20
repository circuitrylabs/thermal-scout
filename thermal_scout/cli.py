"""
Thermal Scout CLI - A thermal-aware Hugging Face model search tool
"""

import typer
from rich.console import Console

from .search import thermal_search

app = typer.Typer(
    name="thermal-scout",
    help="A thermal-aware Hugging Face model search CLI",
    no_args_is_help=True,
)
console = Console()


def get_thermal_indicator(thermal_cost: str) -> str:
    """Convert thermal cost to text representation"""
    return thermal_cost


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query for models"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results to show"),
    model_type: str | None = typer.Option(
        None, "--type", "-t", help="Filter by model type/task"
    ),
    no_thermal: bool = typer.Option(
        False, "--no-thermal", help="Disable thermal-aware sorting"
    ),
):
    """
    Search Hugging Face Hub for models with thermal awareness

    Examples:
        thermal-scout search "sentiment analysis" --limit 5
        thermal-scout search "text generation" --type text-generation
        thermal-scout search "llama" --no-thermal
    """
    console.print(f"\nSearching for: {query}")

    # Perform search
    results = thermal_search(
        query=query, limit=limit, model_type=model_type, thermal_aware=not no_thermal
    )

    if not results:
        console.print("[red]No models found matching your search.[/red]")
        return

    # Simple text output for terminal compatibility
    console.print(f"\nFound {len(results)} models\n")
    
    # Header
    console.print(
        f"{'Model ID':<40} {'Thermal':<12} {'Downloads':>10} {'Likes':>8} {'Type':<15}"
    )
    console.print("-" * 85)
    
    # Results
    for model in results:
        thermal_text = model.get("thermal_cost", "Unknown")
        
        console.print(
            f"{model['modelId']:<40} "
            f"{thermal_text:<12} "
            f"{model.get('downloads', 0):>10,} "
            f"{model.get('likes', 0):>8,} "
            f"{model.get('pipeline_tag', 'n/a') or 'n/a':<15}"
        )

    if not no_thermal:
        console.print("\nResults sorted by thermal efficiency (Low -> High)")


@app.command()
def about():
    """Show information about Thermal Scout"""
    console.print("\nThermal Scout\n")
    console.print("A thermal-aware model search tool for Hugging Face Hub.\n")
    console.print("Features:")
    console.print("- Search models with thermal cost awareness")
    console.print("- Sort results by computational efficiency")
    console.print("- Filter by model type/task\n")
    console.print("Thermal Cost Indicators:")
    console.print("  Low    - Small, efficient models (<1B params)")
    console.print("  Medium - Moderate size models (1-3B params)")
    console.print("  High   - Large models requiring significant compute (3B+ params)\n")
    console.print("Made by CircuitryLabs\n")


if __name__ == "__main__":
    app()
