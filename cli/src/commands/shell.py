"""Interactive REPL shell for Rulesmith CLI.

Provides a persistent shell environment where users can execute
Rulesmith commands without prefixing with 'rulesmith' each time.
"""

import sys
import shlex
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich import box

# Import commands
import typer
from cli.src.commands import (
    init_command,
    update_command,
    status_command,
    prd_command,
    apikey_app,
    new_command,
)

console = Console()


class RulesmithREPL:
    """Interactive REPL for Rulesmith CLI."""

    def __init__(self):
        self.running = False
        self.commands = {
            "init": self._cmd_init,
            "new": self._cmd_new,
            "prd": self._cmd_prd,
            "apikey": self._cmd_apikey,
            "skill": self._cmd_skill,
            "library": self._cmd_library,
            "update": self._cmd_update,
            "status": self._cmd_status,
            "help": self._cmd_help,
            "exit": self._cmd_exit,
            "quit": self._cmd_exit,
        }

    def start(self) -> None:
        """Start the REPL loop."""
        self.running = True

        # Show welcome message
        self._show_welcome()

        # REPL loop
        while self.running:
            try:
                # Get user input
                user_input = Prompt.ask("[bold cyan]rulesmith>[/bold cyan]").strip()

                if not user_input:
                    continue

                # Parse command
                parts = shlex.split(user_input)
                command = parts[0].lower()
                args = parts[1:]

                # Execute command
                if command in self.commands:
                    try:
                        self.commands[command](args)
                    except Exception as e:
                        console.print(f"[red]Error: {e}[/red]")
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("Type 'help' for available commands.")

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' or 'quit' to leave.[/yellow]")
            except EOFError:
                console.print("\n[dim]Goodbye![/dim]")
                break

    def _show_welcome(self) -> None:
        """Show welcome message and available commands."""
        console.print()
        console.print(
            Panel.fit(
                "[bold green]🚀 Rulesmith Interactive Shell[/bold green]\n"
                "[dim]Type 'help' for available commands or 'exit' to quit.[/dim]",
                border_style="green",
                box=box.ROUNDED,
            )
        )
        console.print()

    def _cmd_init(self, args: List[str]) -> None:
        """Handle init command."""
        import typer
        from cli.src.commands import init_command

        # Parse arguments
        quick = "--quick" in args or "-q" in args
        guided = "--guided" in args or "-g" in args
        stack = None
        path = Path(".")

        # Parse --stack and --path
        for i, arg in enumerate(args):
            if arg in ["--stack", "-s"] and i + 1 < len(args):
                stack = args[i + 1]
            elif arg in ["--path", "-p"] and i + 1 < len(args):
                path = Path(args[i + 1])

        # Call the init function directly
        init_command(
            quick=quick,
            guided=guided,
            stack=stack,
            path=path,
        )

    def _cmd_new(self, args: List[str]) -> None:
        """Handle new command."""
        from pathlib import Path
        from cli.src.commands import new_command

        # Parse arguments
        prompt = None
        output = Path(".")
        guided = "--guided" in args or "-g" in args
        quick = "--quick" in args or "-q" in args
        llm_provider = "openai"
        llm_model = None
        dry_run = "--dry-run" in args

        # Get prompt (first non-flag argument)
        i = 0
        while i < len(args):
            arg = args[i]
            if not arg.startswith("-"):
                prompt = arg
                break
            elif arg in ["--output", "-o"] and i + 1 < len(args):
                output = Path(args[i + 1])
                i += 2
            elif arg in ["--provider", "-p"] and i + 1 < len(args):
                llm_provider = args[i + 1]
                i += 2
            elif arg in ["--model", "-m"] and i + 1 < len(args):
                llm_model = args[i + 1]
                i += 2
            else:
                i += 1

        # Call the new function
        new_command(
            prompt=prompt,
            output=output,
            guided=guided,
            quick=quick,
            llm_provider=llm_provider,
            llm_model=llm_model,
            dry_run=dry_run,
        )

    def _cmd_prd(self, args: List[str]) -> None:
        """Handle prd command."""
        from pathlib import Path
        from cli.src.commands import prd_command

        # Parse arguments
        path = Path(".")
        quick = "--quick" in args or "-q" in args
        output = None

        i = 0
        while i < len(args):
            arg = args[i]
            if arg in ["--path", "-p"] and i + 1 < len(args):
                path = Path(args[i + 1])
                i += 2
            elif arg in ["--output", "-o"] and i + 1 < len(args):
                output = args[i + 1]
                i += 2
            else:
                i += 1

        # Call the prd function
        prd_command(
            path=path,
            output=output,
            quick=quick,
        )

    def _cmd_apikey(self, args: List[str]) -> None:
        """Handle apikey command."""
        if not args:
            console.print("[red]Usage: apikey <list|set|remove|show|test> [provider][/red]")
            return

        action = args[0].lower()
        provider = args[1] if len(args) > 1 else None

        if action == "list":
            # Import and call list function
            from cli.src.commands.apikey import list_keys

            list_keys()
        elif action == "set":
            if not provider:
                console.print("[red]Usage: apikey set <provider>[/red]")
                return
            from cli.src.commands.apikey import set_key

            set_key(provider)
        elif action == "remove":
            if not provider:
                console.print("[red]Usage: apikey remove <provider>[/red]")
                return
            from cli.src.commands.apikey import remove_key

            remove_key(provider)
        elif action == "show":
            if not provider:
                console.print("[red]Usage: apikey show <provider>[/red]")
                return
            from cli.src.commands.apikey import show_key

            show_key(provider)
        elif action == "test":
            if not provider:
                console.print("[red]Usage: apikey test <provider>[/red]")
                return
            from cli.src.commands.apikey import test_key

            test_key(provider)
        else:
            console.print(f"[red]Unknown apikey action: {action}[/red]")
            console.print("Available: list, set, remove, show, test")

    def _cmd_update(self, args: List[str]) -> None:
        """Handle update command."""
        from cli.src.commands import update_command

        # Call the update function
        update_command()

    def _cmd_status(self, args: List[str]) -> None:
        """Handle status command."""
        from cli.src.commands import status_command

        # Call the status function
        status_command()

    def _cmd_skill(self, args: List[str]) -> None:
        """Handle skill command."""
        import subprocess
        import sys

        if not args:
            # Show skill help
            console.print("[bold]Skill Commands:[/bold]")
            console.print("  skill list              - List available skills")
            console.print("  skill info <name>       - Show skill details")
            console.print("  skill use <name>        - Load and use a skill")
            console.print("  skill unload <name>     - Unload a skill")
            console.print("  skill active            - Show active skills")
            console.print("  skill search <query>    - Search skills")
            return

        # Get the subcommand and remaining args
        subcommand = args[0]
        subcommand_args = args[1:]

        try:
            # Import the skill module and dispatch
            from cli.src.commands import skill

            if subcommand == "list":
                skill.list_skills(
                    category=subcommand_args[1]
                    if len(subcommand_args) > 1 and subcommand_args[0] in ["--category", "-c"]
                    else None,
                    tag=subcommand_args[1]
                    if len(subcommand_args) > 1 and subcommand_args[0] in ["--tag", "-t"]
                    else None,
                )
            elif subcommand == "info" and subcommand_args:
                skill.skill_info(name=subcommand_args[0])
            elif subcommand == "use" and subcommand_args:
                skill.use_skill(name=subcommand_args[0])
            elif subcommand == "unload" and subcommand_args:
                skill.unload_skill(name=subcommand_args[0])
            elif subcommand == "active":
                skill.list_active()
            elif subcommand == "search" and subcommand_args:
                skill.search_skills(query=subcommand_args[0])
            elif subcommand == "categories":
                skill.list_categories()
            elif subcommand == "reload":
                skill.reload_skills()
            else:
                console.print(f"[red]Unknown skill subcommand: {subcommand}[/red]")
                console.print("[dim]Use 'skill' without arguments to see available commands[/dim]")
        except Exception as e:
            console.print(f"[red]Error executing skill command: {e}[/red]")

    def _cmd_library(self, args: List[str]) -> None:
        """Handle library command."""
        try:
            from cli.src.commands import library

            if not args:
                library.library_callback(typer.Context(library.app))
                return

            subcommand = args[0]
            subcommand_args = args[1:]

            if subcommand == "update":
                rules = "--no-rules" not in subcommand_args
                skills = "--no-skills" not in subcommand_args
                library.update_libraries(rules=rules, skills=skills)
            elif subcommand == "list":
                library.list_sources()
            elif subcommand == "status":
                library.library_status()
            elif subcommand == "add" and len(subcommand_args) >= 2:
                name = subcommand_args[0]
                url = subcommand_args[1]
                lib_type = "rules"
                branch = "main"
                # Parse options
                i = 2
                while i < len(subcommand_args):
                    if subcommand_args[i] in ["--type", "-t"] and i + 1 < len(subcommand_args):
                        lib_type = subcommand_args[i + 1]
                        i += 2
                    elif subcommand_args[i] in ["--branch", "-b"] and i + 1 < len(subcommand_args):
                        branch = subcommand_args[i + 1]
                        i += 2
                    else:
                        i += 1
                library.add_source(name=name, url=url, type=lib_type, branch=branch)
            elif subcommand == "remove" and subcommand_args:
                name = subcommand_args[0]
                lib_type = None
                if "--type" in subcommand_args:
                    idx = subcommand_args.index("--type")
                    if idx + 1 < len(subcommand_args):
                        lib_type = subcommand_args[idx + 1]
                library.remove_source(name=name, type=lib_type)
            else:
                console.print(f"[red]Unknown library subcommand: {subcommand}[/red]")
                console.print(
                    "[dim]Use 'library' without arguments to see available commands[/dim]"
                )
        except Exception as e:
            console.print(f"[red]Error executing library command: {e}[/red]")

    def _cmd_help(self, args: List[str]) -> None:
        """Show help message."""
        help_text = """
[bold]Available Commands:[/bold]

[green]init[/green] [dim][options][/dim]
  Initialize AI rules for current project
  Options: --quick, --guided, --stack <stack>, --path <path>

[green]new[/green] [dim]<prompt> [options][/dim]
  Create a new project with AI-generated PRD
  Options: --output, --guided, --quick, --provider, --model, --dry-run

[green]prd[/green] [dim][options][/dim]
  Generate Product Requirements Document
  Options: --path, --output, --quick

[green]apikey[/green] [dim]<action> [provider][/dim]
  Manage API keys for LLM providers
  Actions: list, set, remove, show, test

[green]skill[/green] [dim]<subcommand> [args][/dim]
  Manage and execute skills
  Subcommands: list, info, use, unload, active, search

[green]library[/green] [dim]<subcommand> [args][/dim]
  Manage rules and skills libraries
  Subcommands: update, list, add, remove, status

[green]update[/green]
  Update rule library from remote repository

[green]status[/green]
  Show current project configuration

[green]help[/green]
  Show this help message

[green]exit[/green] / [green]quit[/green]
  Exit the REPL shell

[dim]Press Ctrl+C to cancel current operation.[/dim]
"""
        console.print(help_text)

    def _cmd_exit(self, args: List[str]) -> None:
        """Exit the REPL."""
        console.print("[dim]Goodbye![/dim]")
        self.running = False


def start_shell() -> None:
    """Entry point to start the REPL shell."""
    repl = RulesmithREPL()
    repl.start()


if __name__ == "__main__":
    start_shell()
