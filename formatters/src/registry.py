"""Formatter registry for discovering and managing formatters."""

from typing import Dict, Type

# Handle both relative and absolute imports
try:
    from .base import BaseFormatter
except ImportError:
    from base import BaseFormatter

# Registry storage - initialized lazily
_formatter_registry: Dict[str, Type[BaseFormatter]] = {}


def _ensure_registry():
    """Initialize registry lazily to avoid circular imports."""
    global _formatter_registry
    if _formatter_registry:
        return

    try:
        from .formatters.cursor import CursorFormatter
        from .formatters.claude import ClaudeFormatter
        from .formatters.copilot import CopilotFormatter
        from .formatters.roo import RooFormatter
        from .formatters.continue_dev import ContinueDevFormatter
    except ImportError:
        from formatters.cursor import CursorFormatter
        from formatters.claude import ClaudeFormatter
        from formatters.copilot import CopilotFormatter
        from formatters.roo import RooFormatter
        from formatters.continue_dev import ContinueDevFormatter

    _formatter_registry.update(
        {
            "cursor": CursorFormatter,
            "claude": ClaudeFormatter,
            "copilot": CopilotFormatter,
            "roo": RooFormatter,
            "continue": ContinueDevFormatter,
        }
    )


def get_formatter(tool_id: str) -> Type[BaseFormatter]:
    """Get formatter class by tool ID."""
    _ensure_registry()
    if tool_id not in _formatter_registry:
        raise ValueError(f"Unknown formatter: {tool_id}")
    return _formatter_registry[tool_id]


def list_formatters() -> Dict[str, str]:
    """List all available formatters."""
    _ensure_registry()
    return {
        tool_id: formatter_class.description
        for tool_id, formatter_class in _formatter_registry.items()
    }


def register_formatter(tool_id: str, formatter_class: Type[BaseFormatter]) -> None:
    """Register a new formatter."""
    _ensure_registry()
    _formatter_registry[tool_id] = formatter_class


def unregister_formatter(tool_id: str) -> None:
    """Unregister a formatter."""
    _ensure_registry()
    if tool_id in _formatter_registry:
        del _formatter_registry[tool_id]


# Backward compatibility alias
FORMATTER_REGISTRY = _formatter_registry
