"""Formatter registry."""

from typing import Dict, Type

from formatters.src.base import BaseFormatter

# Import formatters
from formatters.src.formatters.claude import ClaudeFormatter
from formatters.src.formatters.cursor import CursorFormatter

FORMATTER_REGISTRY: Dict[str, Type[BaseFormatter]] = {
    "cursor": CursorFormatter,
    "claude": ClaudeFormatter,
    # Additional formatters can be added here
}


def get_formatter(tool_id: str) -> Type[BaseFormatter]:
    """Get formatter class by tool ID."""
    if tool_id not in FORMATTER_REGISTRY:
        raise ValueError(f"Unknown formatter: {tool_id}")
    return FORMATTER_REGISTRY[tool_id]


def list_formatters() -> Dict[str, str]:
    """List all available formatters."""
    return {
        tool_id: formatter_class.description
        for tool_id, formatter_class in FORMATTER_REGISTRY.items()
    }
