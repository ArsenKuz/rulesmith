"""Continue.dev formatter - generates .continuerules file."""

from pathlib import Path
from typing import Any, Dict, List

# Handle both relative and absolute imports
try:
    from ..base import BaseFormatter, FormatterConfig, FormatterResult
except ImportError:
    from base import BaseFormatter, FormatterConfig, FormatterResult


class ContinueDevFormatter(BaseFormatter):
    """Formatter for Continue.dev (.continuerules file)."""

    name = "Continue.dev"
    tool_id = "continue"
    description = "Generates .continuerules file"
    file_extension = ".continuerules"
    supports_multiple_files = False

    def format_rules(
        self,
        compiled_rules: List[Dict[str, Any]],
        project_context: Dict[str, Any],
        output_dir: Path,
    ) -> FormatterResult:
        """Generate .continuerules file."""
        output_path = self.get_output_path(output_dir / ".continuerules")

        files_created: List[Path] = []
        files_updated: List[Path] = []
        errors: List[str] = []

        try:
            content = self._generate_content(compiled_rules, project_context)

            if output_path.exists():
                files_updated.append(output_path)
            else:
                files_created.append(output_path)

            output_path.write_text(content)

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

    def _generate_content(
        self,
        rules: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> str:
        """Generate .continuerules content."""

        # Sort rules by weight
        sorted_rules = sorted(
            rules,
            key=lambda x: x.get("weight", 50),
            reverse=True,
        )

        content = f"""# Continue.dev Rules

## Project Context

- **Project:** {context.get("project_name", "Unnamed Project")}
- **Stack:** {context.get("selected_stack", "Unknown")}
- **Generated:** {context.get("timestamp", "Unknown")}

## Rules

"""

        for rule in sorted_rules:
            content += f"""
### {rule.get("id", "Rule")}

**Applies to:** {rule.get("globs", "*")}
**Weight:** {rule.get("weight", 50)}
**Always Apply:** {rule.get("alwaysApply", False)}

{rule.get("description", "No description")}

{rule.get("content", "")}

---

"""

        content += """
## Instructions

When generating code:
1. Follow the rules above based on file patterns
2. Respect rule weights for prioritization
3. Always apply core rules (marked with alwaysApply: true)
4. Consider project context and constraints
"""

        return content

    def validate_output(self, output_path: Path) -> bool:
        """Validate .continuerules file exists."""
        return output_path.exists()
