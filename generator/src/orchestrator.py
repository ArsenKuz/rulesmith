"""Main orchestrator for the Generator."""

from pathlib import Path
from typing import Any, Dict, Optional

from generator.src.assembly.compiler import RuleCompiler
from generator.src.modes.quick import QuickMode


class GeneratorOrchestrator:
    """Orchestrates the entire rule generation workflow."""

    def __init__(
        self,
        detected_stack: str,
        library_path: Path,
        generation_mode: str = "quick",
        console: Any = None,
    ):
        self.detected_stack = detected_stack
        self.library_path = library_path
        self.generation_mode = generation_mode
        self.console = console

        # Initialize components
        if generation_mode == "quick":
            self.interview = QuickMode(detected_stack, console)
        else:
            # For now, default to quick mode if guided not implemented
            self.interview = QuickMode(detected_stack, console)

        self.compiler = RuleCompiler(library_path)

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

        return {
            "interview_answers": answers,
            "selected_stack": final_stack,
            "compiled_rules": compiled_rules,
            "detected_stack": self.detected_stack,
            "confidence": 0.95,  # Placeholder
            "all_signals": {},
            "primary": final_stack,
        }
