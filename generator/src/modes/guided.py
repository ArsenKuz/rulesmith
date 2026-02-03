"""Guided mode: 15-20 question comprehensive interview."""

from typing import Dict, Any, List
from rich.console import Console
from ..interview.engine import InterviewEngine
from ..models.interview import Question, QuestionType


# Guided mode questions
GUIDED_QUESTIONS = [
    # Section 1: Project Context (3-4 questions)
    Question(
        id="project_name",
        type=QuestionType.TEXT,
        text="What's the project name?",
        required=True,
    ),
    Question(
        id="project_description",
        type=QuestionType.TEXT,
        text="Describe the project in 1-2 sentences.",
        description="What problem does it solve? Who are the users?",
        required=True,
    ),
    Question(
        id="confirm_stack",
        type=QuestionType.CONFIRM,
        text="Detected: {detected_stack}. Is this correct?",
        default=True,
    ),
    Question(
        id="manual_stack",
        type=QuestionType.CHOICE,
        text="Select your technology stack:",
        options=[
            "Next.js Full-Stack",
            "React SPA",
            "Django + React",
            "FastAPI + Vue",
            "Laravel",
            "Ruby on Rails",
            "Rust (Actix/Rocket)",
            "Go (Gin/Echo)",
            "Flutter + Firebase",
            "Python Data/ML",
            "Other",
        ],
        skip_if="confirm_stack == true",
    ),
    # Section 2: Architecture & Design (3-4 questions)
    Question(
        id="architecture_pattern",
        type=QuestionType.CHOICE,
        text="What architecture pattern do you follow?",
        options=[
            "Monolithic",
            "Microservices",
            "Serverless",
            "Modular Monolith",
            "Not sure / Don't care",
        ],
        default="Not sure / Don't care",
    ),
    Question(
        id="state_management",
        type=QuestionType.CHOICE,
        text="How do you handle state management?",
        options=[
            "Redux/Zustand",
            "React Context",
            "Database only",
            "Local storage",
            "Custom solution",
            "Not applicable (backend only)",
        ],
        skip_if="manual_stack contains backend only",
    ),
    Question(
        id="api_style",
        type=QuestionType.CHOICE,
        text="What API style do you prefer?",
        options=[
            "REST",
            "GraphQL",
            "tRPC",
            "gRPC",
            "Not applicable (frontend only)",
        ],
        default="REST",
    ),
    # Section 3: Development Practices (4-5 questions)
    Question(
        id="testing_approach",
        type=QuestionType.CHOICE,
        text="What's your testing approach?",
        options=[
            "TDD (Test-Driven Development)",
            "Write tests after implementation",
            "Minimal testing (smoke tests only)",
            "No formal testing",
            "Not sure",
        ],
        default="Write tests after implementation",
    ),
    Question(
        id="code_review",
        type=QuestionType.CHOICE,
        text="How do you handle code review?",
        options=[
            "All code must be reviewed",
            "Review for major changes only",
            "Self-review with automated checks",
            "No formal review process",
            "Not sure",
        ],
    ),
    Question(
        id="documentation_level",
        type=QuestionType.CHOICE,
        text="What level of documentation do you maintain?",
        options=[
            "Comprehensive (API docs, ADRs, runbooks)",
            "Moderate (README + inline comments)",
            "Minimal (README only)",
            "No documentation",
            "Not sure",
        ],
        default="Moderate (README + inline comments)",
    ),
    Question(
        id="code_style",
        type=QuestionType.CHOICE,
        text="How strict are your code style guidelines?",
        options=[
            "Very strict (enforced by CI)",
            "Moderate (linter warnings)",
            "Loose (suggestions only)",
            "No style guidelines",
            "Not sure",
        ],
        default="Moderate (linter warnings)",
    ),
    # Section 4: Constraints & Priorities (3-4 questions)
    Question(
        id="performance_critical",
        type=QuestionType.CONFIRM,
        text="Is performance critical for this project?",
        description="Low latency, high throughput requirements?",
        default=False,
    ),
    Question(
        id="security_compliance",
        type=QuestionType.CHOICE,
        text="Any security/compliance requirements?",
        options=[
            "None",
            "SOC 2",
            "GDPR",
            "HIPAA",
            "PCI DSS",
            "Other",
        ],
        default="None",
    ),
    Question(
        id="scalability_concerns",
        type=QuestionType.CHOICE,
        text="What are your scalability expectations?",
        options=[
            "Small scale (< 1000 users)",
            "Medium scale (1K - 100K users)",
            "Large scale (100K+ users)",
            "Massive scale (millions+)",
            "Not sure",
        ],
        default="Medium scale (1K - 100K users)",
    ),
    # Section 5: AI Tools & Integration (3-4 questions)
    Question(
        id="primary_ai_tool",
        type=QuestionType.CHOICE,
        text="What's your primary AI coding assistant?",
        options=[
            "Cursor",
            "Claude Code",
            "GitHub Copilot",
            "Roo Code",
            "Continue.dev",
            "Multiple tools",
            "Other",
        ],
        required=True,
    ),
    Question(
        id="secondary_tools",
        type=QuestionType.MULTIPLE_CHOICE,
        text="Any secondary AI tools?",
        options=[
            "Cursor",
            "Claude Code",
            "GitHub Copilot",
            "Roo Code",
            "Continue.dev",
            "None",
        ],
        default=["None"],
    ),
    Question(
        id="ai_experience_level",
        type=QuestionType.CHOICE,
        text="What's the team's experience with AI assistants?",
        options=[
            "Experts (using AI daily for months)",
            "Intermediate (regular users)",
            "Beginners (just getting started)",
            "Mixed levels",
        ],
        default="Intermediate (regular users)",
    ),
    Question(
        id="additional_notes",
        type=QuestionType.TEXT,
        text="Any additional notes or special requirements?",
        description="Specific patterns, conventions, or constraints not covered above.",
        required=False,
    ),
]


class GuidedMode:
    """Comprehensive guided interview mode."""

    def __init__(self, detected_stack: str, console: Console = None):
        self.detected_stack = detected_stack
        self.engine = InterviewEngine(self._prepare_questions(), console)

    def _prepare_questions(self) -> List[Question]:
        """Inject context and organize questions into sections."""
        questions = []
        for q in GUIDED_QUESTIONS:
            question_data = q.model_dump()
            # Replace template variables
            text = question_data.get("text", "")
            if "{detected_stack}" in text:
                question_data["text"] = text.format(detected_stack=self.detected_stack)
            questions.append(Question(**question_data))
        return questions

    def run(self) -> Dict[str, Any]:
        """Run guided interview and return comprehensive answers."""
        return self.engine.run()
