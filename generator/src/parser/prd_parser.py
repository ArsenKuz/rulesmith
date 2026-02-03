"""PRD parser for extracting structured data from PRD documents."""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ParsedPRD:
    """Structured data extracted from a PRD."""

    # Project info
    project_name: str = ""
    one_liner: str = ""
    problem_statement: str = ""
    solution_overview: str = ""

    # Tech stack
    suggested_stack: str = ""
    architecture_type: str = ""  # monolith, microservices, serverless
    database_type: str = ""  # sql, nosql, both
    api_style: str = ""  # rest, graphql, grpc
    frontend_framework: str = ""  # react, vue, etc

    # Requirements
    performance_requirements: List[str] = field(default_factory=list)
    security_compliance: List[str] = field(default_factory=list)
    scalability_needs: str = ""  # small, medium, large, massive

    # Features
    key_features: List[str] = field(default_factory=list)
    mvp_scope: str = ""

    # Timeline
    timeline: str = ""
    target_users: str = ""

    # Raw content
    raw_content: str = ""


class PRDParser:
    """Extracts structured data from LLM-generated PRD."""

    def __init__(self):
        self.tech_patterns = {
            "nextjs": ["next.js", "nextjs", "next"],
            "react": ["react", "react.js"],
            "vue": ["vue", "vue.js"],
            "angular": ["angular"],
            "django": ["django"],
            "fastapi": ["fastapi", "fast api"],
            "flask": ["flask"],
            "express": ["express", "express.js"],
            "rails": ["ruby on rails", "rails"],
            "laravel": ["laravel"],
            "spring": ["spring boot", "springboot"],
            "go": ["go", "golang", "gin", "echo", "fiber"],
            "rust": ["rust", "actix", "rocket", "axum"],
            "flutter": ["flutter"],
            "python": ["python"],
            "typescript": ["typescript", "ts"],
            "javascript": ["javascript", "js"],
        }

        self.architecture_patterns = {
            "monolith": ["monolith", "monolithic"],
            "microservices": ["microservices", "micro-service"],
            "serverless": ["serverless", "lambda", "functions"],
            "modular": ["modular monolith", "modular"],
        }

        self.database_patterns = {
            "sql": ["postgresql", "postgres", "mysql", "sqlite", "sql"],
            "nosql": ["mongodb", "mongo", "dynamodb", "cassandra", "nosql"],
            "both": ["both", "sql and nosql", "hybrid"],
        }

        self.api_patterns = {
            "rest": ["rest", "restful"],
            "graphql": ["graphql", "graph ql"],
            "grpc": ["grpc"],
            "trpc": ["trpc", "t-rpc"],
        }

    def parse(self, prd_content: str) -> ParsedPRD:
        """Parse PRD content and extract structured data."""
        parsed = ParsedPRD(raw_content=prd_content)

        # Extract project info
        parsed.project_name = self._extract_project_name(prd_content)
        parsed.one_liner = self._extract_one_liner(prd_content)
        parsed.problem_statement = self._extract_section(
            prd_content, "Problem Statement"
        )
        parsed.solution_overview = self._extract_section(
            prd_content, "Solution Overview"
        )

        # Extract tech stack
        parsed.suggested_stack = self._detect_stack(prd_content)
        parsed.architecture_type = self._detect_architecture(prd_content)
        parsed.database_type = self._detect_database(prd_content)
        parsed.api_style = self._detect_api_style(prd_content)
        parsed.frontend_framework = self._detect_frontend(prd_content)

        # Extract requirements
        parsed.performance_requirements = self._detect_performance_needs(prd_content)
        parsed.security_compliance = self._detect_security_compliance(prd_content)
        parsed.scalability_needs = self._detect_scalability(prd_content)

        # Extract features and timeline
        parsed.key_features = self._extract_features(prd_content)
        parsed.mvp_scope = self._extract_mvp_scope(prd_content)
        parsed.timeline = self._extract_timeline(prd_content)
        parsed.target_users = self._extract_target_users(prd_content)

        return parsed

    def parse_file(self, file_path: Path) -> ParsedPRD:
        """Parse PRD from file."""
        content = file_path.read_text()
        return self.parse(content)

    def _extract_project_name(self, content: str) -> str:
        """Extract project name from PRD."""
        patterns = [
            r"#\s*PRD[-:]?\s*([^\n]+)",
            r"Project Name[:\*]?\s*([^\n]+)",
            r"#\s*([^\n]+)\s*Product Requirements",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""

    def _extract_one_liner(self, content: str) -> str:
        """Extract one-liner/elevator pitch."""
        patterns = [
            r"One[- ]?Liner[:\*]?\s*([^\n]+)",
            r"Elevator Pitch[:\*]?\s*([^\n]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract content from a specific section."""
        pattern = rf"{section_name}[:\*]?\s*\n+([^#]+?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def _detect_stack(self, content: str) -> str:
        """Detect primary technology stack from PRD."""
        content_lower = content.lower()
        scores = {}

        for stack, patterns in self.tech_patterns.items():
            score = 0
            for pattern in patterns:
                count = len(re.findall(rf"\b{re.escape(pattern)}\b", content_lower))
                score += count
            if score > 0:
                scores[stack] = score

        if scores:
            return max(scores, key=scores.get)
        return ""

    def _detect_architecture(self, content: str) -> str:
        """Detect architecture type from PRD."""
        content_lower = content.lower()

        for arch, patterns in self.architecture_patterns.items():
            for pattern in patterns:
                if pattern in content_lower:
                    return arch
        return "monolith"  # Default

    def _detect_database(self, content: str) -> str:
        """Detect database type from PRD."""
        content_lower = content.lower()

        for db_type, patterns in self.database_patterns.items():
            for pattern in patterns:
                if pattern in content_lower:
                    return db_type
        return ""

    def _detect_api_style(self, content: str) -> str:
        """Detect API style from PRD."""
        content_lower = content.lower()

        for api, patterns in self.api_patterns.items():
            for pattern in patterns:
                if pattern in content_lower:
                    return api
        return "rest"  # Default

    def _detect_frontend(self, content: str) -> str:
        """Detect frontend framework from PRD."""
        content_lower = content.lower()
        frontend_keywords = ["react", "vue", "angular", "svelte", "nextjs", "flutter"]

        for keyword in frontend_keywords:
            if keyword in content_lower:
                return keyword
        return ""

    def _detect_performance_needs(self, content: str) -> List[str]:
        """Detect performance requirements."""
        needs = []
        content_lower = content.lower()

        keywords = {
            "low_latency": ["low latency", "real-time", "realtime", "fast response"],
            "high_throughput": [
                "high throughput",
                "high traffic",
                "scalable",
                "performance",
            ],
            "caching": ["cache", "caching", "redis"],
            "cdn": ["cdn", "content delivery"],
        }

        for need, patterns in keywords.items():
            for pattern in patterns:
                if pattern in content_lower:
                    needs.append(need)
                    break

        return needs

    def _detect_security_compliance(self, content: str) -> List[str]:
        """Detect security and compliance requirements."""
        compliance = []
        content_lower = content.lower()

        keywords = {
            "gdpr": ["gdpr", "data privacy", "eu"],
            "hipaa": ["hipaa", "healthcare", "medical"],
            "soc2": ["soc 2", "soc2", "compliance"],
            "pci": ["pci", "payment", "credit card"],
        }

        for comp, patterns in keywords.items():
            for pattern in patterns:
                if pattern in content_lower:
                    compliance.append(comp)
                    break

        return compliance

    def _detect_scalability(self, content: str) -> str:
        """Detect scalability requirements."""
        content_lower = content.lower()

        if re.search(r"millions?\s+of\s+users", content_lower):
            return "massive"
        elif re.search(r"100k|100,000|hundred\s+thousand", content_lower):
            return "large"
        elif re.search(r"10k|10,000|thousand", content_lower):
            return "medium"
        elif re.search(r"small\s+scale|startup|mvp", content_lower):
            return "small"
        return "medium"  # Default

    def _extract_features(self, content: str) -> List[str]:
        """Extract key features from PRD."""
        features = []

        # Match Feature sections
        pattern = r"###?\s*Feature\s*\d*:?\s*([^\n]+)"
        matches = re.findall(pattern, content, re.IGNORECASE)

        for match in matches:
            features.append(match.strip())

        return features

    def _extract_mvp_scope(self, content: str) -> str:
        """Extract MVP scope from PRD."""
        return self._extract_section(content, "MVP Definition")

    def _extract_timeline(self, content: str) -> str:
        """Extract timeline from PRD."""
        timeline_section = self._extract_section(content, "Timeline")
        if timeline_section:
            return timeline_section

        # Try to find timeline patterns
        patterns = [
            r"(\d+\s+(week|month|day)s?)",
            r"(Q[1-4]\s+\d{4})",
            r"(\w+\s+\d{4})",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""

    def _extract_target_users(self, content: str) -> str:
        """Extract target users from PRD."""
        return self._extract_section(content, "Target Users")

    def to_stack_mapping(self, parsed_prd: ParsedPRD) -> str:
        """Map parsed PRD to internal stack ID."""
        stack = parsed_prd.suggested_stack.lower()

        # Map to internal stack IDs
        mappings = {
            "nextjs": "nextjs-fullstack",
            "react": "react-spa",
            "vue": "vue-spa",
            "django": "django-react",
            "fastapi": "fastapi-python",
            "flask": "flask-python",
            "rails": "ruby-on-rails",
            "laravel": "laravel",
            "go": "go-backend",
            "rust": "rust-backend",
            "flutter": "flutter-firebase",
            "python": "python-api",
        }

        if stack in mappings:
            return mappings[stack]

        # If frontend + backend detected, it's full-stack
        if parsed_prd.frontend_framework and stack not in ["react", "vue", "angular"]:
            return f"{parsed_prd.frontend_framework}-{stack}"

        return stack or "generic"
