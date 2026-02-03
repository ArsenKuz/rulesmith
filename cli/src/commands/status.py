"""Status command - Show current project configuration."""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from cli.src.config.manager import ConfigManager

console = Console()


def status_command():
    """Show current project configuration."""

    config_manager = ConfigManager(Path("."))
    config = config_manager.load()

    if not config:
        console.print("[bold yellow]⚠️  No rulesmith configuration found.[/bold yellow]")
        console.print("Run [bold]rulesmith init[/bold] to initialize this project.")
        raise typer.Exit(1)

    # Main info table
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Label", style="cyan", justify="right")
    info_table.add_column("Value", style="white")

    info_table.add_row("Project:", config.project_name)
    info_table.add_row(
        "Stack:", f"{config.detected_stack} (confidence: {config.stack_confidence:.0%})"
    )
    info_table.add_row("Mode:", config.generation_mode)

    if config.selected_stack and config.selected_stack != config.detected_stack:
        info_table.add_row("User Override:", config.selected_stack)

    # Formatters table
    formatters_table = Table(show_header=False, box=None)
    formatters_table.add_column("Status")
    formatters_table.add_column("Formatter")

    for formatter in ["cursor", "claude", "copilot"]:
        status = "✅" if formatter in config.active_formatters else "❌"
        formatters_table.add_row(status, formatter.capitalize())

    # Library info
    library_table = Table(show_header=False, box=None)
    library_table.add_column("Label", style="cyan", justify="right")
    library_table.add_column("Value", style="white")

    library_table.add_row("Version:", config.library_version or "unknown")
    library_table.add_row(
        "Updated:",
        config.library_updated_at.strftime("%Y-%m-%d %H:%M:%S")
        if config.library_updated_at
        else "never",
    )

    # Display everything
    console.print(Panel.fit("[bold blue]📊 Rulesmith Project Status[/bold blue]"))
    console.print()
    console.print(info_table)
    console.print()
    console.print("[bold]Active Formatters:[/bold]")
    console.print(formatters_table)
    console.print()
    console.print("[bold]Library:[/bold]")
    console.print(library_table)
