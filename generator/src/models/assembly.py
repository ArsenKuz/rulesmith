"""Models for rule assembly results."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class CompiledRule(BaseModel):
    """A compiled rule ready for output."""

    id: str
    description: str
    globs: str = "*"
    alwaysApply: bool = False
    weight: int = 50
    content: str
    frontmatter: Dict[str, Any]
    category: Optional[str] = None


class AssemblyResult(BaseModel):
    """Result of the rule assembly process."""

    rules: List[CompiledRule]
    selected_stack: str
    total_rules: int
    core_rules_count: int
    stack_rules_count: int
    domain_rules_count: int
