"""Skill context - Manages execution context for skills.

Provides context management for skill execution including
variables, state, and references.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class SkillContext:
    """Context for skill execution.

    Maintains state and variables for skill execution sessions.
    """

    # Session information
    session_id: str = field(default_factory=lambda: "")
    project_path: Optional[Path] = None

    # Active skills
    active_skills: List[str] = field(default_factory=list)

    # Context variables
    variables: Dict[str, Any] = field(default_factory=dict)

    # Execution state
    state: Dict[str, Any] = field(default_factory=dict)

    def set_variable(self, key: str, value: Any) -> None:
        """Set a context variable.

        Args:
            key: Variable name
            value: Variable value
        """
        self.variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        """Get a context variable.

        Args:
            key: Variable name
            default: Default value if not found

        Returns:
            Variable value or default
        """
        return self.variables.get(key, default)

    def has_variable(self, key: str) -> bool:
        """Check if a variable exists.

        Args:
            key: Variable name

        Returns:
            True if variable exists
        """
        return key in self.variables

    def set_state(self, key: str, value: Any) -> None:
        """Set execution state.

        Args:
            key: State key
            value: State value
        """
        self.state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get execution state.

        Args:
            key: State key
            default: Default value if not found

        Returns:
            State value or default
        """
        return self.state.get(key, default)

    def add_active_skill(self, skill_name: str) -> None:
        """Add a skill to active skills.

        Args:
            skill_name: Name of the skill
        """
        if skill_name not in self.active_skills:
            self.active_skills.append(skill_name)

    def remove_active_skill(self, skill_name: str) -> None:
        """Remove a skill from active skills.

        Args:
            skill_name: Name of the skill
        """
        if skill_name in self.active_skills:
            self.active_skills.remove(skill_name)

    def is_skill_active(self, skill_name: str) -> bool:
        """Check if a skill is active.

        Args:
            skill_name: Name of the skill

        Returns:
            True if skill is active
        """
        return skill_name in self.active_skills

    def clear(self) -> None:
        """Clear all context data."""
        self.variables.clear()
        self.state.clear()
        self.active_skills.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary.

        Returns:
            Dictionary representation of context
        """
        return {
            "session_id": self.session_id,
            "project_path": str(self.project_path) if self.project_path else None,
            "active_skills": self.active_skills,
            "variables": self.variables,
            "state": self.state,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillContext":
        """Create context from dictionary.

        Args:
            data: Dictionary with context data

        Returns:
            New SkillContext instance
        """
        ctx = cls()
        ctx.session_id = data.get("session_id", "")
        ctx.project_path = Path(data["project_path"]) if data.get("project_path") else None
        ctx.active_skills = data.get("active_skills", [])
        ctx.variables = data.get("variables", {})
        ctx.state = data.get("state", {})
        return ctx
