"""Cursor formatter for .cursor/rules/*.mdc files."""

import yaml
from pathlib import Path
from typing import Any, Dict, List

from formatters.src.base import BaseFormatter, FormatterConfig, FormatterResult


class CursorFormatter(BaseFormatter):
    """Formatter for Cursor IDE .mdc rule files."""

    name = "Cursor"
    tool_id = "cursor"
    description = "Formats rules for Cursor IDE .cursor/rules/*.mdc files"
    file_extension = ".mdc"
    supports_multiple_files = True

    def __init__(self, config: FormatterConfig):
        super().__init__(config)

    def format_rules(
        self,
        compiled_rules: List[Dict[str, Any]],
        project_context: Dict[str, Any],
        output_dir: Path,
    ) -> FormatterResult:
        """Format compiled rules into .cursor/rules/*.mdc files."""
        files_created = []
        files_updated = []
        errors = []

        output_path = self.get_output_path(output_dir)
        cursor_rules_dir = output_path / ".cursor" / "rules"
        self.prepare_output_dir(cursor_rules_dir)

        for i, rule in enumerate(compiled_rules):
            try:
                filename = self._generate_filename(rule, i)
                file_path = cursor_rules_dir / filename

                content = self._format_single_rule(rule, project_context)

                if file_path.exists():
                    files_updated.append(file_path)
                else:
                    files_created.append(file_path)

                file_path.write_text(content, encoding="utf-8")

            except Exception as e:
                errors.append(f"Failed to format rule {i}: {str(e)}")

        success = len(errors) == 0
        return FormatterResult(
            success=success,
            files_created=files_created,
            files_updated=files_updated,
            errors=errors,
        )

    def _generate_filename(self, rule: Dict[str, Any], index: int) -> str:
        """Generate filename with priority-based prefix."""
        priority = rule.get("priority", "medium").lower()
        name = rule.get("name", f"rule_{index}").lower().replace(" ", "-")

        prefix_map = {
            "core": "00-core-",
            "high": "10-high-",
            "medium": "20-medium-",
            "low": "30-low-",
        }

        prefix = prefix_map.get(priority, "20-medium-")
        return f"{prefix}{name}{self.file_extension}"

    def _format_single_rule(self, rule: Dict[str, Any], project_context: Dict[str, Any]) -> str:
        """Format a single rule with YAML frontmatter and Markdown body."""
        frontmatter = {
            "name": rule.get("name", "Unnamed Rule"),
            "description": rule.get("description", ""),
            "priority": rule.get("priority", "medium"),
            "version": rule.get("version", "1.0.0"),
            "category": rule.get("category", "general"),
        }

        if "tags" in rule:
            frontmatter["tags"] = rule["tags"]

        if "patterns" in rule:
            frontmatter["patterns"] = rule["patterns"]

        if "globs" in rule:
            frontmatter["globs"] = rule["globs"]

        yaml_content = yaml.dump(
            frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

        body = rule.get("content", rule.get("body", ""))
        if not body:
            body = rule.get("rule_text", "")

        return f"---\n{yaml_content}---\n\n{body}\n"

    def validate_output(self, output_path: Path) -> bool:
        """Validate that generated .mdc files have required frontmatter fields."""
        if not output_path.exists():
            return False

        required_fields = {"name", "description", "priority"}

        try:
            content = output_path.read_text(encoding="utf-8")

            if not content.startswith("---"):
                return False

            parts = content.split("---", 2)
            if len(parts) < 3:
                return False

            frontmatter_text = parts[1].strip()
            if not frontmatter_text:
                return False

            try:
                frontmatter = yaml.safe_load(frontmatter_text)
            except yaml.YAMLError:
                return False

            if not isinstance(frontmatter, dict):
                return False

            return required_fields.issubset(set(frontmatter.keys()))

        except Exception:
            return False
