# Rulesmith Product Requirements Document (PRD)

**Version:** 1.0.0  
**Date:** 2026-02-03  
**Status:** Draft  

---

## Executive Summary

Rulesmith is an intelligent CLI tool that generates customized AI assistant rules for software projects. It detects the technology stack, interviews the developer about project requirements, and outputs formatted rules for multiple AI tools (Cursor, Claude Code, GitHub Copilot, Roo Code, Continue.dev).

### Key Value Propositions
1. **Automatic Stack Detection** - Identifies 10+ technology stacks from project files
2. **Intelligent Interview** - Quick (3-5 questions) or Guided (15-20 questions) modes
3. **Multi-Tool Output** - Generates rules in native formats for all major AI assistants
4. **Modular Rule Library** - YAML-frontmatter Markdown rules that can be combined and extended

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Rulesmith CLI                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Init Cmd   │  │  Update Cmd  │  │     Status Cmd       │   │
│  └──────┬───────┘  └──────────────┘  └──────────────────────┘   │
└─────────┼────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Stack Detection Engine                        │
│   • Parses package.json, requirements.txt, Cargo.toml, etc.     │
│   • Scores matches against known stack signatures                 │
│   • Returns: detected_stack + confidence + signals               │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Generator Orchestrator                        │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│   │   Quick     │  │   Guided    │  │  Rule Compiler      │     │
│   │   Mode      │  │   Mode      │  │  + Requirements Doc │     │
│   │  (3-5 Qs)   │  │  (15-20 Qs) │  │                     │     │
│   └─────────────┘  └─────────────┘  └─────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Tool Formatters                         │
│   ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐  │
│   │ Cursor  │ │ Claude  │ │ Copilot  │ │  Roo   │ │ Continue │  │
│   │ .mdc    │ │ CLAUDE  │ │ .github  │ │ .roo   │ │ .cont... │  │
│   └─────────┘ └─────────┘ └──────────┘ └────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## External Dependencies

### Required Rules Directory Files

The Rulesmith system depends on the existing `/Users/dars/Development/opencode-projects/experiment/Rules` directory which contains:

#### Core Rules (Always Apply) - `/Users/dars/Development/opencode-projects/experiment/Rules/core/`
| File | Purpose | Weight |
|------|---------|--------|
| `communication.md` | When to ask vs act, response style | 100 |
| `security-baseline.md` | Security requirements for all code | 90 |
| `error-handling.md` | Error patterns and recovery | 80 |
| `documentation.md` | Documentation standards | 60 |
| `code-review.md` | Code review checklist | 40 |
| `code-organization.md` | File size limits, naming, imports | 85 |
| `formatting-standards.md` | Ruff, Prettier, linting config | 75 |
| `prd-driven-development.md` | PRD workflow, task breakdown | 95 |

#### Domain Rules - `/Users/dars/Development/opencode-projects/experiment/Rules/domains/`
| File | Applies To | Weight |
|------|------------|--------|
| `web-frontend.md` | `**/*.{tsx,jsx,vue,svelte}` | 70 |
| `web-backend.md` | `**/api/**/*` | 70 |

#### Stack Rules - `/Users/dars/Development/opencode-projects/experiment/Rules/stacks/`
| File | Stack Signature | Weight |
|------|-----------------|--------|
| `nextjs.md` | package.json with `next` | 80 |
| `fastapi-python.md` | requirements.txt with `fastapi` | 80 |

#### Framework Rules - `/Users/dars/Development/opencode-projects/experiment/Rules/frameworks/`
| File | Purpose | Weight |
|------|---------|--------|
| `pipeline-architecture.md` | Domain-driven pipeline patterns | 65 |

#### Testing Rules - `/Users/dars/Development/opencode-projects/experiment/Rules/testing/`
| File | Purpose | Weight |
|------|---------|--------|
| `testing-standards.md` | Testing strategies | 60 |
| `testing-day1.md` | Testing from day 1 | 70 |

