"""PRD generation command - Create Product Requirements Document through interactive prompts."""

import typer
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.text import Text

app = typer.Typer()
console = Console()


class PRDQuestion:
    """A single question in the PRD interview."""

    def __init__(
        self,
        id: str,
        text: str,
        section: str,
        question_type: str = "text",
        description: Optional[str] = None,
        options: Optional[List[str]] = None,
        default: Optional[str] = None,
        required: bool = True,
        multiline: bool = False,
    ):
        self.id = id
        self.text = text
        self.section = section
        self.question_type = question_type
        self.description = description
        self.options = options
        self.default = default
        self.required = required
        self.multiline = multiline


# PRD interview questions organized by section
PRD_QUESTIONS = [
    # Section 1: Executive Summary
    PRDQuestion(
        id="project_name",
        text="What is the project name?",
        section="Executive Summary",
        required=True,
    ),
    PRDQuestion(
        id="one_liner",
        text="Describe the project in one sentence (elevator pitch)",
        section="Executive Summary",
        description="Example: 'A tool that automatically generates AI assistant rules for coding projects'",
        required=True,
    ),
    PRDQuestion(
        id="problem_statement",
        text="What problem does this project solve?",
        section="Executive Summary",
        description="Describe the pain point or gap this addresses",
        multiline=True,
        required=True,
    ),
    PRDQuestion(
        id="solution_overview",
        text="How does this project solve the problem?",
        section="Executive Summary",
        description="High-level approach to the solution",
        multiline=True,
        required=True,
    ),
    PRDQuestion(
        id="success_metrics",
        text="How will you measure success?",
        section="Executive Summary",
        description="List 2-3 specific, measurable outcomes",
        multiline=True,
        required=True,
    ),
    # Section 2: Context & Background
    PRDQuestion(
        id="current_state",
        text="What is the current state? What exists today?",
        section="Context",
        description="Describe existing solutions, workarounds, or lack thereof",
        multiline=True,
        required=True,
    ),
    PRDQuestion(
        id="target_users",
        text="Who are the primary users?",
        section="Context",
        description="Describe your target audience (role, skill level, needs)",
        multiline=True,
        required=True,
    ),
    PRDQuestion(
        id="user_pain_points",
        text="What are the top 3 pain points for users?",
        section="Context",
        description="List specific frustrations with current solutions",
        multiline=True,
        required=True,
    ),
    # Section 3: Goals
    PRDQuestion(
        id="primary_goal_1",
        text="What is the primary goal (must-have)?",
        section="Goals",
        description="The one thing that MUST be achieved for this to be considered a success",
        multiline=True,
        required=True,
    ),
    PRDQuestion(
        id="primary_goal_2",
        text="What is the second primary goal (must-have)?",
        section="Goals",
        required=False,
    ),
    PRDQuestion(
        id="secondary_goal_1",
        text="What is a secondary goal (nice-to-have)?",
        section="Goals",
        required=False,
    ),
    PRDQuestion(
        id="out_of_scope",
        text="What is explicitly OUT of scope?",
        section="Goals",
        description="List things you are NOT building (prevents scope creep)",
        multiline=True,
        required=False,
    ),
    # Section 4: Technical Context
    PRDQuestion(
        id="tech_stack",
        text="What is the primary technology stack?",
        section="Technical",
        question_type="choice",
        options=[
            "Next.js / React",
            "Django / Python",
            "FastAPI / Python",
            "Node.js / Express",
            "Ruby on Rails",
            "Go",
            "Rust",
            "Other",
        ],
        required=True,
    ),
    PRDQuestion(
        id="existing_components",
        text="What existing components or systems will this integrate with?",
        section="Technical",
        description="APIs, databases, services, libraries",
        multiline=True,
        required=False,
    ),
    PRDQuestion(
        id="constraints",
        text="What are the main constraints or limitations?",
        section="Technical",
        description="Time, budget, technical, legal, etc.",
        multiline=True,
        required=False,
    ),
    # Section 5: Key Features
    PRDQuestion(
        id="feature_1",
        text="Describe the main feature (Feature 1)",
        section="Features",
        description="What does it do? Who uses it?",
        multiline=True,
        required=True,
    ),
    PRDQuestion(
        id="feature_1_user_flow",
        text="What is the user flow for Feature 1?",
        section="Features",
        description="Step-by-step: 1. User does X, 2. System does Y, 3. Result is Z",
        multiline=True,
        required=True,
    ),
    PRDQuestion(
        id="feature_2",
        text="Describe a secondary feature (Feature 2)",
        section="Features",
        required=False,
        multiline=True,
    ),
    PRDQuestion(
        id="feature_3",
        text="Describe another feature (Feature 3)",
        section="Features",
        required=False,
        multiline=True,
    ),
    # Section 6: Timeline
    PRDQuestion(
        id="timeline",
        text="What is the target timeline?",
        section="Timeline",
        question_type="choice",
        options=[
            "1 week (MVP/skeleton)",
            "2-3 weeks (basic version)",
            "1 month (full feature set)",
            "2-3 months (comprehensive)",
            "3+ months (enterprise)",
        ],
        required=True,
    ),
    PRDQuestion(
        id="mvp_definition",
        text="What is the definition of 'done' for the MVP?",
        section="Timeline",
        description="Minimum features needed to launch",
        multiline=True,
        required=True,
    ),
    # Section 7: Risks
    PRDQuestion(
        id="main_risk",
        text="What is the biggest risk to this project's success?",
        section="Risks",
        description="Technical, business, team, or external risk",
        multiline=True,
        required=False,
    ),
    PRDQuestion(
        id="risk_mitigation",
        text="How can that risk be mitigated?",
        section="Risks",
        required=False,
        multiline=True,
    ),
]


