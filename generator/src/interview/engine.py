"""Interview engine for asking questions and collecting responses."""

from typing import Any, List
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from ..models.interview import Question, QuestionType, InterviewState


class InterviewEngine:
    """Engine for conducting interviews."""

    def __init__(self, questions: List[Question], console: Console = None):
        self.questions = questions
        self.state = InterviewState()
        self.console = console or Console()

    def run(self) -> dict[str, Any]:
        """Run the interview and return collected answers."""
        self.console.print(
            Panel.fit(
                "[bold blue]AI Rules Generator[/bold blue]\n"
                "Let's create custom AI rules for your project!",
                border_style="blue",
            )
        )

        while self.state.current_question < len(self.questions):
            question = self.questions[self.state.current_question]

            # Check skip condition
            if question.skip_if and self._evaluate_condition(question.skip_if):
                self.state.current_question += 1
                continue

            # Ask question
            answer = self._ask_question(question)

            if answer is None and question.required:
                self.console.print("[red]This question is required.[/red]")
                continue

            # Store answer
            self.state.answers[question.id] = answer
            self.state.history.append({"question": question.id, "answer": answer})
            self.state.current_question += 1

        return self.state.answers

    def _ask_question(self, question: Question) -> Any:
        """Render a single question based on type."""
        # Display question
        self.console.print(f"\n[bold]{question.text}[/bold]")
        if question.description:
            self.console.print(f"[dim]{question.description}[/dim]")

        # Render based on type
        if question.type == QuestionType.TEXT:
            return Prompt.ask("Your answer", default=question.default)

        elif question.type == QuestionType.CHOICE:
            return self._ask_choice(question.options, question.default)

        elif question.type == QuestionType.MULTIPLE_CHOICE:
            return self._ask_multiple_choice(question.options, question.default)

        elif question.type == QuestionType.CONFIRM:
            return Confirm.ask(question.text, default=question.default or False)

        elif question.type == QuestionType.PATH:
            path = Prompt.ask("Path", default=question.default)
            return Path(path).expanduser().resolve()

        return None

    def _ask_choice(self, options: List[str], default: Any = None) -> str:
        """Ask a single choice question."""
        if not options:
            return None

        # Display options
        for i, option in enumerate(options, 1):
            self.console.print(f"  [{i}] {option}")

        default_num = None
        if default and default in options:
            default_num = options.index(default) + 1

        prompt_text = "Enter number"
        if default_num:
            choice = IntPrompt.ask(prompt_text, default=default_num)
        else:
            choice = IntPrompt.ask(prompt_text)

        if 1 <= choice <= len(options):
            return options[choice - 1]
        return None

    def _ask_multiple_choice(
        self, options: List[str], default: Any = None
    ) -> List[str]:
        """Ask a multiple choice question."""
        if not options:
            return []

        # Display options
        self.console.print(
            "[dim]Select multiple by entering numbers separated by commas (e.g., 1,3,5)[/dim]"
        )
        for i, option in enumerate(options, 1):
            self.console.print(f"  [{i}] {option}")

        # Get input
        default_str = None
        if default and isinstance(default, list):
            default_nums = [str(options.index(d) + 1) for d in default if d in options]
            if default_nums:
                default_str = ",".join(default_nums)

        if default_str:
            response = Prompt.ask("Enter numbers", default=default_str)
        else:
            response = Prompt.ask("Enter numbers")

        # Parse response
        selected = []
        try:
            for num_str in response.split(","):
                num = int(num_str.strip())
                if 1 <= num <= len(options):
                    selected.append(options[num - 1])
        except ValueError:
            pass

        return selected

    def _evaluate_condition(self, condition: str) -> bool:
        """Evaluate a skip condition against current answers."""
        # Simple condition evaluation
        # Format: "question_id == value" or "question_id != value"
        # or "question_id contains value"
        try:
            if "==" in condition:
                parts = condition.split("==")
                qid = parts[0].strip()
                expected = parts[1].strip().strip('"').lower()
                actual = str(self.state.answers.get(qid, "")).lower()
                return actual == expected or actual == "true"

            elif "!=" in condition:
                parts = condition.split("!=")
                qid = parts[0].strip()
                expected = parts[1].strip().strip('"').lower()
                actual = str(self.state.answers.get(qid, "")).lower()
                return actual != expected

            elif "contains" in condition:
                parts = condition.split("contains")
                qid = parts[0].strip()
                search = parts[1].strip().strip('"').lower()
                actual = str(self.state.answers.get(qid, "")).lower()
                return search in actual
        except Exception:
            pass

        return False
