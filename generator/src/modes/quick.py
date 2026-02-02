"""
Quick mode for Rulesmith Generator.
Fast configuration with minimal questions.
"""

from typing import Any, Dict, List

from rulesmith.generator.src.models.interview import Question, QuestionType


QUICK_QUESTIONS: List[Question] = [
    Question(
        id="confirm_stack",
        type=QuestionType.CONFIRM,
        text="Detected stack looks correct?",
        description="Accept the detected technology stack",
        default=True,
        required=True,
    ),
    Question(
        id="project_purpose",
        type=QuestionType.TEXT,
        text="What's the main purpose of this project?",
        description="Brief description of what the project does",
        default="",
        required=True,
    ),
    Question(
        id="team_size",
        type=QuestionType.CHOICE,
        text="What's your team size?",
        options=["Solo", "Small (2-5)", "Medium (6-15)", "Large (16+)"],
        default="Small (2-5)",
        required=True,
    ),
    Question(
        id="priority_constraint",
        type=QuestionType.CHOICE,
        text="What's your top priority constraint?",
        options=["Security", "Performance", "Maintainability", "Compliance", "Time-to-market"],
        default="Maintainability",
        required=True,
    ),
    Question(
        id="target_tools",
        type=QuestionType.MULTIPLE_CHOICE,
        text="Which tools do you want configured?",
        options=["ESLint", "Prettier", "TypeScript", "Testing", "CI/CD", "Docker", "Documentation"],
        default=["ESLint", "Prettier"],
        required=False,
    ),
]


class QuickMode:
    """Quick configuration mode with minimal questions."""

    def __init__(self, detected_stack: Dict[str, Any]):
        self.detected_stack = detected_stack

    def get_questions(self) -> List[Question]:
        """Prepare questions with context from detected stack."""
        questions = []

        for q in QUICK_QUESTIONS:
            question_data = q.model_dump()

            if q.id == "confirm_stack":
                stack_str = ", ".join(f"{k}: {v}" for k, v in self.detected_stack.items())
                question_data["description"] = f"Detected: {stack_str}"

            questions.append(Question(**question_data))

        return questions
