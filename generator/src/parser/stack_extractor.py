"""Stack extractor for identifying technology from PRD content."""

from typing import List, Dict, Set
from .prd_parser import ParsedPRD


class StackExtractor:
    """Extracts and validates technology stack from parsed PRD."""

    def __init__(self):
        self.known_stacks = {
            "nextjs-fullstack": {
                "languages": ["typescript", "javascript"],
                "frameworks": ["nextjs", "react"],
                "databases": ["postgresql", "mysql", "mongodb"],
                "tags": ["fullstack", "web", "react"],
            },
            "react-spa": {
                "languages": ["typescript", "javascript"],
                "frameworks": ["react"],
                "databases": [],
                "tags": ["frontend", "spa", "web"],
            },
            "vue-spa": {
                "languages": ["typescript", "javascript"],
                "frameworks": ["vue"],
                "databases": [],
                "tags": ["frontend", "spa", "web"],
            },
            "django-react": {
                "languages": ["python", "typescript"],
                "frameworks": ["django", "react"],
                "databases": ["postgresql", "mysql"],
                "tags": ["fullstack", "web", "python"],
            },
            "fastapi-python": {
                "languages": ["python"],
                "frameworks": ["fastapi"],
                "databases": ["postgresql", "mysql", "mongodb"],
                "tags": ["backend", "api", "python"],
            },
            "flask-python": {
                "languages": ["python"],
                "frameworks": ["flask"],
                "databases": ["postgresql", "mysql", "sqlite"],
                "tags": ["backend", "web", "python"],
            },
            "ruby-on-rails": {
                "languages": ["ruby"],
                "frameworks": ["rails"],
                "databases": ["postgresql", "mysql"],
                "tags": ["fullstack", "web", "ruby"],
            },
            "laravel": {
                "languages": ["php"],
                "frameworks": ["laravel"],
                "databases": ["mysql", "postgresql"],
                "tags": ["fullstack", "web", "php"],
            },
            "go-backend": {
                "languages": ["go"],
                "frameworks": ["gin", "echo", "fiber"],
                "databases": ["postgresql", "mysql"],
                "tags": ["backend", "api", "go"],
            },
            "rust-backend": {
                "languages": ["rust"],
                "frameworks": ["actix", "rocket", "axum"],
                "databases": ["postgresql", "mysql"],
                "tags": ["backend", "api", "rust"],
            },
            "flutter-firebase": {
                "languages": ["dart"],
                "frameworks": ["flutter"],
                "databases": ["firebase", "firestore"],
                "tags": ["mobile", "cross-platform", "flutter"],
            },
            "python-api": {
                "languages": ["python"],
                "frameworks": ["fastapi", "flask", "django"],
                "databases": ["postgresql", "mysql", "mongodb"],
                "tags": ["backend", "api", "python"],
            },
        }

    def extract_from_prd(self, parsed_prd: ParsedPRD) -> Dict[str, any]:
        """Extract stack information from parsed PRD."""
        stack_id = parsed_prd.suggested_stack

        # Get stack details
        stack_info = self.known_stacks.get(stack_id, {})

        return {
            "id": stack_id,
            "languages": stack_info.get("languages", []),
            "frameworks": stack_info.get("frameworks", []),
            "database": parsed_prd.database_type,
            "architecture": parsed_prd.architecture_type,
            "api_style": parsed_prd.api_style,
            "tags": stack_info.get("tags", []),
            "frontend_framework": parsed_prd.frontend_framework,
            "scalability": parsed_prd.scalability_needs,
            "performance_needs": parsed_prd.performance_requirements,
            "compliance": parsed_prd.security_compliance,
        }

    def suggest_rules(self, parsed_prd: ParsedPRD) -> List[str]:
        """Suggest rule categories based on parsed PRD."""
        suggested = set()

        # Always include core rules
        suggested.add("core")

        # Stack-based rules
        if parsed_prd.suggested_stack:
            suggested.add("stacks")

        # Domain rules
        if parsed_prd.frontend_framework:
            suggested.add("domains/web-frontend")
        if parsed_prd.suggested_stack not in ["react-spa", "vue-spa"]:
            suggested.add("domains/web-backend")

        # Requirement-based rules
        if parsed_prd.performance_requirements:
            suggested.add("performance")

        if parsed_prd.security_compliance:
            suggested.add("security")

        if parsed_prd.scalability_needs in ["large", "massive"]:
            suggested.add("performance")
            suggested.add("testing")

        return list(suggested)

    def validate_stack(self, stack_id: str) -> bool:
        """Check if a stack is known/supported."""
        return stack_id in self.known_stacks

    def get_related_stacks(self, stack_id: str) -> List[str]:
        """Get related stacks for alternatives."""
        if stack_id not in self.known_stacks:
            return []

        stack = self.known_stacks[stack_id]
        related = []

        for other_id, other_stack in self.known_stacks.items():
            if other_id == stack_id:
                continue

            # Check for common tags
            common_tags = set(stack.get("tags", [])) & set(other_stack.get("tags", []))
            if len(common_tags) >= 2:
                related.append(other_id)

        return related
