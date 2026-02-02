"""Sync engine for multiple formatters."""

from pathlib import Path
from typing import Any, Dict, List

from formatters.src.base import FormatterConfig
from formatters.src.registry import get_formatter


class SyncEngine:
    """Synchronizes rules across multiple AI tools."""

    def __init__(
        self,
        compiled_rules: List[Dict[str, Any]],
        project_context: Dict[str, Any],
        project_root: Path,
        target_tools: List[str],
    ):
        self.rules = compiled_rules
        self.context = project_context
        self.project_root = project_root
        self.target_tools = target_tools

    def sync_all(self) -> Dict[str, Dict[str, Any]]:
        """Generate rules for all target tools."""
        results: Dict[str, Dict[str, Any]] = {}

        for tool_id in self.target_tools:
            try:
                formatter_class = get_formatter(tool_id)
                formatter = formatter_class(FormatterConfig())

                result = formatter.format_rules(self.rules, self.context, self.project_root)

                results[tool_id] = {
                    "success": result.success,
                    "files_created": [str(f) for f in result.files_created],
                    "files_updated": [str(f) for f in result.files_updated],
                    "errors": result.errors,
                }

            except Exception as e:
                results[tool_id] = {"success": False, "error": str(e)}

        return results

    def validate_all(self) -> Dict[str, bool]:
        """Validate all generated outputs."""
        validations: Dict[str, bool] = {}

        for tool_id in self.target_tools:
            try:
                formatter_class = get_formatter(tool_id)
                formatter = formatter_class(FormatterConfig())

                # Determine validation path based on formatter
                if tool_id == "cursor":
                    path = self.project_root / ".cursor" / "rules"
                elif tool_id == "claude":
                    path = self.project_root / "CLAUDE.md"
                else:
                    validations[tool_id] = False
                    continue

                validations[tool_id] = formatter.validate_output(path)

            except Exception:
                validations[tool_id] = False

        return validations