#### Performance Rules - `/Users/dars/Development/opencode-projects/experiment/Rules/performance/`
| File | Purpose | Weight |
|------|---------|--------|
| `performance-optimization.md` | Performance guidelines | 55 |

### Rulesmith Library Index - `/Users/dars/Development/opencode-projects/experiment/rulesmith-library/`

The `index.yaml` file provides the machine-readable catalog of all rules with their metadata, file paths, and dependencies.

---

## Component Specifications

### 1. CLI Foundation (`cli/`)

**Location:** `cli/` directory  
**Purpose:** Main entry point and command handling

#### Commands

**`rulesmith init`**
- Detects technology stack
- Runs interview (quick or guided mode)
- Generates rules for selected AI tools
- Creates `.rulesmith/config.json`

**Flags:**
- `--quick` - Fast mode with 3-5 questions
- `--guided` - Comprehensive 15-20 question interview
- `--stack <name>` - Override auto-detection
- `--tools <list>` - Comma-separated list of target tools

**`rulesmith update`**
- Updates rule library from GitHub
- Pulls latest rules from remote repository
- Updates local config with new version

**`rulesmith status`**
- Shows current project configuration
- Lists detected stack and active formatters
- Displays library version and last update

#### Configuration Schema (`.rulesmith/config.json`)

