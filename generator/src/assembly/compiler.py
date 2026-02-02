"""Rule assembly and compilation."""

import re
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml


class RuleCompiler:
    """Compiles selected rules into final output."""

    def __init__(self, library_path: Path):
        self.library_path = library_path
        self.resolved_rules: Set[str] = set()
        self.compiled_rules: List[Dict[str, Any]] = []

    def compile(
        self, selected_stack: str, interview_answers: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
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
        all_rule_ids = self._resolve_dependencies(core_rules + stack_rules + domain_rules, index)

        # Load and compile each rule
        compiled = []
        for rule_id in all_rule_ids:
            rule = self._load_rule(rule_id, index)
            if rule:
                # Personalize rule based on interview answers
                personalized = self._personalize_rule(rule, interview_answers)
                compiled.append(personalized)

        # Sort by weight
        compiled.sort(key=lambda x: x.get("weight", 50), reverse=True)

        return compiled

    def _load_index(self) -> Dict[str, Any]:
        """Load library index.yaml."""
        index_path = self.library_path / "index.yaml"
        with open(index_path) as f:
            return yaml.safe_load(f)

    def _get_core_rules(self, index: Dict[str, Any]) -> List[str]:
        """Get IDs of all core rules that alwaysApply."""
        rules = []
        for rule in index.get("categories", {}).get("core", {}).get("rules", []):
            if rule.get("alwaysApply"):
                rules.append(rule["id"])
        return rules

    def _get_stack_rules(self, index: Dict[str, Any], stack_id: str) -> List[str]:
        """Get rules for selected stack."""
        stacks = index.get("categories", {}).get("stacks", {}).get("rules", [])
        for stack in stacks:
            if stack["id"] == stack_id:
                # Return stack + all included rules
                return [stack_id] + stack.get("includes", [])
        return []

    def _select_domain_rules(self, index: Dict[str, Any], answers: Dict[str, Any]) -> List[str]:
        """Select domain rules based on interview answers."""
        selected = []

        # Example logic:
        if answers.get("testing_approach") == "TDD (Test-Driven Development)":
            selected.append("testing-unit")
            selected.append("testing-integration")

        if answers.get("performance_critical"):
            selected.append("performance-optimization")

        if answers.get("security_compliance") != "None":
            selected.append("security-compliance")

        # Add frontend domain if project is web-based
        purpose = answers.get("project_purpose", "").lower()
        if any(term in purpose for term in ["web", "saas", "e-commerce", "content"]):
            selected.append("web-frontend")

        return selected

    def _resolve_dependencies(self, rule_ids: List[str], index: Dict[str, Any]) -> Set[str]:
        """Resolve all includes recursively."""
        resolved: Set[str] = set()
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

    def _load_rule(self, rule_id: str, index: Dict[str, Any]) -> Dict[str, Any]:
        """Load rule file from disk."""
        # Find rule in index
        file_path: Path | None = None
        category_name = ""

        for cat_name, category in index.get("categories", {}).items():
            for rule in category.get("rules", []):
                if rule["id"] == rule_id:
                    file_path = self.library_path / rule["file"]
                    category_name = cat_name
                    break
            if file_path:
                break

        if not file_path or not file_path.exists():
            return {}

        # Parse YAML frontmatter + Markdown
        content = file_path.read_text()
        return self._parse_rule_file(content, rule_id, category_name)

    def _parse_rule_file(self, content: str, rule_id: str, category: str) -> Dict[str, Any]:
        """Parse rule file into structured format."""
        # Extract frontmatter
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            return {}

        frontmatter = yaml.safe_load(match.group(1))
        body = content[match.end() :]

        return {
            "id": rule_id,
            "description": frontmatter.get("description", ""),
            "globs": frontmatter.get("globs", "*"),
            "alwaysApply": frontmatter.get("alwaysApply", False),
            "weight": frontmatter.get("weight", 50),
            "content": body,
            "frontmatter": frontmatter,
            "category": category,
        }

    def _personalize_rule(self, rule: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
        """Personalize rule content based on interview answers."""
        personalized = rule.copy()
        content = rule["content"]

        # Simple template substitution
        for key, value in answers.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in content:
                content = content.replace(placeholder, str(value))

        personalized["content"] = content
        return personalized
