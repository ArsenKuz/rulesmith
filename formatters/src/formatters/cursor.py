"""Cursor IDE formatter - generates .cursor/rules/*.mdc files."""

import re
from pathlib import Path
from typing import Any, Dict, List
import yaml

# Handle both relative and absolute imports
try:
    from ..base import BaseFormatter, FormatterConfig, FormatterResult
except ImportError:
    from base import BaseFormatter, FormatterConfig, FormatterResult


class CursorFormatter(BaseFormatter):
    """Formatter for Cursor IDE (.mdc files)."""

    name = "Cursor"
    tool_id = "cursor"
    description = "Generates .cursor/rules/*.mdc files for Cursor IDE"
    file_extension = ".mdc"
    supports_multiple_files = True

    def format_rules(
        self,
        compiled_rules: List[Dict[str, Any]],
        project_context: Dict[str, Any],
        output_dir: Path,
    ) -> FormatterResult:
        """
        Format rules as .mdc files for Cursor.

        Creates:
        - .cursor/rules/00-core-*.mdc (core rules)
        - .cursor/rules/10-*.mdc (domain/stack rules)
        - .cursor/rules/99-project.mdc (project-specific)
        """
        output_path = self.get_output_path(output_dir / ".cursor" / "rules")
        self.prepare_output_dir(output_path)

        files_created: List[Path] = []
        files_updated: List[Path] = []
        errors: List[str] = []

        try:
            # Sort rules by weight (highest first)
            sorted_rules = sorted(
                compiled_rules,
                key=lambda x: x.get("weight", 50),
                reverse=True,
            )

            # Generate individual .mdc files for each rule
            for i, rule in enumerate(sorted_rules):
                filename = self._generate_filename(rule, i)
                file_path = output_path / filename

                content = self._format_single_rule(rule)

                if file_path.exists():
                    files_updated.append(file_path)
                else:
                    files_created.append(file_path)

                file_path.write_text(content)

            # Generate project summary file
            summary_path = output_path / "99-project-summary.mdc"
            summary_content = self._generate_project_summary(
                compiled_rules, project_context
            )
            summary_path.write_text(summary_content)

            if summary_path.exists():
                files_updated.append(summary_path)
            else:
                files_created.append(summary_path)

            return FormatterResult(
                success=True,
                files_created=files_created,
                files_updated=files_updated,
                errors=errors,
            )

        except Exception as e:
            return FormatterResult(
                success=False,
                files_created=files_created,
                files_updated=files_updated,
                errors=[str(e)],
            )

    def _generate_filename(self, rule: Dict[str, Any], index: int) -> str:
        """Generate .mdc filename with sorting prefix."""
        rule_id = rule.get("id", f"rule-{index}")
        weight = rule.get("weight", 50)

        # Determine prefix based on rule category/weight
        if rule.get("category") == "core" or rule.get("alwaysApply"):
            prefix = f"00-core-{index:02d}"
        elif weight >= 70:
            prefix = f"10-high-{index:02d}"
        elif weight >= 40:
            prefix = f"20-medium-{index:02d}"
        else:
            prefix = f"30-low-{index:02d}"

        return f"{prefix}-{rule_id}.mdc"

    def _format_single_rule(self, rule: Dict[str, Any]) -> str:
        """Format a single rule as .mdc content."""
        frontmatter = {
            "description": rule.get("description", ""),
            "globs": rule.get("globs", "**/*"),
            "alwaysApply": rule.get("alwaysApply", False),
        }

        # Build YAML frontmatter
        yaml_content = yaml.dump(
            frontmatter,
            default_flow_style=False,
            sort_keys=False,
        )

        # Combine frontmatter + body
        content = f"---\n{yaml_content}---\n\n"
        content += rule.get("content", "")

        return content

    def _generate_project_summary(
        self,
        rules: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> str:
        """Generate project summary .mdc file."""
        frontmatter = {
            "description": f"Project overview: {context.get('project_name', 'Unnamed')}",
            "globs": "*",
            "alwaysApply": True,
        }

        yaml_content = yaml.dump(frontmatter, default_flow_style=False)

        body = f"""# Project Context

**Project:** {context.get("project_name", "Unnamed Project")}
**Stack:** {context.get("selected_stack", "Unknown")}
**Generated:** {context.get("timestamp", "Unknown")}

## Active Rules

This project uses {len(rules)} AI assistant rules:

"""

        for rule in rules:
            body += (
                f"- **{rule.get('id')}**: {rule.get('description', 'No description')}\n"
            )

        body += """
## Quick Reference

- Always follow the patterns defined in individual rule files
- When in doubt, prefer explicit over implicit
- Security and error handling are non-negotiable
"""

        return f"---\n{yaml_content}---\n\n{body}"

    def validate_output(self, output_path: Path) -> bool:
        """Validate .mdc files are correctly formatted."""
        if not output_path.exists():
            return False

        for mdc_file in output_path.glob("*.mdc"):
            content = mdc_file.read_text()

            # Must have YAML frontmatter
            if not content.startswith("---"):
                return False

            # Must have required frontmatter fields
            try:
                match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
                if not match:
                    return False

                frontmatter = yaml.safe_load(match.group(1))
                if "description" not in frontmatter or "globs" not in frontmatter:
                    return False
            except Exception:
                return False

        return True
