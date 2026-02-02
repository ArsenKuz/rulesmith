"""Configuration schema for Rulesmith."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    """Configuration for a rulesmith-managed project."""

    version: str = Field(default="1.0.0", description="Config schema version")
    project_name: str = Field(description="Project name")
    project_root: Path = Field(description="Absolute path to project root")

    # Detection results
    detected_stack: str = Field(description="Primary detected stack ID")
    stack_confidence: float = Field(ge=0, le=1, description="Detection confidence (0-1)")
    detected_signals: Dict[str, Any] = Field(
        default_factory=dict, description="Raw detection signals"
    )

    # User overrides
    selected_stack: Optional[str] = Field(None, description="User-selected stack if different")

    # Generation settings
    generation_mode: str = Field(default="quick", description="quick or guided")
    active_formatters: List[str] = Field(
        default_factory=lambda: ["cursor", "claude", "copilot"],
        description="Which AI tools to generate rules for",
    )

    # Library tracking
    library_version: Optional[str] = Field(None, description="Version of rule library used")
    library_updated_at: Optional[datetime] = Field(None, description="Last library update")

    # Project metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {"populate_by_name": True}


class StackResult(BaseModel):
    """Result of stack detection."""

    primary: str = Field(description="Primary detected stack ID")
    confidence: float = Field(ge=0, le=1, description="Detection confidence")
    all_signals: Dict[str, Any] = Field(default_factory=dict, description="All detected signals")
    scores: Dict[str, float] = Field(default_factory=dict, description="Score for each stack")


class FormatterConfig(BaseModel):
    """Configuration for a formatter."""

    enabled: bool = Field(default=True)
    output_path: Optional[Path] = Field(default=None)
    tool_specific_options: Dict[str, Any] = Field(default_factory=dict)
