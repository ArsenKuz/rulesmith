<div align="center">

```
    ____           __               __  _       __      
   / __ \___  ____/ /_  ______     / /_(_)___  / /______
  / /_/ / _ \/ __  / / / / __ \   / __/ / __ \/ //_/ __ \
 / _, _/  __/ /_/ / /_/ / /_/ /  / /_/ / / / / ,< / /_/ /
/_/ |_|\___/\__,_/\__,_/ .___/   \__/_/_/ /_/_/|_|\____/ 
                      /_/                                 
```

[![PyPI](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/rulesmith/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**🤖 Intelligent AI Rule Generator for Modern Development Teams**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 What is Rulesmith?

Rulesmith is an intelligent CLI tool that automatically generates customized AI assistant rules for your software projects. It interviews you about your project, detects your technology stack, and creates tailored rules that help AI coding assistants (Cursor, Claude, Copilot, etc.) understand your codebase and coding standards.

No more generic AI suggestions. Get context-aware, project-specific AI assistance.

## ✨ Features

### 🔍 **Smart Stack Detection**
- Automatically identifies **10+ technology stacks** from project files
- Detects frameworks, languages, and tools without manual configuration
- Supports: React, Vue, Angular, Django, Flask, FastAPI, Node.js, Python, Go, Rust, and more

### 💬 **Intelligent Interview System**
- **Quick Mode**: 3-5 targeted questions for fast setup
- **Guided Mode**: 15-20 comprehensive questions for detailed rules
- Context-aware follow-up questions based on your stack
- Skip irrelevant questions with smart filtering

### 🛠️ **Multi-Tool Support**
Generate rules optimized for your favorite AI assistants:

| Tool | Status | Description |
|------|--------|-------------|
| 🎯 **Cursor** | ✅ Supported | `.cursorrules` with context-aware suggestions |
| 🤖 **Claude Code** | ✅ Supported | `CLAUDE.md` with project-specific instructions |
| 🐙 **GitHub Copilot** | ✅ Supported | `.copilot-instructions.md` for inline assistance |
| 🦘 **Roo Code** | ✅ Supported | `.roo/rules/` with structured rule sets |
| ⚡ **Continue.dev** | ✅ Supported | `.continue/rules/` for IDE integration |

### 📦 **Modular Rule Library**
- **YAML-frontmatter Markdown** rules for easy editing
- Combine rules from different domains (frontend, backend, security)
- Version-controlled rule templates
- Custom rule creation and sharing

### 🚀 **Advanced Capabilities**
- **PRD Commander**: Generate rules from Product Requirements Documents
- **API Key Management**: Secure credential handling for LLM providers
- **Rule Sync**: Keep rules updated across team members
- **Status Monitoring**: Track rule freshness and coverage

## 📦 Installation

### From PyPI (Coming Soon)
```bash
pip install rulesmith
```

### From Source
```bash
git clone https://github.com/ArsenKuz/rulesmith.git
cd rulesmith
pip install -e .
```

### Requirements
- Python 3.10 or higher
- pip or conda package manager

## 🚀 Quick Start

### 1. Initialize AI Rules
```bash
# Interactive interview mode
rulesmith init

# Quick mode (5 minutes)
rulesmith init --quick

# Specific directory
rulesmith init /path/to/project
```

### 2. Configure API Keys (Optional)
```bash
# Add OpenAI API key for enhanced PRD generation
rulesmith apikey add openai

# Add Anthropic API key
rulesmith apikey add anthropic
```

### 3. Generate from PRD
```bash
# Create rules from a Product Requirements Document
rulesmith prd ./docs/product-spec.md

# With specific output directory
rulesmith prd ./spec.md --output ./ai-rules/
```

### 4. Update Rules
```bash
# Pull latest rule templates from library
rulesmith update

# Update specific tool rules
rulesmith update --tool cursor --tool claude
```

### 5. Check Status
```bash
# View current rule configuration
rulesmith status

# Detailed breakdown
rulesmith status --verbose
```

## 🎨 Example Output

Rulesmith generates beautifully structured rule files:

```markdown
---
name: my-project-rules
description: React + TypeScript + Node.js project standards
version: 1.0.0
---

## Project Context
- **Framework**: React 18 with TypeScript
- **Backend**: Node.js + Express
- **Database**: PostgreSQL with Prisma ORM
- **Testing**: Jest + React Testing Library

## Coding Standards

### TypeScript
- Strict mode enabled
- Prefer interfaces over types for objects
- Use explicit return types on public functions

### React
- Functional components only
- Custom hooks in `src/hooks/`
- Props interfaces named `{ComponentName}Props`

### Error Handling
- Use `try/catch` with specific error types
- Log errors with structured logging
- Never swallow exceptions silently
```

## 📚 Documentation

### Core Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `init` | Initialize AI rules for project | `rulesmith init [PATH]` |
| `new` | Create new project with AI rules | `rulesmith new PROJECT_NAME` |
| `prd` | Generate rules from PRD | `rulesmith prd <FILE>` |
| `update` | Update rules from library | `rulesmith update` |
| `status` | Check rule configuration | `rulesmith status` |
| `apikey` | Manage API credentials | `rulesmith apikey <action>` |

### Rule Library Structure
```
rulesmith-library/
├── 00-core/
│   ├── communication.md      # Team communication standards
│   ├── documentation.md      # Documentation requirements
│   ├── error-handling.md     # Error handling patterns
│   ├── security-baseline.md  # Security best practices
│   └── code-review.md        # Code review guidelines
└── 10-domains/
    ├── web-frontend.md       # Frontend-specific rules
    └── web-backend.md        # Backend-specific rules
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Rulesmith CLI                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │   Stack     │  │   Interview  │  │    Formatter   │ │
│  │  Detection  │  │    Engine    │  │     Factory    │ │
│  └──────┬──────┘  └──────┬───────┘  └────────┬───────┘ │
│         │                │                    │         │
│         ▼                ▼                    ▼         │
│  ┌──────────────────────────────────────────────────┐ │
│  │              Rule Library                          │ │
│  │  (Modular, composable rule templates)             │ │
│  └──────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Modules

- **`cli/`** - Command-line interface with Typer
- **`generator/`** - Interview engine and rule compilation
- **`formatters/`** - Multi-tool output adapters
- **`rulesmith-library/`** - Reusable rule templates

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/ArsenKuz/rulesmith.git`
3. **Install dev dependencies**: `pip install -e ".[dev]"`
4. **Create a branch**: `git checkout -b feature/amazing-feature`
5. **Make changes** with tests
6. **Run tests**: `pytest`
7. **Format code**: `black . && ruff check .`
8. **Submit PR** with clear description

### Development Setup

```bash
# Clone and setup
git clone https://github.com/ArsenKuz/rulesmith.git
cd rulesmith
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy cli generator formatters

# Linting
ruff check .
black --check .
```

## 🗺️ Roadmap

- [ ] Web interface for visual rule management
- [ ] Team collaboration features
- [ ] IDE extensions (VS Code, IntelliJ)
- [ ] AI-powered rule suggestions
- [ ] Integration with CI/CD pipelines
- [ ] Custom rule marketplace
- [ ] Export to other AI tools (Aider, Codeium, etc.)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for CLI framework
- Inspired by the modern AI coding assistant ecosystem
- Thanks to all contributors and early adopters

---

<div align="center">

**Made with ❤️ for developers who love clean code**

[⭐ Star this repo](https://github.com/ArsenKuz/rulesmith) • [🐛 Report Bug](https://github.com/ArsenKuz/rulesmith/issues) • [💡 Request Feature](https://github.com/ArsenKuz/rulesmith/issues)

</div>
