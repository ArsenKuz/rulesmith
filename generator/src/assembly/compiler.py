"""Rule compiler for assembling rules from library."""

import re
from typing import Dict, List, Set
from pathlib import Path
import yaml
from ..models.assembly import CompiledRule


class RuleCompiler:
    """Compiles selected rules into final output."""

    def __init__(self, library_path: Path):
        self.library_path = library_path
        self.resolved_rules: Set[str] = set()

    def compile(
        self, selected_stack: str, interview_answers: Dict
    ) -> List[CompiledRule]:
        """
        Compile rules based on stack selection and interview answers.

        Args:
            selected_stack: The chosen technology stack ID
            interview_answers: User responses from interview

        Returns:
            List of compiled rules with metadata
        """
        # Load library index
        index = self._load_index()

        # Get core rules (always included)
        core_rules = self._get_core_rules(index)

        # Get stack-specific rules
        stack_rules = self._get_stack_rules(index, selected_stack)

        # Get domain rules based on answers
        domain_rules = self._select_domain_rules(index, interview_answers)

        # Resolve all includes and dependencies
        all_rule_ids = self._resolve_dependencies(
            core_rules + stack_rules + domain_rules, index
        )

        # Load and compile each rule
        compiled = []
        for rule_id in all_rule_ids:
            rule = self._load_rule(rule_id, index)
            if rule:
                # Personalize rule based on interview answers
                personalized = self._personalize_rule(rule, interview_answers)
                compiled.append(personalized)

        # Sort by weight
        compiled.sort(key=lambda x: x.weight, reverse=True)

        return compiled

    def _load_index(self) -> Dict:
        """Load library index.yaml."""
        index_path = self.library_path / "index.yaml"
        if not index_path.exists():
            return {"categories": {}}

        with open(index_path) as f:
            return yaml.safe_load(f)

    def _get_core_rules(self, index: Dict) -> List[str]:
        """Get IDs of all core rules that alwaysApply."""
        rules = []
        for rule in index.get("categories", {}).get("core", {}).get("rules", []):
            if rule.get("alwaysApply"):
                rules.append(rule["id"])
        return rules

    def _get_stack_rules(self, index: Dict, stack_id: str) -> List[str]:
        """Get rules for selected stack."""
        stacks = index.get("categories", {}).get("stacks", {}).get("rules", [])
        for stack in stacks:
            if stack["id"] == stack_id:
                # Return stack + all included rules
                return [stack_id] + stack.get("includes", [])
        return []

    def _select_domain_rules(self, index: Dict, answers: Dict) -> List[str]:
        """Select domain rules based on interview answers."""
        selected = []

        # Testing approach
        if answers.get("testing_approach") == "TDD (Test-Driven Development)":
            selected.append("testing-unit")
            selected.append("testing-integration")

        # Performance
        if answers.get("performance_critical"):
            selected.append("performance-optimization")

        # Security
        if (
            answers.get("security_compliance")
            and answers.get("security_compliance") != "None"
        ):
            selected.append("security-compliance")

        # Documentation level
        if (
            answers.get("documentation_level")
            == "Comprehensive (API docs, ADRs, runbooks)"
        ):
            selected.append("documentation-adr")

        # Code style
        if answers.get("code_style") == "Very strict (enforced by CI)":
            selected.append("linting-strict")

        # Team size - collaboration rules
        team_size = answers.get("team_size", "")
        if "Medium" in team_size or "Large" in team_size:
            selected.append("collaboration-practices")

        return selected

    def _resolve_dependencies(self, rule_ids: List[str], index: Dict) -> Set[str]:
        """Resolve all includes recursively."""
        resolved = set()
        to_process = list(rule_ids)

        while to_process:
            rule_id = to_process.pop(0)
            if rule_id in resolved:
                continue

            resolved.add(rule_id)

            # Find rule in index and add its includes
            for category in index.get("categories", {}).values():
                for rule in category.get("rules", []):
                    if rule["id"] == rule_id:
                        includes = rule.get("includes", [])
                        to_process.extend(includes)

        return resolved

    def _load_rule(self, rule_id: str, index: Dict) -> CompiledRule:
        """Load rule file from disk."""
        # Find rule in index
        file_path = None
        category_name = None

        for cat_name, category in index.get("categories", {}).items():
            for rule in category.get("rules", []):
                if rule["id"] == rule_id:
                    file_path = self.library_path / rule["file"]
                    category_name = cat_name
                    break
            if file_path:
                break

        if not file_path or not file_path.exists():
            return None

        # Parse YAML frontmatter + Markdown
        content = file_path.read_text()
        return self._parse_rule_file(content, rule_id, category_name)

    def _parse_rule_file(
        self, content: str, rule_id: str, category: str
    ) -> CompiledRule:
        """Parse rule file into structured format."""
        # Extract frontmatter
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            return None

        frontmatter = yaml.safe_load(match.group(1))
        body = content[match.end() :]

        return CompiledRule(
            id=rule_id,
            description=frontmatter.get("description", ""),
            globs=frontmatter.get("globs", "*"),
            alwaysApply=frontmatter.get("alwaysApply", False),
            weight=frontmatter.get("weight", 50),
            content=body,
            frontmatter=frontmatter,
            category=category,
        )

    def _personalize_rule(self, rule: CompiledRule, answers: Dict) -> CompiledRule:
        """Personalize rule content based on interview answers."""
        # Simple template substitution
        content = rule.content

        for key, value in answers.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in content:
                content = content.replace(placeholder, str(value))

        return CompiledRule(
            id=rule.id,
            description=rule.description,
            globs=rule.globs,
            alwaysApply=rule.alwaysApply,
            weight=rule.weight,
            content=content,
            frontmatter=rule.frontmatter,
            category=rule.category,
        )
