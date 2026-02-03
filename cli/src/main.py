"""Rulesmith CLI - AI rule generator for coding assistants."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.columns import Columns
from rich.align import Align
from cli.src.commands import init, update, status, prd, apikey, new, skill, library
from cli.src.commands.shell import start_shell

console = Console()

# Bold 3D ASCII art with strong visual volume
HERO_TITLE = r"""
[bold bright_cyan]██████╗  ██╗   ██╗██╗     ███████╗███████╗███╗   ███╗██╗████████╗██╗  ██╗[/bold bright_cyan]
[bold bright_cyan]██╔══██╗ ██║   ██║██║     ██╔════╝██╔════╝████╗ ████║██║╚══██╔══╝██║  ██║[/bold bright_cyan]
[bold cyan]██████╔╝ ██║   ██║██║     █████╗  ███████╗██╔████╔██║██║   ██║   ███████║[/bold cyan]
[bold cyan]██╔══██╗ ██║   ██║██║     ██╔══╝  ╚════██║██║╚██╔╝██║██║   ██║   ██╔══██║[/bold cyan]
[bold blue]██║  ██║ ╚██████╔╝███████╗███████╗███████║██║ ╚═╝ ██║██║   ██║   ██║  ██║[/bold blue]
[bold blue]╚═╝  ╚═╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝[/bold blue]
"""

VERSION = "2.0.0"


def show_hero_banner():
    """Display the Rulesmith hero banner."""
    # Create the banner with border
    console.print()
    console.print(
        "[bold blue]╔══════════════════════════════════════════════════════════════════════════╗[/bold blue]"
    )
    console.print(
        "[bold blue]║                                                                          ║[/bold blue]"
    )

    # Print the title lines with proper spacing
    for line in HERO_TITLE.strip().split("\n"):
        if line.strip():  # Skip empty lines
            console.print(f"[bold blue]║[/bold blue] {line:<72} [bold blue]║[/bold blue]")

    console.print(
        "[bold blue]║                                                                          ║[/bold blue]"
    )
    console.print(
        "[bold blue]╚══════════════════════════════════════════════════════════════════════════╝[/bold blue]"
    )

    # Tagline panel
    console.print()
    console.print(
        Panel.fit(
            "[bold white]🤖 AI-Powered Project Setup Agent[/bold white]\n"
            "[dim]Generate PRDs, rules, and project structure for Cursor, Claude, Copilot & more[/dim]",
            border_style="bright_cyan",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
    console.print()


def show_quick_start():
    """Show quick start guide with better formatting."""
    console.print("[bold yellow]🚀 Quick Start[/bold yellow]")
    console.print("[dim]─────────────[/dim]\n")

    commands = [
        (
            "[bold green]new[/bold green]",
            "Create a new project with AI-generated PRD",
            "[blue]➜[/blue]",
        ),
        (
            "[bold green]init[/bold green]",
            "Initialize AI rules for existing project",
            "[blue]➜[/blue]",
        ),
        (
            "[bold green]prd[/bold green]",
            "Generate Product Requirements Document",
            "[blue]➜[/blue]",
        ),
        (
            "[bold green]apikey set[/bold green]",
            "Configure API keys for LLM providers",
            "[blue]➜[/blue]",
        ),
        (
            "[bold green]status[/bold green]",
            "Check current project configuration",
            "[blue]➜[/blue]",
        ),
    ]

    for cmd, desc, arrow in commands:
        console.print(f"  {arrow} [bold]rulesmith {cmd}[/bold]")
        console.print(f"    [dim]{desc}[/dim]\n")

    # Tip box
    console.print(
        Panel(
            "[dim]💡 Run[/dim] [bold cyan]rulesmith --help[/bold cyan] [dim]for all available options[/dim]",
            border_style="dim",
            box=box.ROUNDED,
            padding=(0, 2),
        )
    )
    console.print()


# Create the main app with custom no-args callback
app = typer.Typer(
    name="rulesmith",
    help="AI rule generator for coding assistants",
    rich_markup_mode="rich",
    no_args_is_help=False,  # We'll handle this ourselves
)

# Add all commands
app.add_typer(init.app, name="init", help="Initialize AI rules for current project")
app.add_typer(new.app, name="new", help="Create a new project with AI-generated PRD and rules")
app.add_typer(prd.app, name="prd", help="Generate Product Requirements Document")
app.add_typer(apikey.app, name="apikey", help="Manage API keys for LLM providers")
app.add_typer(skill.app, name="skill", help="Manage and execute skills")
app.add_typer(library.app, name="library", help="Manage rules and skills libraries")
app.command(name="update")(update.update_command)
app.command(name="status")(status.status_command)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show version"),
    no_shell: bool = typer.Option(False, "--no-shell", help="Show help instead of starting REPL"),
):
    """Main callback - starts REPL when no command given."""
    if version:
        console.print(f"[bold cyan]Rulesmith[/bold cyan] version [bold]{VERSION}[/bold]")
        raise typer.Exit()

    # If no command provided, start REPL by default
    if ctx.invoked_subcommand is None:
        if no_shell:
            # Show traditional help
            show_hero_banner()
            show_quick_start()
            console.print(ctx.get_help())
        else:
            # Start interactive REPL
            start_shell()


if __name__ == "__main__":
    app()
