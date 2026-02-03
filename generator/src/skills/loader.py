"""Skill loader - Loads skills from disk.

Handles parsing SKILL.md files and extracting metadata.
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class SkillMetadata:
    """Metadata for a skill."""

    name: str
    description: str
    license: Optional[str] = None
    compatibility: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class Skill:
    """A loaded skill with metadata and content."""

    name: str
    path: Path
    metadata: SkillMetadata
    content: str
    references: Optional[Path] = None
    scripts: Optional[Path] = None
    assets: Optional[Path] = None


class SkillLoader:
    """Loads skills from the filesystem."""

    def __init__(self, skills_path: Path):
        """Initialize loader with path to skills directory.

        Args:
            skills_path: Path to skills directory (e.g., ~/.rulesmith/libraries/skills/)
        """
        self.skills_path = skills_path

    def load_skill(self, skill_name: str) -> Optional[Skill]:
        """Load a single skill by name.

        Args:
            skill_name: Name of the skill directory

        Returns:
            Skill object or None if not found
        """
        skill_dir = self.skills_path / skill_name

        if not skill_dir.exists():
            return None

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            return None

        # Parse the SKILL.md file
        content = skill_file.read_text()
        metadata = self._parse_metadata(content)

        if not metadata:
            return None

        # Check for optional directories
        references_dir = skill_dir / "references" if (skill_dir / "references").exists() else None
        scripts_dir = skill_dir / "scripts" if (skill_dir / "scripts").exists() else None
        assets_dir = skill_dir / "assets" if (skill_dir / "assets").exists() else None

        return Skill(
            name=metadata.name,
            path=skill_dir,
            metadata=metadata,
            content=content,
            references=references_dir,
            scripts=scripts_dir,
            assets=assets_dir,
        )

    def load_all_skills(self) -> List[Skill]:
        """Load all available skills.

        Returns:
            List of Skill objects
        """
        skills = []

        if not self.skills_path.exists():
            return skills

        # Iterate through all directories in skills path
        for skill_dir in self.skills_path.iterdir():
            if skill_dir.is_dir():
                skill = self.load_skill(skill_dir.name)
                if skill:
                    skills.append(skill)

        return skills

    def _parse_metadata(self, content: str) -> Optional[SkillMetadata]:
        """Parse YAML frontmatter from SKILL.md content.

        Args:
            content: Full content of SKILL.md

        Returns:
            SkillMetadata or None if parsing fails
        """
        # Look for YAML frontmatter between --- markers
        pattern = r"^---\s*\n(.*?)\n---\s*\n"
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return None

        yaml_content = match.group(1)

        # Parse YAML content manually (simple parser for key: value pairs)
        data = {}
        current_key = None
        current_value = []

        for line in yaml_content.split("\n"):
            line = line.rstrip()

            # Check for new key (starts at column 0 with colon)
            if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
                # Save previous key-value pair
                if current_key:
                    data[current_key] = "\n".join(current_value).strip()

                # Parse new key-value
                key, value = line.split(":", 1)
                current_key = key.strip()
                current_value = [value.strip()] if value.strip() else []
            elif current_key:
                # Continuation of previous value
                current_value.append(line)

        # Save last key-value pair
        if current_key:
            data[current_key] = "\n".join(current_value).strip()

        # Extract required fields
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()

        if not name or not description:
            return None

        # Parse metadata dict if present
        metadata_dict = None
        if "metadata" in data:
            # Simple parsing for metadata section
            metadata_dict = {}
            for line in data["metadata"].split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata_dict[k.strip()] = v.strip()

        return SkillMetadata(
            name=name,
            description=description,
            license=data.get("license"),
            compatibility=data.get("compatibility"),
            metadata=metadata_dict,
        )

    def skill_exists(self, skill_name: str) -> bool:
        """Check if a skill exists.

        Args:
            skill_name: Name of the skill

        Returns:
            True if skill exists
        """
        skill_dir = self.skills_path / skill_name
        skill_file = skill_dir / "SKILL.md"
        return skill_file.exists()

    def get_skill_content(self, skill_name: str) -> Optional[str]:
        """Get just the content of a skill (without frontmatter).

        Args:
            skill_name: Name of the skill

        Returns:
            Skill content or None
        """
        skill = self.load_skill(skill_name)
        if not skill:
            return None

        # Remove frontmatter from content
        pattern = r"^---\s*\n.*?\n---\s*\n"
        content = re.sub(pattern, "", skill.content, flags=re.DOTALL)
        return content.strip()
