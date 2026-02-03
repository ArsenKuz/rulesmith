"""New project mode: 10-15 question interview for new projects."""

from typing import Dict, Any, List
from rich.console import Console
from generator.src.interview.engine import InterviewEngine
from generator.src.models.interview import Question, QuestionType


# New project mode questions - organized by category
NEW_PROJECT_QUESTIONS = [
    # Section 1: Basics (2-3 questions)
    Question(
        id="project_name",
        type=QuestionType.TEXT,
        text="What would you like to name this project?",
        required=True,
    ),
    Question(
        id="project_type",
        type=QuestionType.CHOICE,
        text="What type of application are you building?",
        options=[
            "SaaS (Software as a Service)",
            "Web Application",
            "Mobile App",
            "API / Backend",
            "CLI Tool",
            "Desktop Application",
            "Data/ML Pipeline",
            "Other",
        ],
        required=True,
    ),
    # Section 2: Users (2-3 questions)
    Question(
        id="target_audience",
        type=QuestionType.CHOICE,
        text="Who are your primary users?",
        options=[
            "Consumers (B2C)",
            "Businesses (B2B)",
            "Developers",
            "Internal Team",
            "Mixed / Multiple",
        ],
        required=True,
    ),
    Question(
        id="user_roles",
        type=QuestionType.TEXT,
        text="What user roles or types will exist?",
        description="Examples: Admin, Customer, Guest, Premium User",
        required=False,
    ),
    Question(
        id="expected_scale",
        type=QuestionType.CHOICE,
        text="What scale do you expect?",
        options=[
            "Small (100s of users)",
            "Medium (1K - 10K users)",
            "Large (10K - 100K users)",
            "Massive (100K+ users)",
            "Not sure yet",
        ],
        default="Medium (1K - 10K users)",
    ),
    # Section 3: Tech Stack (3-4 questions)
    Question(
        id="preferred_stack",
        type=QuestionType.CHOICE,
        text="Do you have a preferred technology stack?",
        options=[
            "Any / No preference",
            "React / Next.js",
            "Python / Django",
            "Python / FastAPI",
            "Node.js / Express",
            "Ruby on Rails",
            "Go",
            "Rust",
            "Flutter / Dart",
            "Other",
        ],
        default="Any / No preference",
    ),
    Question(
        id="performance_needs",
        type=QuestionType.CONFIRM,
        text="Do you have specific performance requirements?",
        description="Low latency, high throughput, real-time updates?",
        default=False,
    ),
    Question(
        id="integrations",
        type=QuestionType.TEXT,
        text="Any key integrations needed?",
        description="Payment gateways, auth providers, APIs, databases",
        required=False,
    ),
    # Section 4: Features (2-3 questions)
    Question(
        id="core_functionality",
        type=QuestionType.TEXT,
        text="What is the core functionality?",
        description="Describe the main thing this product does",
        required=True,
    ),
    Question(
        id="mvp_scope",
        type=QuestionType.TEXT,
        text="What should be in the MVP (minimum viable product)?",
        description="List the essential features for first release",
        required=True,
    ),
    Question(
        id="nice_to_haves",
        type=QuestionType.TEXT,
        text="Any nice-to-have features for later?",
        description="Features that can be added after MVP",
        required=False,
    ),
    # Section 5: Constraints (2-3 questions)
    Question(
        id="timeline",
        type=QuestionType.CHOICE,
        text="What is your target timeline?",
        options=[
            "ASAP (1-2 weeks)",
            "Short (1 month)",
            "Medium (3 months)",
            "Long (6+ months)",
            "No rush",
        ],
        default="Medium (3 months)",
    ),
    Question(
        id="team_size",
        type=QuestionType.CHOICE,
        text="What is your team size?",
        options=[
            "Solo developer",
            "Small team (2-5)",
            "Medium team (6-15)",
            "Large team (15+)",
        ],
        default="Small team (2-5)",
    ),
    Question(
        id="compliance",
        type=QuestionType.CHOICE,
        text="Any compliance requirements?",
        options=[
            "None",
            "GDPR (Data Privacy)",
            "HIPAA (Healthcare)",
            "SOC 2 (Security)",
            "PCI DSS (Payments)",
            "Other",
        ],
        default="None",
    ),
    # Section 6: AI Preferences (2 questions)
    Question(
        id="coding_style",
        type=QuestionType.CHOICE,
        text="What coding style do you prefer?",
        options=[
            "Clean / Minimal",
            "Verbose / Documented",
            "Performance-focused",
            "Type-safe / Strict",
            "Flexible / Dynamic",
        ],
        default="Clean / Minimal",
    ),
    Question(
        id="primary_ai_tool",
        type=QuestionType.CHOICE,
        text="What is your primary AI coding assistant?",
        options=[
            "Cursor",
            "Claude Code",
            "GitHub Copilot",
            "Roo Code",
            "Continue.dev",
            "Other",
        ],
        required=True,
    ),
]

# Quick mode subset - 5 questions
QUICK_NEW_PROJECT_QUESTIONS = [
    Question(
        id="project_name",
        type=QuestionType.TEXT,
        text="What would you like to name this project?",
        required=True,
    ),
    Question(
        id="project_type",
        type=QuestionType.CHOICE,
        text="What type of application are you building?",
        options=[
            "SaaS (Software as a Service)",
            "Web Application",
            "Mobile App",
            "API / Backend",
            "CLI Tool",
            "Other",
        ],
        required=True,
    ),
    Question(
        id="preferred_stack",
        type=QuestionType.CHOICE,
        text="Do you have a preferred technology stack?",
        options=[
            "Any / No preference",
            "React / Next.js",
            "Python",
            "Node.js",
            "Other",
        ],
        default="Any / No preference",
    ),
    Question(
        id="core_functionality",
        type=QuestionType.TEXT,
        text="What is the core functionality?",
        description="Describe the main thing this product does",
        required=True,
    ),
    Question(
        id="primary_ai_tool",
        type=QuestionType.CHOICE,
        text="What is your primary AI coding assistant?",
        options=[
            "Cursor",
            "Claude Code",
            "GitHub Copilot",
            "Roo Code",
            "Continue.dev",
            "Other",
        ],
        required=True,
    ),
]


class NewProjectMode:
    """Interview mode for new project creation."""

    def __init__(
        self,
        initial_prompt: str,
        console: Console = None,
        quick_mode: bool = False,
    ):
        self.initial_prompt = initial_prompt
        self.console = console or Console()
        self.quick_mode = quick_mode

        # Select questions based on mode
        if quick_mode:
            questions = QUICK_NEW_PROJECT_QUESTIONS
        else:
            questions = NEW_PROJECT_QUESTIONS

        self.engine = InterviewEngine(questions, console)

    def run(self) -> Dict[str, Any]:
        """Run interview and return answers with initial prompt included."""
        answers = self.engine.run()

        # Include the initial prompt
        answers["initial_prompt"] = self.initial_prompt

        return answers
