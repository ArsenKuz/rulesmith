"""Skill command - Manage and execute skills.

Provides CLI interface for:
- Listing available skills
- Loading skills into context
- Viewing skill information
- Managing active skills
"""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from generator.src.skills import SkillRegistry, SkillExecutor, SkillLoader

app = typer.Typer(help="Manage and execute skills")
console = Console()

# Initialize skills components
SKILLS_PATH = Path.home() / ".rulesmith" / "libraries" / "skills"
registry = SkillRegistry(SKILLS_PATH)
executor = SkillExecutor(SKILLS_PATH)


@app.command("list")
def list_skills(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
):
    """List all available skills."""
    registry.load_index()

    skills = registry.list_skills(category=category, tag=tag)

    if not skills:
        console.print("[yellow]No skills found.[/yellow]")
        if not SKILLS_PATH.exists():
            console.print(f"[dim]Skills directory not found: {SKILLS_PATH}[/dim]")
            console.print("[dim]Run 'rulesmith library update' to download skills.[/dim]")
        return

    # Create table
    table = Table(
        title="Available Skills",
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED,
    )

    table.add_column("Name", style="bold green")
    table.add_column("Description", style="white")
    table.add_column("Category", style="dim")
    table.add_column("Status", style="dim")

    for skill in skills:
        status = "[green]✓[/green]" if skill.loaded else "[dim]○[/dim]"
        table.add_row(
            skill.name,
            skill.description[:60] + "..." if len(skill.description) > 60 else skill.description,
            skill.category or "-",
            status,
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(skills)} skills[/dim]")
    console.print("[dim]Run 'rulesmith skill info <name>' for details[/dim]")


@app.command("info")
def skill_info(
    name: str = typer.Argument(..., help="Skill name"),
):
    """Show detailed information about a skill."""
    registry.load_index()

    # Check if skill exists
    if not registry.skill_exists(name):
        console.print(f"[red]Skill '{name}' not found.[/red]")
        console.print("[dim]Run 'rulesmith skill list' to see available skills.[/dim]")
        raise typer.Exit(1)

    # Load the skill
    skill = registry.get_skill(name)

    if not skill:
        console.print(f"[red]Failed to load skill '{name}'.[/red]")
        raise typer.Exit(1)

    # Display skill info
    console.print()
    console.print(
        Panel.fit(
            f"[bold cyan]{skill.metadata.name}[/bold cyan]\n"
            f"[dim]{skill.metadata.description}[/dim]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    )

    # Metadata table
    table = Table(show_header=False, box=None)
    table.add_column("Property", style="bold")
    table.add_column("Value")

    if skill.metadata.license:
        table.add_row("License:", skill.metadata.license)
    if skill.metadata.compatibility:
        table.add_row("Compatibility:", skill.metadata.compatibility)

    # Check for resources
    has_refs = skill.references is not None
    has_scripts = skill.scripts is not None
    has_assets = skill.assets is not None

    resources = []
    if has_refs:
        resources.append("references")
    if has_scripts:
        resources.append("scripts")
    if has_assets:
        resources.append("assets")

    if resources:
        table.add_row("Resources:", ", ".join(resources))

    console.print(table)

    # Active status
    if executor.is_skill_active(name):
        console.print("\n[green]✓ This skill is currently loaded[/green]")
    else:
        console.print(f"\n[dim]Load with: rulesmith skill use {name}[/dim]")


@app.command("use")
def use_skill(
    name: str = typer.Argument(..., help="Skill name to use"),
):
    """Load and use a skill."""
    registry.load_index()

    # Check if skill exists
    if not registry.skill_exists(name):
        console.print(f"[red]Skill '{name}' not found.[/red]")
        raise typer.Exit(1)

    # Load the skill
    result = executor.load_skill(name)

    if result.success:
        console.print(f"[green]✓ {result.message}[/green]")

        # Get skill content preview
        content = executor.get_skill_context(name)
        if content:
            preview = content[:500] + "..." if len(content) > 500 else content
            console.print("\n[bold]Skill Context:[/bold]")
            console.print(Panel(preview, border_style="dim", box=box.ROUNDED))
    else:
        console.print(f"[red]✗ {result.message}[/red]")
        raise typer.Exit(1)


@app.command("unload")
def unload_skill(
    name: str = typer.Argument(..., help="Skill name to unload"),
):
    """Unload an active skill."""
    result = executor.unload_skill(name)

    if result.success:
        console.print(f"[green]✓ {result.message}[/green]")
    else:
        console.print(f"[yellow]⚠ {result.message}[/yellow]")


@app.command("active")
def list_active():
    """List all currently active skills."""
    active_skills = executor.get_active_skills()

    if not active_skills:
        console.print("[dim]No skills currently active.[/dim]")
        console.print("[dim]Use 'rulesmith skill use <name>' to load a skill.[/dim]")
        return

    console.print(f"\n[bold]Active Skills ({len(active_skills)}):[/bold]\n")

    for skill in active_skills:
        console.print(f"  [green]●[/green] [bold]{skill.name}[/bold]")
        console.print(f"    [dim]{skill.metadata.description}[/dim]\n")


@app.command("search")
def search_skills(
    query: str = typer.Argument(..., help="Search query"),
):
    """Search for skills by name or description."""
    registry.load_index()

    results = registry.search_skills(query)

    if not results:
        console.print(f"[yellow]No skills found matching '{query}'.[/yellow]")
        return

    console.print(f"\n[bold]Search Results for '{query}':[/bold]\n")

    for skill in results:
        console.print(f"  [bold]{skill.name}[/bold]")
        console.print(f"    [dim]{skill.description}[/dim]\n")


@app.command("categories")
def list_categories():
    """List all skill categories."""
    registry.load_index()

    categories = registry.get_categories()

    if not categories:
        console.print("[dim]No categories defined.[/dim]")
        return

    console.print("\n[bold]Skill Categories:[/bold]\n")

    for category in categories:
        count = len(registry.list_skills(category=category))
        console.print(f"  [bold]{category}[/bold] [dim]({count} skills)[/dim]")


@app.command("reload")
def reload_skills():
    """Reload skills from disk (refresh registry)."""
    registry.refresh()
    executor.clear_all()
    console.print("[green]✓ Skills registry refreshed[/green]")
    console.print("[dim]All active skills have been cleared.[/dim]")


# Support calling without subcommand
@app.callback(invoke_without_command=True)
def skill_callback(ctx: typer.Context):
    """Default callback - show help if no subcommand."""
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
