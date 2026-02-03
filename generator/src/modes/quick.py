"""Quick mode: 3-5 question interview."""

from typing import Dict, Any, List
from rich.console import Console
from ..interview.engine import InterviewEngine
from ..interview.questions import QUICK_QUESTIONS
from ..models.interview import Question


class QuickMode:
    """Quick 3-5 question interview mode."""

    def __init__(self, detected_stack: str, console: Console = None):
        self.detected_stack = detected_stack
        self.engine = InterviewEngine(self._prepare_questions(), console)

    def _prepare_questions(self) -> List[Question]:
        """Inject detected stack into question text."""
        questions = []
        for q in QUICK_QUESTIONS:
            question_data = q.model_dump()
            if "{detected_stack}" in question_data.get("text", ""):
                question_data["text"] = question_data["text"].format(
                    detected_stack=self.detected_stack
                )
            questions.append(Question(**question_data))
        return questions

    def run(self) -> Dict[str, Any]:
        """Run quick interview and return answers."""
        return self.engine.run()
