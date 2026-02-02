"""Utilities module."""

from pathlib import Path
from typing import Optional


def get_project_root(path: Optional[Path] = None) -> Path:
    """Get the project root path."""
    if path is None:
        path = Path.cwd()
    return path.resolve()


def find_git_root(path: Path) -> Optional[Path]:
    """Find the git repository root from a path."""
    current = path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return None