```json
{
  "version": "1.0.0",
  "project_name": "string",
  "project_root": "path",
  "detected_stack": "string",
  "stack_confidence": 0.0-1.0,
  "detected_signals": {},
  "selected_stack": "string | null",
  "generation_mode": "quick | guided",
  "active_formatters": ["cursor", "claude", "copilot"],
  "library_version": "string",
  "library_updated_at": "ISO8601",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

#### Stack Detection Engine

**Detectable Stacks (Minimum 10):**
1. Next.js Full-Stack (Next.js + React + TypeScript)
2. React SPA (Vite/CRA + React)
3. Django + React (Django backend, React frontend)
4. FastAPI + Vue (FastAPI backend, Vue frontend)
5. Laravel (PHP)
6. Ruby on Rails
7. Rust (Actix/Rocket/Axum)
8. Go (Gin/Echo/Fiber)
9. Flutter + Firebase (Mobile)
10. Python Data/ML (Jupyter, pandas, scikit-learn)
11. Express.js API
12. NestJS

**Detection Algorithm:**
1. Collect signals from project files (package.json, requirements.txt, etc.)
2. Score each stack based on weighted criteria
3. Return primary stack with confidence score

### 2. Generator Agent (`generator/`)

**Location:** `generator/` directory  
**Purpose:** Interview users and compile rules

#### Interview Engine

**Question Types:**
- `text` - Free text input
- `choice` - Single selection from options
- `multiple_choice` - Multiple selections
- `confirm` - Yes/No question
- `path` - File/directory path

**Quick Mode Questions (3-5):**
1. Confirm detected stack
2. Project purpose (SaaS, E-commerce, API, etc.)
3. Team size
4. Primary constraint (Performance, Security, DX, etc.)
5. Target AI tools (Cursor, Claude, Copilot, etc.)

**Guided Mode Questions (15-20):**
- Section 1: Project Context (3-4 Qs)
- Section 2: Architecture & Design (3-4 Qs)
- Section 3: Development Practices (4-5 Qs)
- Section 4: Constraints & Priorities (3-4 Qs)
- Section 5: AI Tools & Integration (3-4 Qs)

#### Rule Compiler

**Compilation Process:**
1. Load library index.yaml
2. Get core rules (alwaysApply: true)
3. Get stack-specific rules from detected stack
4. Select domain rules based on interview answers
5. Resolve all includes and dependencies recursively
6. Sort by weight (highest first)
7. Personalize content with interview answers

**Output Format:**
```python
{
  "id": "rule-id",
  "description": "Rule description",
  "globs": "**/*.py",
  "alwaysApply": true,
  "weight": 100,
  "content": "# Markdown content...",
  "category": "core | stack | domain"
}
```

#### Requirements Document Generator

Creates a PRD-style document based on interview answers including:
- Project overview and characteristics
- Technology stack details
- Development practices (testing, code review, documentation)
- Constraints and priorities
- AI assistant configuration
- Rule generation summary

### 3. Multi-Tool Formatters (`formatters/`)

**Location:** `formatters/` directory  
**Purpose:** Convert compiled rules to each AI tool's native format

#### Cursor Formatter

**Output:** `.cursor/rules/*.mdc`
**Format:** YAML frontmatter + Markdown body

**Filename Convention:**
- `00-core-{index}-{rule-id}.mdc` - Core rules (alwaysApply)
- `10-high-{index}-{rule-id}.mdc` - High weight (≥70)
- `20-medium-{index}-{rule-id}.mdc` - Medium weight (40-69)
- `30-low-{index}-{rule-id}.mdc` - Low weight (<40)
- `99-project-summary.mdc` - Project overview

#### Claude Code Formatter

**Output:** `CLAUDE.md` (single file)
**Format:** Structured Markdown sections

**Structure:**
1. Project Overview
2. Core Principles (alwaysApply rules)
3. Stack-Specific Guidelines
4. Domain-Specific Patterns
5. Communication Preferences
6. Additional Context

#### GitHub Copilot Formatter

**Output:** `.github/copilot-instructions.md`
**Format:** Markdown with structured guidelines

**Structure:**
1. Project Context
2. Coding Standards
3. Pull Request Guidelines
4. Testing Approach
5. Additional Notes

#### Roo Code Formatter

**Output:** `.roo/rules/*.md`
**Format:** Similar to Cursor but different path

#### Continue.dev Formatter

**Output:** `.continuerules` (single file)
**Format:** Concatenated rules with separators

---

## File Structure

```
rulesmith/
├── PRD.md                          # This document
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup
├── pyproject.toml                  # Modern Python packaging
├── .gitignore                      # Git ignore rules
│
├── cli/                            # CLI Foundation (Agent 1)
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                 # Entry point
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── init.py            # Init command
│   │   │   ├── update.py          # Update command
│   │   │   └── status.py          # Status command
│   │   ├── detectors/
│   │   │   ├── __init__.py
│   │   │   ├── stack_detector.py  # Detection engine
│   │   │   └── signals/           # Signal detectors
│   │   │       ├── __init__.py
│   │   │       ├── javascript.py
│   │   │       ├── python.py
│   │   │       ├── rust.py
│   │   │       ├── go.py
│   │   │       └── ...
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── manager.py         # Config I/O
│   │   │   └── schema.py          # Pydantic models
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── paths.py           # Path utilities
│   │       └── github.py          # GitHub API client
│   └── tests/
│       ├── __init__.py
│       ├── test_commands/
│       ├── test_detectors/
│       └── fixtures/
│
├── generator/                      # Generator Agent (Agent 3)
│   ├── src/
│   │   ├── __init__.py
│   │   ├── orchestrator.py        # Main workflow
│   │   ├── modes/
│   │   │   ├── __init__.py
│   │   │   ├── quick.py          # Quick mode
│   │   │   └── guided.py         # Guided mode
│   │   ├── interview/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py         # Interview engine
│   │   │   ├── questions.py      # Question definitions
│   │   │   └── adapters.py       # CLI adapters
│   │   ├── assembly/
│   │   │   ├── __init__.py
│   │   │   ├── compiler.py       # Rule compiler
│   │   │   ├── resolver.py       # Dependency resolver
│   │   │   └── context.py        # Context builder
│   │   ├── requirements/
│   │   │   ├── __init__.py
│   │   │   ├── generator.py      # PRD generator
│   │   │   └── templates/
│   │   │       └── requirements.md
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── interview.py      # Interview models
│   │       ├── assembly.py       # Assembly models
│   │       └── requirements.py   # Requirements models
│   └── tests/
│
├── formatters/                     # Multi-Tool Formatters (Agent 4)
│   ├── src/
│   │   ├── __init__.py
│   │   ├── base.py               # Base formatter
│   │   ├── registry.py           # Formatter registry
│   │   ├── sync.py              # Sync engine
│   │   ├── formatters/
│   │   │   ├── __init__.py
│   │   │   ├── cursor.py        # Cursor (.mdc)
│   │   │   ├── claude.py        # Claude Code (CLAUDE.md)
│   │   │   ├── copilot.py       # GitHub Copilot
│   │   │   ├── roo.py          # Roo Code
│   │   │   └── continue_dev.py  # Continue.dev
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_writer.py   # File operations
│   │       └── template.py      # Template utilities
│   └── tests/
│
└── scripts/                        # Build & utility scripts
    ├── setup.sh                   # Initial setup
    ├── test.sh                    # Run tests
    └── validate.py                # Rule validation
```

---

## Build Instructions

### Phase 1: Project Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install typer>=0.9.0 pydantic>=2.0.0 pyyaml>=6.0 requests>=2.31.0 rich>=13.0.0 pathspec>=0.11.0 jinja2>=3.1.0
   ```

### Phase 2: Build CLI Foundation

**Reference Files:**
- `/Users/dars/Development/opencode-projects/experiment/agent1-cli-foundation-PLAN.md`

**Tasks:**
1. Create CLI structure with Typer
2. Implement `init`, `update`, `status` commands
3. Build stack detection engine with 10+ detectors
4. Create configuration manager
5. Add tests with fixtures

**Key Implementation Details:**
- Use Pydantic for config validation
- Use Rich for terminal formatting
- Support `--quick`, `--guided`, `--stack` flags
- Detect stacks from package.json, requirements.txt, etc.

### Phase 3: Build Generator

**Reference Files:**
- `/Users/dars/Development/opencode-projects/experiment/agent3-generator-PLAN.md`

**Tasks:**
1. Build interview engine with Rich prompts
2. Create Quick mode (3-5 questions)
3. Create Guided mode (15-20 questions)
4. Implement rule compiler with dependency resolution
5. Build requirements document generator with Jinja2

**Key Implementation Details:**
- Support text, choice, multiple_choice, confirm, path question types
- Resolve rule includes recursively
- Sort rules by weight (highest first)
- Generate PRD-style requirements doc

### Phase 4: Build Formatters

**Reference Files:**
- `/Users/dars/Development/opencode-projects/experiment/agent4-formatters-PLAN.md`

**Tasks:**
1. Create base formatter interface
2. Implement Cursor formatter (.mdc files)
3. Implement Claude formatter (CLAUDE.md)
4. Implement Copilot formatter (copilot-instructions.md)
5. Implement Roo and Continue formatters
6. Build sync engine

**Key Implementation Details:**
- All formatters inherit from BaseFormatter
- Use YAML frontmatter for Cursor (.mdc)
- Single file output for Claude and Copilot
- Use weight field for rule prioritization
- Validate generated output

### Phase 5: Integration & Testing

**Tasks:**
1. Wire CLI commands to generator
2. Wire generator to formatters
3. Add library loading from Rules directory
4. Create integration tests
5. Validate all output formats

---

## Dependencies

### Core Dependencies
```
typer>=0.9.0          # CLI framework
pydantic>=2.0.0       # Data validation
pyyaml>=6.0           # YAML parsing
requests>=2.31.0      # HTTP client
rich>=13.0.0          # Terminal UI
pathspec>=0.11.0      # Glob patterns
jinja2>=3.1.0         # Templating
```

### Development Dependencies
```
pytest>=7.0.0         # Testing
pytest-cov>=4.0.0     # Coverage
black>=23.0.0         # Formatting
ruff>=0.1.0           # Linting
mypy>=1.0.0           # Type checking
```

---

## Testing Strategy

### Unit Tests
- Test each detector with sample project structures
- Test config serialization/deserialization
- Test CLI argument parsing
- Test rule compiler with mock rules
- Test each formatter with sample rules

### Integration Tests
- Test full `init` flow with sample projects
- Test `update` command (mock GitHub API)
- Test `status` command with various configs
- Test multi-formatter sync

### Test Fixtures
Create minimal project structures in `tests/fixtures/`:
```
fixtures/
├── nextjs-project/
│   ├── package.json (with next dependency)
│   └── app/
├── django-project/
│   ├── requirements.txt (with django)
│   └── manage.py
├── rust-project/
│   ├── Cargo.toml
│   └── src/
└── ...
```

---

## Acceptance Criteria

### CLI Foundation
- [ ] All 3 commands work: init, update, status
- [ ] Detects at least 10 different technology stacks
- [ ] Confidence score calculation works correctly
- [ ] Configuration persists correctly to `.rulesmith/config.json`
- [ ] Library update pulls from GitHub (or local Rules dir)
- [ ] CLI help text is comprehensive
- [ ] Error handling is robust

### Generator
- [ ] Quick mode asks 3-5 questions, completes in <2 minutes
- [ ] Guided mode asks 15-20 questions, covers all aspects
- [ ] Interview engine supports all question types
- [ ] Rule compiler correctly resolves includes
- [ ] Compiled rules are sorted by weight
- [ ] Requirements document is generated correctly
- [ ] Can override detected stack with manual selection

### Formatters
- [ ] Cursor formatter creates valid .mdc files
- [ ] Claude formatter creates valid CLAUDE.md
- [ ] Copilot formatter creates valid copilot-instructions.md
- [ ] All formatters handle multiple rules correctly
- [ ] File naming conventions are consistent
- [ ] Registry system allows adding new formatters
- [ ] Sync engine updates all formatters in one call

### Overall
- [ ] All tests pass (>80% coverage)
- [ ] Documentation is complete
- [ ] Code follows style guidelines (Ruff/Black)
- [ ] No security vulnerabilities
- [ ] Performance is acceptable (<5s for init command)

---

## Reference Documents

### Agent Plans (Implementation Details)
1. **Agent 1 - CLI Foundation:** `/Users/dars/Development/opencode-projects/experiment/agent1-cli-foundation-PLAN.md`
2. **Agent 2 - Rule Library:** `/Users/dars/Development/opencode-projects/experiment/agent2-rule-library-PLAN.md`
3. **Agent 3 - Generator:** `/Users/dars/Development/opencode-projects/experiment/agent3-generator-PLAN.md`
4. **Agent 4 - Formatters:** `/Users/dars/Development/opencode-projects/experiment/agent4-formatters-PLAN.md`

### Rules Library
- **Rules Directory:** `/Users/dars/Development/opencode-projects/experiment/Rules/`
- **Library Index:** `/Users/dars/Development/opencode-projects/experiment/rulesmith-library/index.yaml`
- **Library README:** `/Users/dars/Development/opencode-projects/experiment/Rules/README.md`

### Example Rule Files to Study
- **Communication:** `/Users/dars/Development/opencode-projects/experiment/Rules/core/communication.md`
- **Security:** `/Users/dars/Development/opencode-projects/experiment/Rules/core/security-baseline.md`
- **PRD-Driven:** `/Users/dars/Development/opencode-projects/experiment/Rules/core/prd-driven-development.md`
- **Next.js Stack:** `/Users/dars/Development/opencode-projects/experiment/Rules/stacks/nextjs.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-03 | Initial PRD |

---

## Next Steps

1. ✅ Create rulesmith directory and initialize git
2. ✅ Create PRD document
3. ⏳ Set up project structure
4. ⏳ Build CLI foundation
5. ⏳ Build Generator
6. ⏳ Build Formatters
7. ⏳ Integration and testing
