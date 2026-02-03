"""Models for requirements document generation."""

from typing import Any, Dict, Optional
from pydantic import BaseModel
from datetime import datetime


class RequirementsDocument(BaseModel):
    """Requirements document model."""

    content: str
    timestamp: datetime
    project_name: Optional[str] = None
    detected_stack: str
    generation_mode: str
    total_rules: int
    interview_answers: Dict[str, Any]
