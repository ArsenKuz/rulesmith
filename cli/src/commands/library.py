"""Library command - Manage rules and skills libraries.

Provides commands to:
- Update libraries from remote repositories
- List configured library sources
- Add/remove custom library sources
- Check library status
"""

import typer
import subprocess
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

app = typer.Typer(help="Manage rules and skills libraries")
console = Console()

# Configuration paths
RULESMITH_DIR = Path.home() / ".rulesmith"
LIBRARY_CONFIG_FILE = RULESMITH_DIR / "library-config.json"
LIBRARIES_DIR = RULESMITH_DIR / "libraries"
RULES_DIR = LIBRARIES_DIR / "rules"
SKILLS_DIR = LIBRARIES_DIR / "skills"


@dataclass
class LibrarySource:
    """A library source configuration."""

    name: str
    url: str
    branch: str = "main"
    type: str = "rules"  # or "skills"


@dataclass
class LibraryConfig:
    """Library configuration."""

    rules_sources: List[LibrarySource]
    skills_sources: List[LibrarySource]
    last_update: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rules": {
                "sources": [
                    {"name": s.name, "url": s.url, "branch": s.branch} for s in self.rules_sources
                ]
            },
            "skills": {
                "sources": [
                    {"name": s.name, "url": s.url, "branch": s.branch} for s in self.skills_sources
                ]
            },
            "last_update": self.last_update,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LibraryConfig":
        """Create from dictionary."""
        rules_sources = [
            LibrarySource(
                name=s["name"], url=s["url"], branch=s.get("branch", "main"), type="rules"
            )
            for s in data.get("rules", {}).get("sources", [])
        ]
        skills_sources = [
            LibrarySource(
                name=s["name"], url=s["url"], branch=s.get("branch", "main"), type="skills"
            )
            for s in data.get("skills", {}).get("sources", [])
        ]
        return cls(
            rules_sources=rules_sources,
            skills_sources=skills_sources,
            last_update=data.get("last_update"),
        )


def get_default_config() -> LibraryConfig:
    """Get default library configuration."""
    return LibraryConfig(
        rules_sources=[
            LibrarySource(
                name="official",
                url="https://github.com/ArsenKuz/rulesmith-rules",
                branch="main",
                type="rules",
            )
        ],
        skills_sources=[
            LibrarySource(
                name="official",
                url="https://github.com/ArsenKuz/rulesmith-skills",
                branch="main",
                type="skills",
            )
        ],
    )


def load_config() -> LibraryConfig:
    """Load library configuration."""
    if LIBRARY_CONFIG_FILE.exists():
        try:
            with open(LIBRARY_CONFIG_FILE, "r") as f:
                data = json.load(f)
            return LibraryConfig.from_dict(data)
        except Exception:
            pass

    # Return default config
    return get_default_config()


def save_config(config: LibraryConfig) -> None:
    """Save library configuration."""
    RULESMITH_DIR.mkdir(parents=True, exist_ok=True)
    with open(LIBRARY_CONFIG_FILE, "w") as f:
        json.dump(config.to_dict(), f, indent=2)


def ensure_directories() -> None:
    """Ensure library directories exist."""
    LIBRARIES_DIR.mkdir(parents=True, exist_ok=True)
    RULES_DIR.mkdir(exist_ok=True)
    SKILLS_DIR.mkdir(exist_ok=True)


