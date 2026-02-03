"""Base formatter interface and utilities."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class FormatterConfig:
    """Configuration for a formatter."""

    enabled: bool = True
    output_path: Optional[Path] = None
    tool_specific_options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FormatterResult:
    """Result of formatting operation."""

    success: bool
    files_created: List[Path]
    files_updated: List[Path]
    errors: List[str]


class BaseFormatter(ABC):
    """Abstract base class for all AI tool formatters."""

    # Formatter metadata (must be defined by subclasses)
    name: str = ""
    tool_id: str = ""
    description: str = ""
    file_extension: str = ".md"
    supports_multiple_files: bool = False

    def __init__(self, config: FormatterConfig):
        self.config = config

    @abstractmethod
    def format_rules(
        self,
        compiled_rules: List[Dict[str, Any]],
        project_context: Dict[str, Any],
        output_dir: Path,
    ) -> FormatterResult:
        """
        Format compiled rules for this AI tool.

        Args:
            compiled_rules: List of compiled rules from Generator Agent
            project_context: Project metadata (name, stack, etc.)
            output_dir: Where to write output files

        Returns:
            FormatterResult with operation status
        """
        pass

    @abstractmethod
    def validate_output(self, output_path: Path) -> bool:
        """Validate that generated output is correct."""
        pass

    def get_output_path(self, default_path: Path) -> Path:
        """Get output path (config override or default)."""
        return self.config.output_path or default_path

    def prepare_output_dir(self, path: Path) -> None:
        """Create output directory if needed."""
        path.mkdir(parents=True, exist_ok=True)
