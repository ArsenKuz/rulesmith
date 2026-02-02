"""
Interview engine for Rulesmith Generator.
Handles the interactive questioning flow.
"""

from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.prompt import Confirm, IntPrompt, Prompt

from rulesmith.generator.src.models.interview import InterviewState, Question, QuestionType


class InterviewEngine:
    """Engine for conducting interactive interviews."""

    def __init__(self, questions: List[Question], console: Console):
        self.questions = {q.id: q for q in questions}
        self.questions_order = [q.id for q in questions]
        self.console = console
        self.state = InterviewState()

    def run(self) -> Dict[str, Any]:
        """Run the interview and return all answers."""
        self.console.print("[bold blue]Rulesmith Configuration Interview[/bold blue]")
        self.console.print("=" * 50)
        self.console.print()

        for question_id in self.questions_order:
            question = self.questions[question_id]

            if self.state.should_skip(question):
                continue

            self.state.current_question = question_id
            answer = self._ask_question(question)
            self.state.record_answer(question_id, answer)

        self.console.print()
        self.console.print("[bold green]Interview complete![/bold green]")

        return self.state.answers

    def _ask_question(self, question: Question) -> Any:
        """Ask a single question based on its type."""
        if question.description:
            self.console.print(f"[dim]{question.description}[/dim]")

        if question.type == QuestionType.TEXT:
            return self._ask_text(question)
        elif question.type == QuestionType.CHOICE:
            return self._ask_choice(question)
        elif question.type == QuestionType.MULTIPLE_CHOICE:
            return self._ask_multiple_choice(question)
        elif question.type == QuestionType.CONFIRM:
            return self._ask_confirm(question)
        elif question.type == QuestionType.PATH:
            return self._ask_path(question)
        else:
            return self._ask_text(question)

    def _ask_text(self, question: Question) -> str:
        """Ask a text question."""
        default = question.default if question.default is not None else ""

        if question.required:
            return Prompt.ask(
                f"[bold]{question.text}[/bold]", default=default, console=self.console
            )
        else:
            result = Prompt.ask(
                f"[bold]{question.text}[/bold] (optional)", default=default, console=self.console
            )
            return result if result else None

    def _ask_choice(self, question: Question) -> str:
        """Ask a single choice question."""
        self.console.print(f"[bold]{question.text}[/bold]")

        for i, option in enumerate(question.options or [], 1):
            self.console.print(f"  {i}. {option}")

        default_idx = 1
        if question.default and question.options:
            try:
                default_idx = question.options.index(question.default) + 1
            except ValueError:
                default_idx = 1

        choice = IntPrompt.ask("Enter number", default=default_idx, console=self.console)

        if question.options and 1 <= choice <= len(question.options):
            return question.options[choice - 1]
        return question.options[0] if question.options else ""

    def _ask_multiple_choice(self, question: Question) -> List[str]:
        """Ask a multiple choice question."""
        self.console.print(f"[bold]{question.text}[/bold]")
        self.console.print("[dim]Enter numbers separated by commas (e.g., 1,3,4)[/dim]")

        for i, option in enumerate(question.options or [], 1):
            self.console.print(f"  {i}. {option}")

        if not question.required:
            self.console.print("  0. None / Skip")

        default_str = ""
        if question.default and question.options:
            if isinstance(question.default, list):
                try:
                    indices = [str(question.options.index(d) + 1) for d in question.default]
                    default_str = ",".join(indices)
                except ValueError:
                    default_str = ""

        response = Prompt.ask("Enter numbers", default=default_str, console=self.console)

        if not response:
            return []

        try:
            indices = [int(x.strip()) for x in response.split(",")]
            if 0 in indices:
                return []
            selected = []
            for idx in indices:
                if question.options and 1 <= idx <= len(question.options):
                    selected.append(question.options[idx - 1])
            return selected
        except ValueError:
            return []

    def _ask_confirm(self, question: Question) -> bool:
        """Ask a yes/no confirmation question."""
        default = question.default if isinstance(question.default, bool) else True
        return Confirm.ask(f"[bold]{question.text}[/bold]", default=default, console=self.console)

    def _ask_path(self, question: Question) -> str:
        """Ask for a file/directory path."""
        default = question.default if question.default is not None else "."
        return Prompt.ask(f"[bold]{question.text}[/bold]", default=default, console=self.console)
