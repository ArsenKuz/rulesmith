"""CLI commands for Rulesmith."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cli.src.config import ConfigManager
from cli.src.detectors import StackDetector

app = typer.Typer(help="Initialize AI rules for current project")
console = Console()


@app.callback()
def init_callback():
    """Initialize AI rules for the current project."""
    pass


@app.command()
def init(
    quick: bool = typer.Option(False, "--quick", "-q", help="Quick mode with 3-5 questions"),
    guided: bool = typer.Option(
        False, "--guided", "-g", help="Guided mode with comprehensive interview"
    ),
    stack: Optional[str] = typer.Option(None, "--stack", "-s", help="Override auto-detected stack"),
    tools: Optional[str] = typer.Option(
        None, "--tools", "-t", help="Comma-separated list of target tools"
    ),
    project_path: Path = typer.Argument(Path("."), help="Path to project"),
):
    """Initialize AI rules for your project."""
    project_path = project_path.resolve()

    console.print(
        Panel.fit(
            f"[bold blue]Rulesmith - AI Rule Generator[/bold blue]\nProject: {project_path}",
            border_style="blue",
        )
    )

    # Detect stack
    console.print("\n[bold]Detecting technology stack...[/bold]")
    detector = StackDetector(project_path)
    result = detector.detect()

    if result.primary == "unknown":
        console.print("[yellow]⚠ Could not detect technology stack automatically.[/yellow]")
        console.print("Using generic rules. Consider specifying with --stack")
    else:
        console.print(
            f"[green]✓ Detected: {result.primary} (confidence: {result.confidence:.0%})[/green]"
        )

    # Use override if provided
    final_stack = stack or result.primary
    mode = "guided" if guided else "quick"

    # Parse tools
    target_tools = ["cursor", "claude", "copilot"]
    if tools:
        target_tools = [t.strip() for t in tools.split(",")]

    console.print(f"\n[bold]Mode:[/bold] {mode}")
    console.print(f"[bold]Stack:[/bold] {final_stack}")
    console.print(f"[bold]Target Tools:[/bold] {', '.join(target_tools)}")

    # Import and run generator
    try:
        from generator.src.orchestrator import GeneratorOrchestrator

        orchestrator = GeneratorOrchestrator(
            detected_stack=final_stack,
            library_path=ConfigManager(project_path).get_library_path(),
            generation_mode=mode,
            console=console,
        )

        result = orchestrator.run()

        # Save configuration
        config_manager = ConfigManager(project_path)
        from cli.src.config import ProjectConfig

        config = ProjectConfig(
            project_name=project_path.name,
            project_root=project_path,
            detected_stack=result.primary,
            stack_confidence=result.confidence,
            detected_signals=result.all_signals,
            selected_stack=final_stack if stack else None,
            generation_mode=mode,
            active_formatters=target_tools,
        )
        config_manager.save(config)

        # Run formatters
        console.print("\n[bold green]Generating rule files...[/bold green]")
        from formatters.src.sync import SyncEngine

        sync = SyncEngine(
            compiled_rules=result["compiled_rules"],
            project_context={
                "project_name": project_path.name,
                "selected_stack": final_stack,
                "generation_mode": mode,
            },
            project_root=project_path,
            target_tools=target_tools,
        )

        sync_results = sync.sync_all()

        for tool, tool_result in sync_results.items():
            if tool_result["success"]:
                console.print(f"[green]✓ {tool}[/green]")
                for f in tool_result.get("files_created", []):
                    console.print(f"  Created: {f}")
            else:
                console.print(f"[red]✗ {tool}: {tool_result.get('error', 'Unknown error')}[/red]")

        console.print(
            Panel.fit(
                "[bold green]✓ Rules generated successfully![/bold green]\n\n"
                "Run [cyan]rulesmith status[/cyan] to see project status\n"
                "Run [cyan]rulesmith update[/cyan] to update rule library",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
