"""Configuration manager for Rulesmith."""

import json
from pathlib import Path
from typing import Optional

from .schema import ProjectConfig


class ConfigManager:
    """Manages .rulesmith/config.json files."""

    CONFIG_DIR = ".rulesmith"
    CONFIG_FILE = "config.json"

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.config_path = self.project_path / self.CONFIG_DIR / self.CONFIG_FILE

    def load(self) -> Optional[ProjectConfig]:
        """Load existing configuration or return None."""
        if not self.config_path.exists():
            return None

        with open(self.config_path) as f:
            data = json.load(f)

        # Convert path strings back to Path objects
        if "project_root" in data and isinstance(data["project_root"], str):
            data["project_root"] = Path(data["project_root"])

        return ProjectConfig(**data)

    def save(self, config: ProjectConfig) -> None:
        """Save configuration to disk."""
        config_dir = self.project_path / self.CONFIG_DIR
        config_dir.mkdir(exist_ok=True)

        # Update timestamp
        from datetime import datetime

        config.updated_at = datetime.now()

        with open(self.config_path, "w") as f:
            json.dump(
                config.model_dump(mode="json"),
                f,
                indent=2,
                default=str,
            )

    def exists(self) -> bool:
        """Check if config exists."""
        return self.config_path.exists()

    def delete(self) -> None:
        """Delete configuration."""
        if self.config_path.exists():
            self.config_path.unlink()

    def get_library_path(self) -> Path:
        """Get the library path (from environment or default)."""
        import os

        env_path = os.environ.get("RULESMITH_LIBRARY_PATH")
        if env_path:
            return Path(env_path)

        # Default to parent directory rules
        return self.project_path.parent / "rulesmith-library"
