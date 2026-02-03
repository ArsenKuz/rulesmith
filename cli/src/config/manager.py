"""Configuration manager for Rulesmith."""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from .schema import ProjectConfig


class ConfigManager:
    """Manages .rulesmith/config.json files."""

    CONFIG_DIR = ".rulesmith"
    CONFIG_FILE = "config.json"

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path).resolve()
        self.config_path = self.project_path / self.CONFIG_DIR / self.CONFIG_FILE

    def load(self) -> Optional[ProjectConfig]:
        """Load existing configuration or return None."""
        if not self.config_path.exists():
            return None

        with open(self.config_path) as f:
            data = json.load(f)

        # Convert string paths back to Path objects
        if "project_root" in data and isinstance(data["project_root"], str):
            data["project_root"] = Path(data["project_root"])

        # Parse datetime strings
        for field in ["created_at", "updated_at", "library_updated_at"]:
            if field in data and isinstance(data[field], str):
                data[field] = datetime.fromisoformat(data[field])

        return ProjectConfig(**data)

    def save(self, config: ProjectConfig) -> None:
        """Save configuration to disk."""
        config_dir = self.project_path / self.CONFIG_DIR
        config_dir.mkdir(exist_ok=True)

        config.updated_at = datetime.now()

        with open(self.config_path, "w") as f:
            json.dump(config.model_dump(), f, indent=2, default=self._json_serializer)

    def create_config(
        self,
        project_name: str,
        detected_stack: str,
        stack_confidence: float,
        detected_signals: Dict[str, Any],
        generation_mode: str = "quick",
        selected_stack: Optional[str] = None,
    ) -> ProjectConfig:
        """Create a new project configuration."""
        return ProjectConfig(
            project_name=project_name,
            project_root=self.project_path,
            detected_stack=detected_stack,
            stack_confidence=stack_confidence,
            detected_signals=detected_signals,
            generation_mode=generation_mode,
            selected_stack=selected_stack,
        )

    def _json_serializer(self, obj):
        """Custom JSON serializer for special types."""
        if isinstance(obj, Path):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
