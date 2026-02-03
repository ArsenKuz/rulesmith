"""Question definitions for interviews."""

from ..models.interview import Question, QuestionType


# Quick mode questions
QUICK_QUESTIONS = [
    Question(
        id="confirm_stack",
        type=QuestionType.CONFIRM,
        text="Detected: {detected_stack}. Is this correct?",
        description="We auto-detected your technology stack.",
        default=True,
    ),
    Question(
        id="project_purpose",
        type=QuestionType.CHOICE,
        text="What's the primary purpose of this project?",
        options=[
            "SaaS / Web Application",
            "E-commerce",
            "Content Site / Blog",
            "Internal Tool",
            "API / Backend Service",
            "Mobile Application",
            "Data/ML Pipeline",
            "Other",
        ],
        required=True,
    ),
    Question(
        id="team_size",
        type=QuestionType.CHOICE,
        text="What's your team size?",
        options=[
            "Solo developer",
            "Small team (2-5)",
            "Medium team (6-15)",
            "Large team (16+)",
        ],
        default="Small team (2-5)",
    ),
    Question(
        id="priority_constraint",
        type=QuestionType.CHOICE,
        text="What's the most important constraint?",
        options=[
            "Performance / Speed",
            "Security / Compliance",
            "Developer Experience",
            "Time to Market",
            "Maintainability",
            "Cost Optimization",
        ],
        default="Developer Experience",
    ),
    Question(
        id="target_tools",
        type=QuestionType.MULTIPLE_CHOICE,
        text="Which AI tools do you use?",
        options=[
            "Cursor",
            "Claude Code",
            "GitHub Copilot",
            "Roo Code",
            "Continue.dev",
            "Other",
        ],
        default=["Cursor", "Claude Code"],
    ),
]
