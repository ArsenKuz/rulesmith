"""Skill executor - Executes skill workflows.

Handles the execution of skills within the AI context.
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from .loader import SkillLoader, Skill


@dataclass
class ExecutionResult:
    """Result of skill execution."""

    success: bool
    message: str
    context_updates: Optional[Dict[str, Any]] = None


class SkillExecutor:
    """Executes skills and manages their context."""

    def __init__(self, skills_path: Path):
        """Initialize executor.

        Args:
            skills_path: Path to skills directory
        """
        self.loader = SkillLoader(skills_path)
        self.skills_path = skills_path
        self._active_skills: Dict[str, Skill] = {}

    def load_skill(self, skill_name: str) -> ExecutionResult:
        """Load a skill into the active context.

        Args:
            skill_name: Name of the skill to load

        Returns:
            Execution result
        """
        # Check if already loaded
        if skill_name in self._active_skills:
            return ExecutionResult(
                success=True,
                message=f"Skill '{skill_name}' is already loaded",
            )

        # Load the skill
        skill = self.loader.load_skill(skill_name)

        if not skill:
            return ExecutionResult(
                success=False,
                message=f"Skill '{skill_name}' not found",
            )

        # Add to active skills
        self._active_skills[skill_name] = skill

        return ExecutionResult(
            success=True,
            message=f"Loaded skill: {skill.metadata.description}",
            context_updates={
                "skill_name": skill_name,
                "skill_description": skill.metadata.description,
            },
        )

    def unload_skill(self, skill_name: str) -> ExecutionResult:
        """Unload a skill from the active context.

        Args:
            skill_name: Name of the skill to unload

        Returns:
            Execution result
        """
        if skill_name not in self._active_skills:
            return ExecutionResult(
                success=False,
                message=f"Skill '{skill_name}' is not loaded",
            )

        del self._active_skills[skill_name]

        return ExecutionResult(
            success=True,
            message=f"Unloaded skill: {skill_name}",
        )

    def get_active_skills(self) -> List[Skill]:
        """Get all currently active skills.

        Returns:
            List of active skills
        """
        return list(self._active_skills.values())

    def get_skill_context(self, skill_name: Optional[str] = None) -> str:
        """Get the context content for active skill(s).

        Args:
            skill_name: Specific skill to get context for, or None for all

        Returns:
            Context content string
        """
        if skill_name:
            # Get specific skill context
            skill = self._active_skills.get(skill_name)
            if skill:
                return self.loader.get_skill_content(skill_name) or ""
            return ""

        # Get all active skills context
        contexts = []
        for name in self._active_skills:
            content = self.loader.get_skill_content(name)
            if content:
                contexts.append(f"\n## Skill: {name}\n\n{content}")

        return "\n".join(contexts)

    def is_skill_active(self, skill_name: str) -> bool:
        """Check if a skill is currently active.

        Args:
            skill_name: Name of the skill

        Returns:
            True if skill is active
        """
        return skill_name in self._active_skills

    def clear_all(self) -> ExecutionResult:
        """Clear all active skills.

        Returns:
            Execution result
        """
        count = len(self._active_skills)
        self._active_skills.clear()

        return ExecutionResult(
            success=True,
            message=f"Cleared {count} active skill(s)",
        )

    def get_skill_scripts(self, skill_name: str) -> Optional[Path]:
        """Get the scripts directory for a skill.

        Args:
            skill_name: Name of the skill

        Returns:
            Path to scripts directory or None
        """
        skill = self._active_skills.get(skill_name)
        if skill:
            return skill.scripts
        return None

    def get_skill_references(self, skill_name: str) -> Optional[Path]:
        """Get the references directory for a skill.

        Args:
            skill_name: Name of the skill

        Returns:
            Path to references directory or None
        """
        skill = self._active_skills.get(skill_name)
        if skill:
            return skill.references
        return None

    def get_skill_assets(self, skill_name: str) -> Optional[Path]:
        """Get the assets directory for a skill.

        Args:
            skill_name: Name of the skill

        Returns:
            Path to assets directory or None
        """
        skill = self._active_skills.get(skill_name)
        if skill:
            return skill.assets
        return None
