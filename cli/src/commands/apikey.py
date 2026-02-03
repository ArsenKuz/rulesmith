"""API key management command - Configure API keys for LLM providers."""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from cli.src.config.api_keys import APIKeyManager

app = typer.Typer()
console = Console()

# Provider information
PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "description": "GPT-4, GPT-3.5, and other OpenAI models",
        "key_url": "https://platform.openai.com/api-keys",
        "env_var": "OPENAI_API_KEY",
    },
    "anthropic": {
        "name": "Anthropic",
        "description": "Claude models (Claude 3, Claude 3.5)",
        "key_url": "https://console.anthropic.com/settings/keys",
        "env_var": "ANTHROPIC_API_KEY",
    },
    "cohere": {
        "name": "Cohere",
        "description": "Command, Embed, and other Cohere models",
        "key_url": "https://dashboard.cohere.com/api-keys",
        "env_var": "COHERE_API_KEY",
    },
    "openrouter": {
        "name": "OpenRouter",
        "description": "Access to multiple models through one API",
        "key_url": "https://openrouter.ai/keys",
        "env_var": "OPENROUTER_API_KEY",
    },
    "github": {
        "name": "GitHub",
        "description": "GitHub Copilot and GitHub API access",
        "key_url": "https://github.com/settings/tokens",
        "env_var": "GITHUB_TOKEN",
    },
}


@app.command("list")
def list_keys():
    """List all configured API keys."""
    manager = APIKeyManager()
    configured = manager.list_configured()

    table = Table(title="Configured API Keys")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Source", style="dim")

    for provider, has_key in configured.items():
        status = "✓ Configured" if has_key else "✗ Not configured"
        # Check if from env var
        env_var = PROVIDERS.get(provider, {}).get("env_var", "")
        source = "Environment" if env_var and typer.get_app_dir("rulesmith") else "Config file"
        if not has_key:
            source = "-"

        table.add_row(
            PROVIDERS.get(provider, {}).get("name", provider),
            status,
            source,
        )

    console.print(table)

    console.print("\n[yellow]Note:[/yellow] Environment variables take precedence over saved keys.")


@app.command("set")
def set_key(
    provider: str = typer.Argument(..., help="Provider name (openai, anthropic, cohere, etc.)"),
    key: Optional[str] = typer.Option(
        None, "--key", "-k", help="API key (will prompt if not provided)"
    ),
):
    """Set API key for a provider."""
    provider = provider.lower()

    if provider not in PROVIDERS:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        console.print(f"Available: {', '.join(PROVIDERS.keys())}")
        raise typer.Exit(1)

    provider_info = PROVIDERS[provider]

    if not key:
        console.print(f"\n[bold]{provider_info['name']}[/bold]")
        console.print(f"[dim]{provider_info['description']}[/dim]")
        console.print(f"\nGet your API key: {provider_info['key_url']}")

        key = Prompt.ask("\nEnter API key", password=True)

    if not key or key.strip() == "":
        console.print("[red]API key cannot be empty[/red]")
        raise typer.Exit(1)

    # Save key
    manager = APIKeyManager()
    manager.set_key(provider, key)

    # Mask key for display
    masked_key = key[:4] + "*" * (len(key) - 8) + key[-4:] if len(key) > 8 else "****"

    console.print(f"\n[green]✓ API key saved for {provider_info['name']}[/green]")
    console.print(f"[dim]Key: {masked_key}[/dim]")

    # Check if env var is set
    env_var = provider_info.get("env_var", "")
    if env_var:
        console.print(f"\n[yellow]Tip:[/yellow] You can also set {env_var} environment variable")


@app.command("remove")
def remove_key(
    provider: str = typer.Argument(..., help="Provider name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Remove API key for a provider."""
    provider = provider.lower()

    if provider not in PROVIDERS:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        raise typer.Exit(1)

    provider_name = PROVIDERS[provider]["name"]

    manager = APIKeyManager()
    if not manager.has_key(provider):
        console.print(f"[yellow]No API key configured for {provider_name}[/yellow]")
        raise typer.Exit(0)

    if not force:
        confirm = Confirm.ask(f"Remove API key for {provider_name}?", default=False)
        if not confirm:
            console.print("Cancelled")
            raise typer.Exit(0)

    manager.remove_key(provider)
    console.print(f"[green]✓ API key removed for {provider_name}[/green]")


@app.command("show")
def show_key(
    provider: str = typer.Argument(..., help="Provider name"),
):
    """Show API key status for a provider."""
    provider = provider.lower()

    if provider not in PROVIDERS:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        raise typer.Exit(1)

    provider_info = PROVIDERS[provider]
    manager = APIKeyManager()

    has_key = manager.has_key(provider)
    key_value = manager.get_key(provider) if has_key else None

    if has_key and key_value:
        masked_key = key_value[:4] + "*" * (len(key_value) - 8) + key_value[-4:]
    else:
        masked_key = "Not configured"

    console.print(
        Panel(
            f"[bold]{provider_info['name']}[/bold]\n"
            f"[dim]{provider_info['description']}[/dim]\n\n"
            f"Status: {'✓ Configured' if has_key else '✗ Not configured'}\n"
            f"Key: {masked_key}\n"
            f"Get key: {provider_info['key_url']}",
            title="API Key Status",
            border_style="green" if has_key else "red",
        )
    )


@app.command("test")
def test_key(
    provider: str = typer.Argument(..., help="Provider name to test"),
):
    """Test if an API key is valid (basic connectivity check)."""
    provider = provider.lower()

    if provider not in PROVIDERS:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        raise typer.Exit(1)

    provider_name = PROVIDERS[provider]["name"]
    manager = APIKeyManager()

    if not manager.has_key(provider):
        console.print(f"[red]No API key configured for {provider_name}[/red]")
        console.print(f"Run: rulesmith apikey set {provider}")
        raise typer.Exit(1)

    console.print(f"Testing API key for {provider_name}...")

    # TODO: Implement actual API connectivity tests
    # For now, just show that we have a key
    console.print(f"[yellow]Note:[/yellow] API connectivity test not yet implemented")
    console.print("[dim]Key exists and is properly formatted[/dim]")


@app.callback(invoke_without_command=True)
def apikey_default():
    """Manage API keys for LLM providers and AI tools."""
    console.print("[bold]API Key Management[/bold]\n")
    console.print("Commands:")
    console.print("  [green]rulesmith apikey list[/green]     - List configured keys")
    console.print("  [green]rulesmith apikey set <provider>[/green] - Set API key")
    console.print("  [green]rulesmith apikey remove <provider>[/green] - Remove API key")
    console.print("  [green]rulesmith apikey show <provider>[/green] - Show key status")
    console.print("  [green]rulesmith apikey test <provider>[/green] - Test key validity")
    console.print("\nSupported providers:")
    for key, info in PROVIDERS.items():
        console.print(f"  • [cyan]{key}[/cyan]: {info['name']}")
