"""New command - Create a new project from scratch (Mode 1)."""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from cli.src.config.manager import ConfigManager
from cli.src.config.api_keys import APIKeyManager

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def new_command(
    prompt: Optional[str] = typer.Argument(None, help="Initial project idea/prompt"),
    output: Path = typer.Option(
        Path("."), "--output", "-o", help="Output directory for new project"
    ),
    guided: bool = typer.Option(
        False, "--guided", "-g", help="Guided mode - full interview (15 questions)"
    ),
    quick: bool = typer.Option(
        False, "--quick", "-q", help="Quick mode - minimal interview (5 questions)"
    ),
    llm_provider: str = typer.Option(
        "openai", "--provider", "-p", help="LLM provider (openai, anthropic, ollama)"
    ),
    llm_model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model name"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Skip LLM call, use template only"),
):
    """Create a new project with AI-generated PRD and rules."""

    # Get initial prompt if not provided
    if not prompt:
        prompt = console.input("[bold]Enter your project idea:[/bold] ")

    if not prompt:
        console.print("[red]Error: Project idea is required[/red]")
        raise typer.Exit(1)

    # Show welcome
    console.print(
        Panel.fit(
            f"[bold green]🆕 New Project: Rulesmith[/bold green]\n"
            f"Creating a new project from your idea:\n"
            f"[italic]{prompt}[/italic]",
            border_style="green",
        )
    )

    # Create output directory
    output_path = output.resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # Check for API keys
    api_manager = APIKeyManager()
    if not dry_run and not api_manager.has_key(llm_provider):
        console.print(f"[yellow]⚠️  No API key found for {llm_provider}[/yellow]")
        console.print("Set it with: [bold]rulesmith apikey set <provider> <key>[/bold]")
        console.print("Or use --dry-run to skip LLM generation")

        if not dry_run:
            proceed = console.input("Continue without LLM generation? [y/N]: ")
            if proceed.lower() != "y":
                raise typer.Exit(1)
            dry_run = True

    # Import here to avoid circular dependencies
    from generator.src.interview.modes.new_project import NewProjectMode
    from generator.src.llm import PRDGenerator
    from generator.src.parser import PRDParser, StackExtractor
    from generator.src.assembly.compiler import RuleCompiler
    from formatters.src.sync import SyncEngine

    # Phase 1: Interview
    console.print("\n[bold blue]Phase 1: Project Interview[/bold blue]")
    interview_mode = NewProjectMode(initial_prompt=prompt, console=console, quick_mode=quick)
    interview_answers = interview_mode.run()

    # Phase 2: Generate PRD via LLM (or template if dry-run)
    console.print("\n[bold blue]Phase 2: Generating PRD[/bold blue]")

    prd_content = None
    if not dry_run:
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Calling LLM to generate PRD...", total=None)

                api_key = api_manager.get_key(llm_provider)
                prd_gen = PRDGenerator(provider=llm_provider, api_key=api_key, model=llm_model)

                prd_content = prd_gen.generate(
                    initial_prompt=prompt,
                    interview_answers=interview_answers,
                    temperature=0.7,
                )

                progress.update(task, completed=True)

            console.print("[green]✓ PRD generated successfully[/green]")

        except Exception as e:
            console.print(f"[red]LLM generation failed: {e}[/red]")
            console.print("[yellow]Falling back to template-based PRD[/yellow]")

    # Save PRD to file
    project_name = interview_answers.get("project_name", "untitled")
    docs_dir = output_path / "docs"
    docs_dir.mkdir(exist_ok=True)

    if prd_content:
        prd_path = docs_dir / f"prd-{project_name.lower().replace(' ', '-')}.md"
        prd_path.write_text(prd_content)
        console.print(f"[green]✓ PRD saved:[/green] {prd_path}")
    else:
        # Generate a basic PRD from interview answers
        from generator.src.requirements.generator import RequirementsGenerator

        req_gen = RequirementsGenerator()
        prd_content = req_gen.generate(interview_answers, "new-project", [], "quick")
        prd_path = docs_dir / f"prd-{project_name.lower().replace(' ', '-')}.md"
        prd_path.write_text(prd_content)
        console.print(f"[yellow]⚠ Template PRD saved:[/yellow] {prd_path}")

    # Phase 3: Parse PRD and extract stack
    console.print("\n[bold blue]Phase 3: Analyzing PRD[/bold blue]")

    parser = PRDParser()
    parsed_prd = parser.parse(prd_content)

    stack_extractor = StackExtractor()
    stack_info = stack_extractor.extract_from_prd(parsed_prd)
    suggested_rules = stack_extractor.suggest_rules(parsed_prd)

    console.print(f"[green]✓ Detected stack:[/green] {stack_info['id']}")
    console.print(f"[dim]Architecture: {stack_info['architecture']}[/dim]")
    console.print(f"[dim]Suggested rules: {len(suggested_rules)} categories[/dim]")

    # Phase 4: Compile rules
    console.print("\n[bold blue]Phase 4: Compiling Rules[/bold blue]")

    library_path = Path("/Users/dars/Development/opencode-projects/experiment/rulesmith-library")
    compiler = RuleCompiler(library_path)

    final_stack = stack_info["id"]
    compiled_rules = compiler.compile(final_stack, interview_answers)

    console.print(f"[green]✓ Compiled {len(compiled_rules)} rules[/green]")

    # Phase 5: Generate formatted rules for AI tools
    console.print("\n[bold blue]Phase 5: Generating AI Assistant Rules[/bold blue]")

    project_context = {
        "name": project_name,
        "stack": final_stack,
        "stack_info": stack_info,
        "interview_answers": interview_answers,
        "parsed_prd": parsed_prd,
    }

    # Get target tools from interview
    primary_tool = interview_answers.get("primary_ai_tool", "cursor")
    secondary_tools = interview_answers.get("secondary_tools", [])
    if secondary_tools is None:
        secondary_tools = []

    target_tools = [primary_tool.lower().replace(" ", "")]
    for tool in secondary_tools:
        tool_id = tool.lower().replace(" ", "").replace(".dev", "")
        if tool_id and tool_id not in target_tools and tool_id != "none":
            target_tools.append(tool_id)

    # Map to internal tool IDs
    tool_mapping = {
        "cursor": "cursor",
        "claude": "claude",
        "claudecode": "claude",
        "githubcopilot": "copilot",
        "copilot": "copilot",
        "roo": "roo",
        "roocode": "roo",
        "continue": "continue",
        "continuedev": "continue",
        "multiple": "cursor",  # Default to cursor if multiple
    }

    mapped_tools = []
    for tool in target_tools:
        mapped = tool_mapping.get(tool, tool)
        if mapped not in mapped_tools:
            mapped_tools.append(mapped)

    sync_engine = SyncEngine(compiled_rules, project_context, output_path, mapped_tools)
    results = sync_engine.sync_all()

    # Display results
    success_count = sum(1 for r in results.values() if r.get("success"))
    console.print(f"[green]✓ Generated rules for {success_count}/{len(mapped_tools)} tools[/green]")

    for tool_id, result in results.items():
        if result.get("success"):
            files = result.get("files_created", [])
            console.print(f"  [dim]{tool_id}:[/dim] {len(files)} files created")
        else:
            console.print(
                f"  [red]{tool_id}: Failed - {result.get('error', 'Unknown error')}[/red]"
            )

    # Save configuration
    config_manager = ConfigManager(output_path)
    config = config_manager.create_config(
        project_name=project_name,
        detected_stack=final_stack,
        stack_confidence=0.9,
        detected_signals=stack_info,
        generation_mode="guided" if guided else "quick",
        selected_stack=final_stack,
    )
    config_manager.save(config)

    console.print(f"\n[green]✓ Configuration saved:[/green] {config_manager.config_path}")

    # Final summary
    console.print("\n" + "=" * 60)
    console.print("[bold green]🎉 Project Setup Complete![/bold green]")
    console.print("=" * 60)
    console.print(f"\n[bold]Project:[/bold] {project_name}")
    console.print(f"[bold]Location:[/bold] {output_path}")
    console.print(f"[bold]Stack:[/bold] {final_stack}")
    console.print(f"[bold]PRD:[/bold] {prd_path}")
    console.print(f"[bold]AI Tools:[/bold] {', '.join(mapped_tools)}")
    console.print("\n[bold yellow]Next steps:[/bold yellow]")
    console.print("  1. Review the generated PRD in docs/")
    console.print("  2. Review AI assistant rules in respective directories")
    console.print("  3. Start coding with your AI assistant!")
    console.print("")