def update_repository(source: LibrarySource, target_dir: Path) -> bool:
    """Update a single repository.

    Args:
        source: Library source configuration
        target_dir: Directory to clone/pull into

    Returns:
        True if successful
    """
    repo_dir = target_dir / source.name

    try:
        if repo_dir.exists():
            # Pull existing repository
            result = subprocess.run(
                ["git", "-C", str(repo_dir), "pull", "origin", source.branch],
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        else:
            # Clone new repository
            result = subprocess.run(
                ["git", "clone", "-b", source.branch, source.url, str(repo_dir)],
                capture_output=True,
                text=True,
                check=True,
            )
            return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error updating {source.name}: {e}[/red]")
        if e.stderr:
            console.print(f"[dim]{e.stderr}[/dim]")
        return False


@app.command("update")
def update_libraries(
    rules: bool = typer.Option(True, "--rules/--no-rules", help="Update rules library"),
    skills: bool = typer.Option(True, "--skills/--no-skills", help="Update skills library"),
):
    """Update rules and skills libraries from remote repositories."""
    ensure_directories()
    config = load_config()

    console.print("[bold blue]📦 Updating Libraries[/bold blue]\n")

    success_count = 0
    total_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Update rules
        if rules:
            for source in config.rules_sources:
                total_count += 1
                task = progress.add_task(f"Updating rules: {source.name}...", total=None)

                if update_repository(source, RULES_DIR):
                    progress.update(task, description=f"[green]✓[/green] Rules: {source.name}")
                    success_count += 1
                else:
                    progress.update(task, description=f"[red]✗[/red] Rules: {source.name}")

        # Update skills
        if skills:
            for source in config.skills_sources:
                total_count += 1
                task = progress.add_task(f"Updating skills: {source.name}...", total=None)

                if update_repository(source, SKILLS_DIR):
                    progress.update(task, description=f"[green]✓[/green] Skills: {source.name}")
                    success_count += 1
                else:
                    progress.update(task, description=f"[red]✗[/red] Skills: {source.name}")

    # Update timestamp
    config.last_update = datetime.now().isoformat()
    save_config(config)

    console.print()
    if success_count == total_count:
        console.print(
            f"[green]✓ Successfully updated {success_count}/{total_count} libraries[/green]"
        )
    else:
        console.print(f"[yellow]⚠ Updated {success_count}/{total_count} libraries[/yellow]")


@app.command("list")
def list_sources():
    """List configured library sources."""
    config = load_config()

    console.print("\n[bold]Library Sources:[/bold]\n")

    # Rules sources
    if config.rules_sources:
        console.print("[bold cyan]Rules:[/bold cyan]")
        for source in config.rules_sources:
            console.print(f"  [bold]{source.name}[/bold]")
            console.print(f"    URL: {source.url}")
            console.print(f"    Branch: {source.branch}\n")

    # Skills sources
    if config.skills_sources:
        console.print("[bold cyan]Skills:[/bold cyan]")
        for source in config.skills_sources:
            console.print(f"  [bold]{source.name}[/bold]")
            console.print(f"    URL: {source.url}")
            console.print(f"    Branch: {source.branch}\n")

    # Last update
    if config.last_update:
        last_update = datetime.fromisoformat(config.last_update)
        console.print(f"[dim]Last updated: {last_update.strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
    else:
        console.print("[dim]Never updated[/dim]")


@app.command("add")
def add_source(
    name: str = typer.Argument(..., help="Source name"),
    url: str = typer.Argument(..., help="Repository URL"),
    type: str = typer.Option("rules", "--type", "-t", help="Library type (rules or skills)"),
    branch: str = typer.Option("main", "--branch", "-b", help="Git branch"),
):
    """Add a new library source."""
    config = load_config()

    new_source = LibrarySource(name=name, url=url, branch=branch, type=type)

    if type == "rules":
        # Check for duplicates
        if any(s.name == name for s in config.rules_sources):
            console.print(f"[red]Rules source '{name}' already exists[/red]")
            raise typer.Exit(1)
        config.rules_sources.append(new_source)
    elif type == "skills":
        if any(s.name == name for s in config.skills_sources):
            console.print(f"[red]Skills source '{name}' already exists[/red]")
            raise typer.Exit(1)
        config.skills_sources.append(new_source)
    else:
        console.print(f"[red]Invalid type '{type}'. Must be 'rules' or 'skills'[/red]")
        raise typer.Exit(1)

    save_config(config)
    console.print(f"[green]✓ Added {type} source: {name}[/green]")


@app.command("remove")
def remove_source(
    name: str = typer.Argument(..., help="Source name"),
    type: str = typer.Option(None, "--type", "-t", help="Library type (rules or skills)"),
):
    """Remove a library source."""
    config = load_config()

    removed = False

    if type is None or type == "rules":
        rules_sources = [s for s in config.rules_sources if s.name != name]
        if len(rules_sources) < len(config.rules_sources):
            config.rules_sources = rules_sources
            removed = True
            console.print(f"[green]✓ Removed rules source: {name}[/green]")

    if type is None or type == "skills":
        skills_sources = [s for s in config.skills_sources if s.name != name]
        if len(skills_sources) < len(config.skills_sources):
            config.skills_sources = skills_sources
            removed = True
            console.print(f"[green]✓ Removed skills source: {name}[/green]")

    if not removed:
        console.print(f"[red]Source '{name}' not found[/red]")
        raise typer.Exit(1)

    save_config(config)


@app.command("status")
def library_status():
    """Show library status and statistics."""
    ensure_directories()
    config = load_config()

    console.print("\n[bold blue]📊 Library Status[/bold blue]\n")

    # Rules status
    rules_count = 0
    if RULES_DIR.exists():
        for source in config.rules_sources:
            source_dir = RULES_DIR / source.name
            if source_dir.exists():
                # Count .md files
                rules_count += len(list(source_dir.rglob("*.md")))

    console.print(f"[bold]Rules:[/bold]")
    console.print(f"  Sources: {len(config.rules_sources)}")
    console.print(f"  Files: {rules_count}")
    console.print(f"  Directory: {RULES_DIR}\n")

    # Skills status
    skills_count = 0
    if SKILLS_DIR.exists():
        for source in config.skills_sources:
            source_dir = SKILLS_DIR / source.name
            if source_dir.exists():
                skills_count += len([d for d in source_dir.iterdir() if d.is_dir()])

    console.print(f"[bold]Skills:[/bold]")
    console.print(f"  Sources: {len(config.skills_sources)}")
    console.print(f"  Skills: {skills_count}")
    console.print(f"  Directory: {SKILLS_DIR}\n")

    # Last update
    if config.last_update:
        last_update = datetime.fromisoformat(config.last_update)
        console.print(f"[dim]Last updated: {last_update.strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
    else:
        console.print("[yellow]⚠ Libraries have never been updated[/yellow]")
        console.print("[dim]Run 'rulesmith library update' to download[/dim]")


# Support calling without subcommand
@app.callback(invoke_without_command=True)
def library_callback(ctx: typer.Context):
    """Default callback - show help if no subcommand."""
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
