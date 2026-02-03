"""Update command - Update rule library from GitHub."""

import typer
import subprocess
from pathlib import Path
from datetime import datetime
from rich.console import Console

from cli.src.config.manager import ConfigManager

console = Console()

LIBRARY_REPO = "github.com/user/rulesmith-library"
LIBRARY_PATH = Path.home() / ".rulesmith" / "library"


def update_command():
    """Update rule library from GitHub repository."""
    console.print("[bold blue]📦 Updating rule library...[/bold blue]")

    try:
        # Clone or pull latest library
        if LIBRARY_PATH.exists():
            # Git pull
            result = subprocess.run(
                ["git", "-C", str(LIBRARY_PATH), "pull", "origin", "main"],
                capture_output=True,
                text=True,
                check=True,
            )
            console.print(f"[dim]{result.stdout}[/dim]")
        else:
            # Fresh clone
            LIBRARY_PATH.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                ["git", "clone", f"https://{LIBRARY_REPO}.git", str(LIBRARY_PATH)],
                capture_output=True,
                text=True,
                check=True,
            )
            console.print(f"[dim]{result.stdout}[/dim]")

        # Update local config with new version if in a project
        config_manager = ConfigManager(Path("."))
        config = config_manager.load()
        if config:
            config.library_version = get_library_version()
            config.library_updated_at = datetime.now()
            config_manager.save(config)

        console.print("[bold green]✅ Library updated successfully![/bold green]")

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error updating library:[/bold red] {e.stderr}")
        raise typer.Exit(1)


def get_library_version() -> str:
    """Get current library version from git."""
    try:
        result = subprocess.run(
            ["git", "-C", str(LIBRARY_PATH), "describe", "--tags", "--always"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"
