"""
Interview models for Rulesmith Generator.
Pydantic models for question definitions and interview state.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    """Types of interview questions."""

    TEXT = "text"
    CHOICE = "choice"
    MULTIPLE_CHOICE = "multiple_choice"
    CONFIRM = "confirm"
    PATH = "path"


class Question(BaseModel):
    """A single interview question."""

    id: str = Field(..., description="Unique identifier for the question")
    type: QuestionType = Field(..., description="Type of question")
    text: str = Field(..., description="Question text to display to user")
    description: Optional[str] = Field(default=None, description="Additional help text")
    options: Optional[List[str]] = Field(
        default=None, description="Options for choice/multiple_choice"
    )
    default: Optional[Any] = Field(default=None, description="Default value")
    required: bool = Field(default=True, description="Whether an answer is required")
    skip_if: Optional[str] = Field(
        default=None, description="Question ID to skip if this answer is True"
    )


class InterviewState(BaseModel):
    """Current state of an interview session."""

    current_question: Optional[str] = Field(default=None, description="ID of current question")
    answers: Dict[str, Any] = Field(
        default_factory=dict, description="All answers collected so far"
    )
    context: Dict[str, Any] = Field(
        default_factory=dict, description="Context data from stack detection"
    )
    history: List[str] = Field(default_factory=list, description="Order of questions asked")

    def record_answer(self, question_id: str, answer: Any) -> None:
        """Record an answer and update history."""
        self.answers[question_id] = answer
        if question_id not in self.history:
            self.history.append(question_id)

    def should_skip(self, question: Question) -> bool:
        """Check if a question should be skipped based on skip_if condition."""
        if not question.skip_if:
            return False
        return self.answers.get(question.skip_if, False)
