"""Skill registry - Manages skill discovery and registration.

Provides a centralized registry for available skills with filtering
and search capabilities.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from .loader import SkillLoader, Skill, SkillMetadata


@dataclass
class SkillInfo:
    """Lightweight skill information for registry."""

    name: str
    description: str
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    loaded: bool = False


class SkillRegistry:
    """Registry for managing available skills."""

    def __init__(self, skills_path: Path):
        """Initialize registry.

        Args:
            skills_path: Path to skills directory
        """
        self.loader = SkillLoader(skills_path)
        self.skills_path = skills_path
        self._skills: Dict[str, Skill] = {}
        self._skill_info: Dict[str, SkillInfo] = {}
        self._loaded = False

    def load_index(self) -> None:
        """Load skill index from index.yaml if available."""
        index_file = self.skills_path / "index.yaml"

        if not index_file.exists():
            # No index file, scan directory instead
            self._scan_directory()
            return

        # Parse index.yaml
        import yaml

        try:
            with open(index_file, "r") as f:
                index = yaml.safe_load(f)

            # Load skills from index
            for skill_data in index.get("skills", []):
                name = skill_data.get("name", "")
                if name:
                    self._skill_info[name] = SkillInfo(
                        name=name,
                        description=skill_data.get("description", ""),
                        category=skill_data.get("category"),
                        tags=skill_data.get("tags", []),
                        loaded=False,
                    )
        except Exception:
            # Fall back to directory scan
            self._scan_directory()

    def _scan_directory(self) -> None:
        """Scan skills directory and build index."""
        if not self.skills_path.exists():
            return

        for skill_dir in self.skills_path.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    # Quick metadata extraction
                    try:
                        content = skill_file.read_text()
                        metadata = self.loader._parse_metadata(content)
                        if metadata:
                            self._skill_info[metadata.name] = SkillInfo(
                                name=metadata.name,
                                description=metadata.description,
                                loaded=False,
                            )
                    except Exception:
                        pass

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name (loads if not already loaded).

        Args:
            name: Skill name

        Returns:
            Skill object or None
        """
        if name in self._skills:
            return self._skills[name]

        # Load the skill
        skill = self.loader.load_skill(name)
        if skill:
            self._skills[name] = skill
            # Update info
            if name in self._skill_info:
                self._skill_info[name].loaded = True

        return skill

    def list_skills(
        self, category: Optional[str] = None, tag: Optional[str] = None
    ) -> List[SkillInfo]:
        """List available skills with optional filtering.

        Args:
            category: Filter by category
            tag: Filter by tag

        Returns:
            List of skill info objects
        """
        if not self._skill_info:
            self.load_index()

        skills = list(self._skill_info.values())

        # Apply filters
        if category:
            skills = [s for s in skills if s.category == category]

        if tag:
            skills = [s for s in skills if tag in s.tags]

        return skills

    def search_skills(self, query: str) -> List[SkillInfo]:
        """Search skills by name or description.

        Args:
            query: Search query

        Returns:
            List of matching skills
        """
        if not self._skill_info:
            self.load_index()

        query = query.lower()
        results = []

        for info in self._skill_info.values():
            if query in info.name.lower() or query in info.description.lower():
                results.append(info)

        return results

    def get_categories(self) -> List[str]:
        """Get all available categories.

        Returns:
            List of category names
        """
        if not self._skill_info:
            self.load_index()

        categories = set()
        for info in self._skill_info.values():
            if info.category:
                categories.add(info.category)

        return sorted(list(categories))

    def get_tags(self) -> List[str]:
        """Get all available tags.

        Returns:
            List of tag names
        """
        if not self._skill_info:
            self.load_index()

        tags = set()
        for info in self._skill_info.values():
            tags.update(info.tags)

        return sorted(list(tags))

    def skill_exists(self, name: str) -> bool:
        """Check if a skill exists in the registry.

        Args:
            name: Skill name

        Returns:
            True if skill exists
        """
        if not self._skill_info:
            self.load_index()

        return name in self._skill_info

    def get_skill_info(self, name: str) -> Optional[SkillInfo]:
        """Get skill info without loading full skill.

        Args:
            name: Skill name

        Returns:
            SkillInfo or None
        """
        if not self._skill_info:
            self.load_index()

        return self._skill_info.get(name)

    def refresh(self) -> None:
        """Refresh the registry (reload from disk)."""
        self._skills.clear()
        self._skill_info.clear()
        self._loaded = False
        self.load_index()

    def get_loaded_skills(self) -> List[Skill]:
        """Get all currently loaded skills.

        Returns:
            List of loaded Skill objects
        """
        return list(self._skills.values())
