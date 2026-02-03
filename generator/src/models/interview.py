"""Interview state and question models."""

from typing import Any, Callable, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    """Question types for interviews."""

    TEXT = "text"
    CHOICE = "choice"
    MULTIPLE_CHOICE = "multiple_choice"
    CONFIRM = "confirm"
    PATH = "path"


class Question(BaseModel):
    """Interview question definition."""

    id: str
    type: QuestionType
    text: str
    description: Optional[str] = None
    options: Optional[List[str]] = None
    default: Optional[Any] = None
    required: bool = True
    validate: Optional[Callable] = None
    skip_if: Optional[str] = None


class InterviewState(BaseModel):
    """State for the interview process."""

    current_question: int = 0
    answers: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)
    history: List[dict] = Field(default_factory=list)
