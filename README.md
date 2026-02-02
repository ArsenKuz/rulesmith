# Rulesmith - AI Rule Generator

An intelligent CLI tool that generates customized AI assistant rules for software projects.

## Features

- **Automatic Stack Detection** - Identifies 10+ technology stacks from project files
- **Intelligent Interview** - Quick (3-5 questions) or Guided (15-20 questions) modes
- **Multi-Tool Output** - Generates rules for Cursor, Claude Code, GitHub Copilot, Roo Code, Continue.dev
- **Modular Rule Library** - YAML-frontmatter Markdown rules that can be combined

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Initialize AI rules for your project
rulesmith init

# Or use quick mode
rulesmith init --quick

# Update rules from library
rulesmith update

# Check project status
rulesmith status
```

## Architecture

- **CLI Foundation** (`cli/`) - Main entry point with stack detection
- **Generator** (`generator/`) - Interview and rule compilation
- **Formatters** (`formatters/`) - Multi-tool output formatting

## Dependencies

See `requirements.txt` for full list.

## License

MIT