def ask_question(question: PRDQuestion) -> str:
    """Ask a single question and return the answer."""
    console.print(f"\n[bold blue]{question.section}[/bold blue]")
    console.print(f"[bold]{question.text}[/bold]")

    if question.description:
        console.print(f"[dim]{question.description}[/dim]")

    if question.question_type == "choice" and question.options:
        for i, option in enumerate(question.options, 1):
            console.print(f"  [{i}] {option}")

        default_num = 1
        if question.default and question.default in question.options:
            default_num = question.options.index(question.default) + 1

        choice = IntPrompt.ask("Enter number", default=default_num)
        if 1 <= choice <= len(question.options):
            return question.options[choice - 1]
        return question.options[0] if question.options else ""

    elif question.multiline:
        console.print("[dim]Enter your answer (empty line to finish):[/dim]")
        lines = []
        while True:
            line = Prompt.ask("", default="")
            if line == "" and len(lines) > 0:
                break
            lines.append(line)
        return "\n".join(lines)

    else:
        default = question.default or ""
        return Prompt.ask("Your answer", default=default)


def generate_prd_content(answers: dict) -> str:
    """Generate PRD markdown content from answers."""

    current_date = datetime.now().strftime("%Y-%m-%d")

    content = f"""# PRD-{answers.get("project_name", "Untitled").replace(" ", "-")}

**Status**: Draft  
**Last Updated**: {current_date}  
**Author**: [Your Name]  
**Stakeholders**: [Team/Stakeholders]

---

## 1. Executive Summary

### Project Name
{answers.get("project_name", "TBD")}

### One-Liner
{answers.get("one_liner", "TBD")}

### Problem Statement
{answers.get("problem_statement", "TBD")}

### Solution Overview
{answers.get("solution_overview", "TBD")}

### Success Metrics
{answers.get("success_metrics", "TBD")}

---

## 2. Context & Background

### Current State
{answers.get("current_state", "TBD")}

### Target Users
{answers.get("target_users", "TBD")}

### User Pain Points
{answers.get("user_pain_points", "TBD")}

---

## 3. Goals & Objectives

### Primary Goals (Must-Have)
1. {answers.get("primary_goal_1", "TBD")}
"""

    if answers.get("primary_goal_2"):
        content += f"2. {answers['primary_goal_2']}\n"

    content += "\n### Secondary Goals (Nice-to-Have)\n"
    if answers.get("secondary_goal_1"):
        content += f"1. {answers['secondary_goal_1']}\n"
    else:
        content += "1. TBD\n"

    content += f"""
### Non-Goals (Out of Scope)
{answers.get("out_of_scope", "TBD")}

---

## 4. Technical Context

### Technology Stack
{answers.get("tech_stack", "TBD")}

### Existing Components
{answers.get("existing_components", "TBD")}

### Constraints
{answers.get("constraints", "TBD")}

---

## 5. Key Features

### Feature 1: {answers.get("feature_1", "Main Feature")}

**Description**: {answers.get("feature_1", "TBD")}

**User Flow**:
{answers.get("feature_1_user_flow", "TBD")}

**Acceptance Criteria**:
- [ ] Criteria 1 (given/when/then)
- [ ] Criteria 2 (given/when/then)
- [ ] Criteria 3 (given/when/then)

---
"""

    if answers.get("feature_2"):
        content += f"""
### Feature 2

**Description**: {answers["feature_2"]}

**User Flow**:
- Step 1
- Step 2
- Step 3

---
"""

    if answers.get("feature_3"):
        content += f"""
### Feature 3

**Description**: {answers["feature_3"]}

**User Flow**:
- Step 1
- Step 2
- Step 3

---
"""

    content += f"""
## 6. Implementation Plan

### Timeline
{answers.get("timeline", "TBD")}

### MVP Definition
{answers.get("mvp_definition", "TBD")}

### Phases
1. **Phase 1 - Foundation**: Basic structure and core functionality
2. **Phase 2 - Core Features**: Main feature implementation
3. **Phase 3 - Polish**: Testing, documentation, and launch

---

## 7. Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {answers.get("main_risk", "TBD")} | Medium | High | {answers.get("risk_mitigation", "TBD")} |

---

## 8. Definition of Done (DoD)

- [ ] All primary goals achieved
- [ ] Acceptance criteria met for all features
- [ ] Code reviewed and approved
- [ ] Tests passing (unit + integration)
- [ ] Documentation complete
- [ ] Deployed and tested

---

## 9. Open Questions

1. [List any questions that need answers before proceeding]
2. 
3. 

---

**End of PRD**
"""

    return content


