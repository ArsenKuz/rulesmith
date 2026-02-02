"""Main entry point for Rulesmith CLI."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cli.src.config import ConfigManager
from cli.src.detectors.stack_detector import StackDetector

app = typer.Typer(name="rulesmith", help="AI rule generator for coding assistants")
console = Console()


@app.command()
def init(
    project_path: Optional[Path] = typer.Argument(None, help="Path to project directory"),
    quick: bool = typer.Option(False, "--quick", help="Quick mode - skip guided questions"),
    guided: bool = typer.Option(False, "--guided", help="Guided mode - interactive setup"),
    stack: Optional[str] = typer.Option(None, "--stack", help="Override detected stack"),
    tools: Optional[str] = typer.Option(
        None, "--tools", help="Comma-separated list of tools (cursor,claude,copilot)"
    ),
):
    """Initialize a new Rulesmith project."""
    path = Path(project_path) if project_path else Path.cwd()

    console.print(Panel.fit(f"[bold blue]Initializing Rulesmith in {path}[/bold blue]"))

    # Detect stack
    detector = StackDetector(path)
    result = detector.detect()

    console.print(f"\n[bold]Detected Stack:[/bold] {result.primary}")
    console.print(f"[bold]Confidence:[/bold] {result.confidence:.0%}")

    if result.scores:
        console.print("\n[dim]All matches:[/dim]")
        for stack_id, score in sorted(result.scores.items(), key=lambda x: x[1], reverse=True):
            console.print(f"  {stack_id}: {score}")

    # Mode selection
    mode = "guided" if guided else "quick"
    if quick and guided:
        console.print("[yellow]Warning: both --quick and --guided set, using guided[/yellow]")
        mode = "guided"

    console.print(f"\n[bold]Mode:[/bold] {mode}")

    # Tools
    active_tools = tools.split(",") if tools else ["cursor", "claude", "copilot"]
    console.print(f"[bold]Tools:[/bold] {', '.join(active_tools)}")

    # TODO: Run generator
    console.print("\n[dim]Would run generator...[/dim]")
    console.print("[green]✓[/green] Done!")


@app.command()
def update(
    project_path: Optional[Path] = typer.Argument(None, help="Path to project directory"),
):
    """Update rules for an existing project."""
    path = Path(project_path) if project_path else Path.cwd()

    console.print(Panel.fit(f"[bold blue]Updating Rulesmith project in {path}[/bold blue]"))

    config_manager = ConfigManager(path)

    if not config_manager.exists():
        console.print("[red]✗ No Rulesmith configuration found. Run 'rulesmith init' first.[/red]")
        raise typer.Exit(1)

    config = config_manager.load()
    console.print(f"[green]✓[/green] Found configuration for: {config.project_name}")
    console.print(f"[green]✓[/green] Stack: {config.detected_stack}")
    console.print(f"[green]✓[/green] Tools: {', '.join(config.active_formatters)}")

    # TODO: Run generator
    console.print("\n[dim]Would run generator...[/dim]")
    console.print("[green]✓[/green] Done!")


@app.command()
def status(
    project_path: Optional[Path] = typer.Argument(None, help="Path to project directory"),
):
    """Show status of the current project."""
    path = Path(project_path) if project_path else Path.cwd()

    console.print(Panel.fit(f"[bold blue]Rulesmith Status: {path}[/bold blue]"))

    config_manager = ConfigManager(path)

    if not config_manager.exists():
        console.print("[yellow]⚠ No Rulesmith configuration found[/yellow]")
        console.print("Run [bold]rulesmith init[/bold] to set up this project")
        return

    config = config_manager.load()

    table = Table(show_header=False, box=None)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("Project", config.project_name)
    table.add_row("Stack", f"{config.detected_stack} ({config.stack_confidence:.0%} confidence)")
    table.add_row("Mode", config.generation_mode)
    table.add_row("Tools", ", ".join(config.active_formatters))
    table.add_row("Version", config.version)
    table.add_row("Created", str(config.created_at))
    table.add_row("Updated", str(config.updated_at))

    console.print(table)


if __name__ == "__main__":
    app()
