"""Init command - Initialize AI rules for current project."""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich import box

from cli.src.detectors.stack_detector import StackDetector
from cli.src.config.manager import ConfigManager

app = typer.Typer()
console = Console()


def get_stack_emoji(stack: str) -> str:
    """Get emoji for detected stack."""
    stack_emojis = {
        "nextjs": "⚛️",
        "react": "⚛️",
        "vue": "🟢",
        "python": "🐍",
        "django": "🐍",
        "fastapi": "🐍",
        "nodejs": "🟩",
        "go": "🐹",
        "rust": "🦀",
        "ruby": "💎",
        "php": "🐘",
    }
    return stack_emojis.get(stack.lower(), "📦")


@app.callback(invoke_without_command=True)
def init_command(
    quick: bool = typer.Option(
        False, "--quick", "-q", help="Quick mode - skip interactive prompts"
    ),
    guided: bool = typer.Option(False, "--guided", "-g", help="Guided mode - interactive setup"),
    stack: Optional[str] = typer.Option(
        None, "--stack", "-s", help="Override auto-detection with specific stack"
    ),
    path: Path = typer.Option(Path("."), "--path", "-p", help="Path to project directory"),
):
    """Initialize AI rules for current project."""

    project_path = path.resolve()

    # Header panel
    console.print()
    console.print(
        Panel.fit(
            f"[bold blue]🔧 Initializing Rulesmith[/bold blue]\n[dim]{project_path}[/dim]",
            border_style="blue",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
    console.print()

    # Detect stack with styled progress
    with Progress(
        SpinnerColumn(spinner_name="dots", style="cyan"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("🔍 Analyzing project files...", total=None)
        detector = StackDetector(project_path)
        result = detector.detect()

    # Results panel
    stack_emoji = get_stack_emoji(result.primary)

    results_table = Table(show_header=False, box=None, padding=(0, 2))
    results_table.add_column("Label", style="dim", justify="right")
    results_table.add_column("Value", style="bold")

    results_table.add_row("Stack:", f"{stack_emoji} {result.primary}")
    results_table.add_row("Confidence:", f"[green]{result.confidence:.0%}[/green]")

    if result.all_signals:
        signals_list = list(result.all_signals.keys())[:5]
        signals_str = ", ".join(signals_list)
        results_table.add_row("Signals:", f"[dim]{signals_str}[/dim]")

    console.print(
        Panel(
            results_table,
            title="[bold green]✓ Detection Results[/bold green]",
            border_style="green",
            box=box.ROUNDED,
        )
    )

    # Save configuration
    config_manager = ConfigManager(project_path)
    config = config_manager.create_config(
        project_name=project_path.name,
        detected_stack=result.primary,
        stack_confidence=result.confidence,
        detected_signals=result.all_signals,
        generation_mode="quick" if quick else "guided" if guided else "quick",
        selected_stack=stack,
    )
    config_manager.save(config)

    # Success panel
    console.print()
    console.print(
        Panel.fit(
            f"[bold green]✅ Configuration Saved[/bold green]\n\n"
            f"[dim]Location:[/dim] {config_manager.config_path}\n"
            f"[dim]Mode:[/dim] {config.generation_mode}",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )

    # Next steps
    console.print()
    console.print("[bold yellow]📋 Next Steps:[/bold yellow]")
    console.print()
    console.print("  [bold cyan]1.[/bold cyan] Run [bold]rulesmith update[/bold] to fetch rules")
    console.print("  [bold cyan]2.[/bold cyan] Review the generated configuration")
    console.print("  [bold cyan]3.[/bold cyan] Start coding with your AI assistant!")
    console.print()
