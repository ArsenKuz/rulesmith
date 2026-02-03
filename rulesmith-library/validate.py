#!/usr/bin/env python3
"""Validate all rule files follow correct format."""

import yaml
import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class RuleValidationError:
    file: Path
    error: str


class RuleValidator:
    REQUIRED_FIELDS = {"description", "globs"}
    VALID_FIELDS = {
        "description",
        "globs",
        "alwaysApply",
        "weight",
        "tags",
        "related",
        "includes",
        "signals",
    }

    def validate_file(self, filepath: Path) -> list:
        errors = []
        content = filepath.read_text()

        # Check for YAML frontmatter
        if not content.startswith("---"):
            errors.append(RuleValidationError(filepath, "Missing YAML frontmatter"))
            return errors

        # Extract frontmatter
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            errors.append(RuleValidationError(filepath, "Invalid frontmatter format"))
            return errors

        # Parse YAML
        try:
            frontmatter = yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            errors.append(RuleValidationError(filepath, f"YAML parse error: {e}"))
            return errors

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in frontmatter:
                errors.append(
                    RuleValidationError(filepath, f"Missing required field: {field}")
                )

        # Check for invalid fields
        for field in frontmatter:
            if field not in self.VALID_FIELDS:
                errors.append(RuleValidationError(filepath, f"Invalid field: {field}"))

        # Validate globs format
        if "globs" in frontmatter and not isinstance(frontmatter["globs"], str):
            errors.append(RuleValidationError(filepath, "globs must be a string"))

        # Validate weight range
        if "weight" in frontmatter:
            weight = frontmatter["weight"]
            if not isinstance(weight, int) or weight < 0 or weight > 100:
                errors.append(
                    RuleValidationError(filepath, "weight must be integer 0-100")
                )

        return errors


def main():
    library_path = Path(__file__).parent
    validator = RuleValidator()
    all_errors = []

    # Find all .md files
    for md_file in library_path.rglob("*.md"):
        if md_file.name in ["README.md", "CHANGELOG.md"]:
            continue
        errors = validator.validate_file(md_file)
        all_errors.extend(errors)

    if all_errors:
        print(f"Found {len(all_errors)} validation error(s):")
        for error in all_errors:
            print(f"  {error.file}: {error.error}")
        return 1
    else:
        print("All rule files are valid!")
        return 0


if __name__ == "__main__":
    exit(main())
