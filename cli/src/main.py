"""Main entry point for Rulesmith CLI."""

import typer
from cli.src.commands import init_app, status_app, update_app

app = typer.Typer(
    name="rulesmith",
    help="AI rule generator for coding assistants",
    no_args_is_help=True,
)

# Add subcommands
app.add_typer(init_app, name="init")
app.add_typer(update_app, name="update")
app.add_typer(status_app, name="status")


@app.callback()
def main():
    """Rulesmith - Generate AI assistant rules for your project."""
    pass


if __name__ == "__main__":
    app()
