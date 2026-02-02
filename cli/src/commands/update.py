"""Update command for Rulesmith."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from cli.src.config import ConfigManager

app = typer.Typer(help="Update rule library")
console = Console()


@app.command()
def update(
    project_path: Path = typer.Argument(Path("."), help="Path to project"),
):
    """Update rule library from GitHub."""
    project_path = project_path.resolve()

    console.print(
        Panel.fit(
            "[bold blue]Rulesmith - Update Library[/bold blue]",
            border_style="blue",
        )
    )

    # Check if project is initialized
    config_manager = ConfigManager(project_path)
    if not config_manager.exists():
        console.print("[red]Error: Project not initialized. Run 'rulesmith init' first.[/red]")
        raise typer.Exit(1)

    # Get library path
    library_path = config_manager.get_library_path()

    console.print(f"\nLibrary path: {library_path}")

    # Update library (git pull or clone)
    import subprocess

    try:
        if library_path.exists():
            console.print("[bold]Pulling latest changes...[/bold]")
            result = subprocess.run(
                ["git", "-C", str(library_path), "pull", "origin", "main"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                console.print("[green]✓ Library updated successfully[/green]")
            else:
                console.print(f"[yellow]Warning: {result.stderr}[/yellow]")
        else:
            console.print("[bold]Cloning library...[/bold]")
            # In real implementation, this would clone from GitHub
            console.print("[yellow]Library not found. Please clone manually:[/yellow]")
            console.print(
                f"  git clone https://github.com/user/rulesmith-library.git {library_path}"
            )

        # Update config with new timestamp
        config = config_manager.load()
        if config:
            from datetime import datetime

            config.library_updated_at = datetime.now()
            config_manager.save(config)

    except Exception as e:
        console.print(f"[red]Error updating library: {e}[/red]")
        raise typer.Exit(1)
