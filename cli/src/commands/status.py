"""Status command for Rulesmith."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cli.src.config import ConfigManager

app = typer.Typer(help="Show project status")
console = Console()


@app.callback(invoke_without_command=True)
def status(
    project_path: Path = typer.Argument(Path("."), help="Path to project"),
):
    """Show current project configuration and status."""
    project_path = project_path.resolve()

    console.print(
        Panel.fit(
            "[bold blue]📊 Rulesmith Project Status[/bold blue]",
            border_style="blue",
        )
    )

    # Check if project is initialized
    config_manager = ConfigManager(project_path)
    config = config_manager.load()

    if not config:
        console.print("[yellow]⚠ Project not initialized. Run 'rulesmith init' first.[/yellow]")
        raise typer.Exit(1)

    # Display configuration
    table = Table(show_header=False, border_style="dim")
    table.add_column("Property", style="bold cyan")
    table.add_column("Value")

    table.add_row("Project", config.project_name)
    table.add_row("Stack", f"{config.detected_stack} (confidence: {config.stack_confidence:.0%})")
    if config.selected_stack and config.selected_stack != config.detected_stack:
        table.add_row("Selected Stack", config.selected_stack)
    table.add_row("Mode", config.generation_mode)

    console.print(table)

    # Display active formatters
    console.print("\n[bold]Active Formatters:[/bold]")
    for formatter in config.active_formatters:
        # Check if formatter output exists
        if formatter == "cursor":
            exists = (project_path / ".cursor" / "rules").exists()
        elif formatter == "claude":
            exists = (project_path / "CLAUDE.md").exists()
        elif formatter == "copilot":
            exists = (project_path / ".github" / "copilot-instructions.md").exists()
        elif formatter == "roo":
            exists = (project_path / ".roo" / "rules").exists()
        else:
            exists = False

        status_icon = "✅" if exists else "⚠️"
        console.print(f"  {status_icon} {formatter}")

    # Display library info
    console.print("\n[bold]Library:[/bold]")
    if config.library_version:
        console.print(f"  Version: {config.library_version}")
    if config.library_updated_at:
        console.print(f"  Updated: {config.library_updated_at}")

    # Display metadata
    console.print("\n[bold]Metadata:[/bold]")
    console.print(f"  Created: {config.created_at}")
    console.print(f"  Last Updated: {config.updated_at}")
