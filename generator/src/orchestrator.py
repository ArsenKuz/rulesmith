"""Main orchestrator for the generator workflow."""

from typing import Dict, Any
from pathlib import Path
from rich.console import Console
from .modes.quick import QuickMode
from .modes.guided import GuidedMode
from .assembly.compiler import RuleCompiler
from .requirements.generator import RequirementsGenerator


class GeneratorOrchestrator:
    """Orchestrates the entire rule generation workflow."""

    def __init__(
        self,
        detected_stack: str,
        library_path: Path,
        generation_mode: str = "quick",
        console: Console = None,
    ):
        self.detected_stack = detected_stack
        self.library_path = library_path
        self.generation_mode = generation_mode
        self.console = console or Console()

        # Initialize components
        if generation_mode == "quick":
            self.interview = QuickMode(detected_stack, self.console)
        else:
            self.interview = GuidedMode(detected_stack, self.console)

        self.compiler = RuleCompiler(library_path)
        self.requirements_gen = RequirementsGenerator()

    def run(self) -> Dict[str, Any]:
        """Execute full generation workflow."""
        # Phase 1: Interview
        if self.console:
            self.console.print("\n[bold green]Phase 1: Project Interview[/bold green]")
        answers = self.interview.run()

        # Determine final stack
        final_stack = answers.get("manual_stack", self.detected_stack)

        # Phase 2: Compile Rules
        if self.console:
            self.console.print("\n[bold green]Phase 2: Compiling Rules[/bold green]")
        compiled_rules = self.compiler.compile(final_stack, answers)

        if self.console:
            self.console.print(f"  Compiled {len(compiled_rules)} rules")

        # Phase 3: Generate Requirements Doc
        if self.console:
            self.console.print(
                "\n[bold green]Phase 3: Generating Requirements[/bold green]"
            )
        requirements = self.requirements_gen.generate(
            answers, final_stack, compiled_rules, self.generation_mode
        )

        return {
            "interview_answers": answers,
            "selected_stack": final_stack,
            "compiled_rules": compiled_rules,
            "requirements_document": requirements,
        }
