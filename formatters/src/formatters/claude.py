"""Claude formatter for CLAUDE.md single file output."""

from pathlib import Path
from typing import Any, Dict, List

from formatters.src.base import BaseFormatter, FormatterConfig, FormatterResult


class ClaudeFormatter(BaseFormatter):
    """Formatter for Claude AI CLAUDE.md single file."""

    name = "Claude"
    tool_id = "claude"
    description = "Formats rules for Claude AI CLAUDE.md file"
    file_extension = ".md"
    supports_multiple_files = False

    def __init__(self, config: FormatterConfig):
        super().__init__(config)

    def format_rules(
        self,
        compiled_rules: List[Dict[str, Any]],
        project_context: Dict[str, Any],
        output_dir: Path,
    ) -> FormatterResult:
        """Format compiled rules into a single CLAUDE.md file."""
        files_created = []
        files_updated = []
        errors = []

        try:
            output_path = self.get_output_path(output_dir)
            self.prepare_output_dir(output_path.parent)

            content = self._generate_content(compiled_rules, project_context)

            claude_file = output_path / "CLAUDE.md"

            if claude_file.exists():
                files_updated.append(claude_file)
            else:
                files_created.append(claude_file)

            claude_file.write_text(content, encoding="utf-8")

        except Exception as e:
            errors.append(f"Failed to generate CLAUDE.md: {str(e)}")

        success = len(errors) == 0
        return FormatterResult(
            success=success,
            files_created=files_created,
            files_updated=files_updated,
            errors=errors,
        )

    def _generate_content(
        self, compiled_rules: List[Dict[str, Any]], project_context: Dict[str, Any]
    ) -> str:
        """Generate CLAUDE.md content with required sections."""
        sections = []

        project_name = project_context.get("name", "Project")
        sections.append(f"# {project_name}\n")

        sections.append("## Project Overview\n")
        overview = project_context.get("description", "AI coding assistant rules and guidelines.")
        sections.append(f"{overview}\n")

        tech_stack = project_context.get("tech_stack", {})
        if tech_stack:
            sections.append("**Technology Stack:**")
            for category, tools in tech_stack.items():
                if isinstance(tools, list):
                    sections.append(f"- {category}: {', '.join(tools)}")
                else:
                    sections.append(f"- {category}: {tools}")
            sections.append("")

        sections.append("## Core Principles\n")

        core_rules = [r for r in compiled_rules if r.get("priority") == "core"]
        high_rules = [r for r in compiled_rules if r.get("priority") == "high"]
        medium_rules = [r for r in compiled_rules if r.get("priority") == "medium"]
        low_rules = [r for r in compiled_rules if r.get("priority") == "low"]

        priority_order = core_rules + high_rules + medium_rules + low_rules

        if priority_order:
            for rule in priority_order:
                name = rule.get("name", "Unnamed Rule")
                description = rule.get("description", "")
                content = rule.get("content", rule.get("body", ""))

                sections.append(f"### {name}\n")
                if description:
                    sections.append(f"{description}\n")
                if content:
                    sections.append(f"{content}\n")
        else:
            sections.append("No core principles defined.\n")

        sections.append("## Stack Guidelines\n")

        if tech_stack:
            for category, tools in tech_stack.items():
                sections.append(f"### {category.capitalize()}\n")

                related_rules = [
                    r
                    for r in compiled_rules
                    if category.lower() in r.get("category", "").lower()
                    or category.lower() in r.get("name", "").lower()
                ]

                if related_rules:
                    for rule in related_rules[:3]:
                        name = rule.get("name", "")
                        content = rule.get("content", rule.get("body", ""))
                        if name and content:
                            sections.append(f"**{name}**")
                            sections.append(f"{content}\n")
                else:
                    if isinstance(tools, list):
                        sections.append(f"Primary tools: {', '.join(tools)}\n")
                    else:
                        sections.append(f"Primary tool: {tools}\n")
        else:
            sections.append("No stack guidelines defined.\n")

        return "\n".join(sections)

    def validate_output(self, output_path: Path) -> bool:
        """Validate that CLAUDE.md has required sections."""
        if not output_path.exists():
            return False

        required_sections = {
            "project overview",
            "core principles",
            "stack guidelines",
        }

        try:
            content = output_path.read_text(encoding="utf-8").lower()

            found_sections = set()
            for section in required_sections:
                if f"## {section}" in content or f"# {section}" in content:
                    found_sections.add(section)

            return found_sections == required_sections

        except Exception:
            return False
