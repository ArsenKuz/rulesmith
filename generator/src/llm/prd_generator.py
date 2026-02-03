"""PRD generator using LLM."""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from .client import create_llm_client, LLMResponse


class PRDGenerator:
    """Generates PRDs via LLM API."""

    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.client = create_llm_client(provider, api_key, model)
        self.provider = provider

    def generate(
        self,
        initial_prompt: str,
        interview_answers: Dict[str, Any],
        max_tokens: int = 4000,
        temperature: float = 0.7,
    ) -> str:
        """Generate PRD from user prompt and interview answers."""
        system_prompt = self._get_system_prompt()
        user_prompt = self._construct_user_prompt(initial_prompt, interview_answers)

        response = self.client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response.content

    def _get_system_prompt(self) -> str:
        """Get system prompt for PRD generation."""
        return """You are a technical product manager specializing in creating comprehensive Product Requirements Documents (PRDs). 

Your task is to generate detailed, well-structured PRDs that serve as the foundation for software development projects.

Guidelines:
1. Be specific and actionable - avoid vague statements
2. Include technical details where relevant
3. Structure the PRD with clear sections
4. Write from the perspective of the development team
5. Include acceptance criteria for features
6. Consider scalability, security, and performance
7. Be realistic about timelines and constraints

Generate the PRD in Markdown format with proper headings and formatting."""

    def _construct_user_prompt(
        self, initial_prompt: str, interview_answers: Dict[str, Any]
    ) -> str:
        """Construct user prompt from inputs."""
        sections = []

        sections.append("# PRD Generation Request")
        sections.append(f"\n## Project Idea\n{initial_prompt}")

        sections.append("\n## Project Details from Interview")
        for key, value in interview_answers.items():
            # Format key for readability
            readable_key = key.replace("_", " ").title()
            sections.append(f"\n**{readable_key}:** {value}")

        sections.append(
            """
## Required PRD Structure

Please generate a comprehensive PRD with the following sections:

1. **Executive Summary** - Project name, one-liner, problem statement, solution overview, success metrics
2. **Context & Background** - Current state, target users, user pain points
3. **Goals & Objectives** - Primary goals (must-have), secondary goals (nice-to-have), non-goals (out of scope)
4. **Technical Architecture** - Suggested technology stack, architecture pattern, data model overview, API design approach
5. **Key Features** - Detailed description of 2-4 main features with user flows and acceptance criteria
6. **Implementation Plan** - Timeline estimates, MVP definition, phased approach
7. **Risks & Mitigation** - Key risks and how to address them
8. **Definition of Done** - Clear criteria for completion
9. **Open Questions** - Questions that need answers before proceeding

Make the PRD specific, actionable, and comprehensive. Use the project details provided above to inform all sections."""
        )

        return "\n".join(sections)

    def save_prd(
        self, content: str, output_path: Path, project_name: str = "Untitled"
    ) -> Path:
        """Save PRD to file."""
        # Ensure directory exists
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        current_date = datetime.now().strftime("%Y-%m-%d")
        project_slug = project_name.lower().replace(" ", "-")
        filename = f"prd-{project_slug}-{current_date}.md"

        file_path = output_path / filename

        # Add frontmatter to content
        full_content = f"""---
version: 1.0.0
created: {current_date}
project: {project_name}
generated_by: Rulesmith (LLM: {self.provider})
---

{content}
"""

        file_path.write_text(full_content)
        return file_path
