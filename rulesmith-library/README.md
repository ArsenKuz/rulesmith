# Rulesmith Library

A modular rule template system for AI coding assistants, stored as YAML frontmatter + Markdown.

## Structure

```
rulesmith-library/
├── 00-core/          # Universal rules (apply to ALL projects)
├── 10-domains/       # Domain-specific categories
├── 20-stacks/        # Complete stack definitions
├── 30-frameworks/    # Framework deep-dives
├── 40-patterns/      # Cross-cutting patterns
└── index.yaml        # Machine-readable catalog
```

## Rule Format

Every rule file uses YAML frontmatter with Markdown body:

```yaml
---
description: "Clear one-line description"
globs: "**/*.py"
alwaysApply: false
weight: 50
tags:
  - python
  - backend
---

# Rule Content

## Section
Content here...
```

## Usage

1. Include relevant rules in your AI assistant configuration
2. Rules are automatically matched via `globs` patterns
3. `alwaysApply: true` rules are always included
4. Higher `weight` values take precedence

## License

MIT