@app.callback(invoke_without_command=True)
def prd_command(
    path: Path = typer.Option(
        Path("."), "--path", "-p", help="Path to project directory"
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output filename (default: docs/prd-<project-name>.md)",
    ),
    quick: bool = typer.Option(
        False, "--quick", "-q", help="Quick mode - skip optional questions"
    ),
):
    """Generate a Product Requirements Document through interactive prompts."""

    project_path = path.resolve()

    console.print(
        Panel.fit(
            "[bold green]📋 PRD Generator[/bold green]\n"
            "Let's create a comprehensive Product Requirements Document!",
            border_style="green",
        )
    )

    # Run interview
    answers = {}
    current_section = None

    for question in PRD_QUESTIONS:
        # Skip optional questions in quick mode
        if quick and not question.required:
            continue

        # Print section header if changed
        if question.section != current_section:
            current_section = question.section

        # Ask question
        answer = ask_question(question)

        # Store answer
        answers[question.id] = answer

    # Generate PRD content
    prd_content = generate_prd_content(answers)

    # Determine output path
    docs_dir = project_path / "docs"
    docs_dir.mkdir(exist_ok=True)

    if output:
        output_path = docs_dir / output
    else:
        project_name_slug = (
            answers.get("project_name", "untitled").replace(" ", "-").lower()
        )
        output_path = docs_dir / f"prd-{project_name_slug}.md"

    # Check if file exists
    if output_path.exists():
        overwrite = Confirm.ask(
            f"\n[yellow]File {output_path.name} already exists. Overwrite?[/yellow]",
            default=False,
        )
        if not overwrite:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_path = docs_dir / f"prd-{project_name_slug}-{timestamp}.md"
            console.print(f"[dim]Saving as: {output_path.name}[/dim]")

    # Write PRD
    output_path.write_text(prd_content)

    console.print(f"\n[bold green]✓ PRD generated:[/bold green] {output_path}")
    console.print(
        f"[dim]Total sections: ~{len(set(q.section for q in PRD_QUESTIONS if not quick or q.required))}[/dim]"
    )

    console.print("\n[yellow]Next steps:[/yellow]")
    console.print("  1. Review and edit the PRD")
    console.print("  2. Share with stakeholders for feedback")
    console.print("  3. Create GitHub issues from features")
    console.print("  4. Start with Phase 1 implementation")
