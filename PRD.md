# Rulesmith Product Requirements Document (PRD) v2.0

**Version:** 2.0.0  
**Date:** 2026-02-03  
**Status:** Active  

---

## Executive Summary

Rulesmith is an **AI-powered project setup agent** that helps developers bootstrap new projects from scratch or configure existing ones. It combines LLM-powered PRD generation with intelligent rule selection to provide a complete development setup.

### Two Operating Modes

**Mode 1: New Project (from 0)** 🆕
- User provides a basic idea/prompt
- Agent interviews to refine requirements
- **Generates production-ready PRD** via LLM
- Selects optimal rules based on PRD analysis
- Outputs AI assistant rules + PRD document

**Mode 2: Existing Project** 🔍
- Detects technology stack from files
- Maps to appropriate rules from `/rules` library
- Outputs AI assistant rules

### Key Value Propositions
1. **Zero-to-Production PRDs** - Generates comprehensive PRDs from simple prompts via LLM
2. **Intelligent Rule Curation** - Selects best rules based on PRD content or stack detection
3. **AI Assistant Ready** - Outputs rules for Cursor, Claude Code, Copilot, Roo, Continue.dev
4. **Extensible Architecture** - Plugin system for future schemas and skills

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Rulesmith CLI Agent                                  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         MODE SELECTION                                │  │
│  │                    (new project / existing project)                   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                        │
│                    ▼                               ▼                        │
│  ┌───────────────────────────────┐    ┌───────────────────────────────┐     │
│  │     MODE 1: NEW PROJECT       │    │    MODE 2: EXISTING PROJECT   │     │
│  │      (Greenfield Setup)       │    │      (Brownfield Detection)   │     │
│  └───────────────────────────────┘    └───────────────────────────────┘     │
│                    │                               │                        │
│  ┌─────────────────┴──────────┐       ┌──────────┴─────────────────┐        │
│  │  1. Initial Prompt         │       │  1. Stack Detection        │        │
│  │     (User's idea)          │       │     (Parse files)          │        │
│  │                            │       │                            │        │
│  │  2. Clarification Interview│       │  2. Identify Tech Stack    │        │
│  │     (10-15 questions)      │       │     (Match signatures)     │        │
│  │                            │       │                            │        │
│  │  3. LLM PRD Generation     │       │  3. Quick Context Qs       │        │
│  │     (GPT-4/Claude)         │       │     (Team size, etc)       │        │
│  │                            │       │                            │        │
│  │  4. Parse PRD → Stack      │       │  4. Map to Rules           │        │
│  │     (Extract requirements) │       │     (Library lookup)       │        │
│  └────────────────────────────┘       └────────────────────────────┘        │
│                    │                               │                        │
│                    └───────────────┬───────────────┘                        │
│                                    ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      SHARED: RULE SELECTION                           │  │
│  │     (Select from /rules library based on stack/domain/context)        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     RULE COMPILATION & ASSEMBLY                       │  │
│  │     (Resolve dependencies, personalize, sort by weight)               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     MULTI-TOOL FORMATTERS                             │  │
│  │  ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐        │  │
│  │  │ Cursor  │ │ Claude  │ │ Copilot  │ │  Roo   │ │ Continue │        │  │
│  │  │ .mdc    │ │ CLAUDE  │ │ .github  │ │ .roo   │ │ .cont... │        │  │
│  │  └─────────┘ └─────────┘ └──────────┘ └────────┘ └──────────┘        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         OUTPUT                                        │  │
│  │  • PRD.md (Mode 1 only)                                               │  │
│  │  • AI assistant rules (all modes)                                     │  │
│  │  • .rulesmith/config.json                                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Mode 1: New Project Workflow (Primary)

### Phase 1: Project Conception

**Input:** User's initial idea/prompt
```bash
rulesmith new "I want to build a SaaS platform for pet groomers \
              to manage appointments and handle payments"
```

**Process:**
1. Capture initial prompt
2. Display confirmation and scope estimate
3. Begin clarification interview

### Phase 2: Clarification Interview

**Duration:** 10-15 questions, ~5 minutes

**Question Categories:**

| Category | Questions | Purpose |
|----------|-----------|---------|
| **Basics** | 2-3 | Project name, type (SaaS, API, Mobile, etc.) |
| **Users** | 2-3 | Target audience, user roles, scale |
| **Tech** | 3-4 | Preferred stack (if any), performance needs, integrations |
| **Features** | 2-3 | Core functionality, MVP scope, nice-to-haves |
| **Constraints** | 2-3 | Timeline, budget, team size, compliance |
| **AI Preferences** | 2 | Coding style, documentation level, review process |

**Example Questions:**
1. "What type of application is this?" [SaaS / API / Mobile / CLI / Desktop]
2. "Who are your primary users?" [Consumers / Businesses / Developers]
3. "Any preferred tech stack?" [Any / React/Node / Python / Go / Specific]
4. "Expected user scale?" [100s / 1000s / 10000s / Millions]
5. "Timeline constraint?" [ASAP / 3 months / 6 months / No rush]
6. "Compliance requirements?" [GDPR / HIPAA / SOC2 / None]

### Phase 3: LLM PRD Generation

**Prompt Engineering:**
- Combine user prompt + interview answers
- Structured output with sections
- Reference schema for consistency

**LLM Call Structure:**
```
System: You are a technical product manager creating PRDs.
       Use the provided schema and best practices.

Context:
- User's idea: {initial_prompt}
- Project type: {project_type}
- Users: {target_users}
- Scale: {expected_scale}
- Stack preference: {preferred_stack}
- Timeline: {timeline}
- Constraints: {constraints}

Generate a comprehensive PRD with:
1. Executive Summary
2. Goals & Objectives
3. User Stories & Use Cases
4. Functional Requirements
5. Non-Functional Requirements
6. Technical Architecture
7. Data Model
8. API Design
9. UI/UX Considerations
10. Implementation Phases
11. Testing Strategy
12. Deployment Plan
13. Success Metrics
```

**Output:** `PRD.md` file in project directory

### Phase 4: PRD Analysis & Stack Extraction

**Automated Parsing:**
- Extract tech stack recommendations from PRD
- Identify domains (frontend, backend, database, etc.)
- Detect performance/security requirements
- Map to available rules

**Stack Resolution Logic:**
```python
if PRD suggests "React + Node.js + PostgreSQL":
    stack = "nextjs-fullstack"
elif PRD suggests "Python + FastAPI":
    stack = "fastapi-python"
# etc.
```

### Phase 5: Rule Selection & Formatting

Same as Mode 2 (see below), but using PRD-derived stack instead of file detection.

---

## Mode 2: Existing Project Workflow

### Phase 1: Stack Detection

**Detection Sources:**
| File | Stack Indicators |
|------|-----------------|
| `package.json` | next, react, vue, express |
| `requirements.txt` | django, flask, fastapi |
| `Cargo.toml` | actix-web, rocket, axum |
| `go.mod` | gin, echo, fiber |
| `Gemfile` | rails, sinatra |
| `composer.json` | laravel, symfony |
| `pubspec.yaml` | flutter |

### Phase 2: Quick Context Questions

Even for existing projects, ask:
1. "Confirm this is a {detected_stack} project?"
2. "Team size?" (affects communication rules)
3. "Primary constraint?" (performance, security, DX)
4. "Target AI tools?" (cursor, claude, copilot, etc.)

### Phase 3: Rule Selection

**Selection Criteria:**
- **Core rules** - Always included (communication, security, error-handling)
- **Stack rules** - Based on detected/selected technology
- **Domain rules** - Based on project type (web, mobile, api, etc.)
- **Requirement rules** - Based on context (testing, performance, etc.)

---

## Rule Library Structure

### External Rules Directory
**Location:** `/Users/dars/Development/opencode-projects/experiment/Rules/`

**Organization:**
```
Rules/
├── core/              # Universal rules (always apply)
│   ├── communication.md
│   ├── security-baseline.md
│   ├── error-handling.md
│   ├── documentation.md
│   ├── prd-driven-development.md
│   ├── code-organization.md
│   ├── formatting-standards.md
│   └── code-review.md
├── domains/           # Domain-specific
│   ├── web-frontend.md
│   ├── web-backend.md
│   ├── mobile-app.md
│   └── cli-tool.md
├── stacks/            # Technology stacks
│   ├── nextjs.md
│   ├── fastapi-python.md
│   ├── django-react.md
│   ├── react-spa.md
│   ├── flutter-firebase.md
│   └── rust-actix.md
├── frameworks/        # Architecture patterns
│   ├── pipeline-architecture.md
│   └── microservices.md
├── testing/           # Testing strategies
│   ├── testing-standards.md
│   └── testing-day1.md
├── security/          # Security specifics
│   └── security-compliance.md
└── performance/       # Optimization
    └── performance-optimization.md
```

### Rule Format

Each rule is a Markdown file with YAML frontmatter:

```markdown
---
description: Brief description
globs: "**/*.py"           # File patterns
alwaysApply: false         # Always include?
weight: 70                 # Priority (100=highest)
includes:                  # Dependencies
  - security-baseline
  - error-handling
---

# Rule Title

## Context
When to use this rule...

## Requirements
1. Specific requirement
2. Another requirement

## Examples

### Good
```python
# Good example
```

### Bad
```python
# Bad example
```
```

---

## Component Specifications

### 1. CLI Module (`cli/`)

**Primary Commands:**

```bash
# Mode 1: New project
rulesmith new "your idea here" [--guided] [--output ./my-project]

# Mode 2: Existing project
rulesmith init [path] [--quick] [--guided]

# Other commands
rulesmith status              # Show current config
rulesmith update              # Update rule library
rulesmith doctor              # Diagnose issues
```

**Command: `rulesmith new`**
- Accepts initial prompt as argument
- Runs clarification interview
- Calls LLM to generate PRD
- Analyzes PRD to select rules
- Outputs PRD + AI assistant rules

**Command: `rulesmith init`**
- Detects existing project stack
- Runs brief context interview
- Selects rules based on stack
- Outputs AI assistant rules

### 2. Interview Engine (`generator/src/interview/`)

**Architecture:**
- Question definitions with branching logic
- Rich terminal UI (colors, progress bars)
- Adaptive questioning based on previous answers
- Support for text, choice, multiple-choice, confirm inputs

**Key Features:**
- Skip logic (e.g., skip scaling questions for CLI tools)
- Validation (ensure required fields answered)
- Save/resume (can interrupt and continue)
- Templates (pre-defined question sets for project types)

### 3. LLM Integration (`generator/src/llm/`)

**New Component - To Be Built:**

```python
class PRDGenerator:
    """Generates PRDs via LLM API."""
    
    def generate(
        self,
        initial_prompt: str,
        interview_answers: Dict,
        model: str = "gpt-4"
    ) -> str:
        # Construct system + user prompts
        # Call LLM API
        # Parse and validate output
        # Return markdown PRD
```

**Supported Providers:**
- OpenAI (GPT-4, GPT-4-turbo)
- Anthropic (Claude 3 Opus/Sonnet)
- Local models (via Ollama/LM Studio)

**Configuration:**
```json
{
  "llm_provider": "openai",
  "llm_model": "gpt-4",
  "llm_api_key": "sk-...",
  "prd_template": "default",
  "max_tokens": 4000
}
```

### 4. PRD Parser (`generator/src/parser/`)

**New Component - To Be Built:**

```python
class PRDParser:
    """Extracts structured data from LLM-generated PRD."""
    
    def parse(self, prd_content: str) -> ParsedPRD:
        # Extract tech stack suggestions
        # Identify domains
        # Detect requirements
        # Return structured object
```

**Extracted Fields:**
- Suggested tech stack
- Architecture type (monolith, microservices, serverless)
- Database type (SQL, NoSQL, both)
- API style (REST, GraphQL, gRPC)
- Frontend framework (if applicable)
- Performance requirements
- Security/compliance needs

### 5. Rule Compiler (`generator/src/assembly/`)

**Enhanced for dual modes:**

```python
class RuleCompiler:
    def compile_for_new_project(
        self,
        parsed_prd: ParsedPRD,
        interview_answers: Dict
    ) -> List[CompiledRule]:
        # 1. Get core rules
        # 2. Get stack rules from PRD
        # 3. Get domain rules from project type
        # 4. Get requirement rules (testing, perf, etc.)
        # 5. Resolve dependencies
        # 6. Sort by weight
        # 7. Personalize with context
        pass
    
    def compile_for_existing_project(
        self,
        detected_stack: str,
        interview_answers: Dict
    ) -> List[CompiledRule]:
        # Similar but uses detected stack instead of PRD
        pass
```

### 6. Formatters (`formatters/`)

**Target Outputs:**

| Tool | Format | Location |
|------|--------|----------|
| Cursor | `.mdc` files | `.cursor/rules/` |
| Claude Code | `CLAUDE.md` | Project root |
| GitHub Copilot | `copilot-instructions.md` | `.github/` |
| Roo Code | `.md` files | `.roo/rules/` |
| Continue.dev | `.continuerules` | Project root |

**Shared Features:**
- Rule prioritization by weight
- File naming conventions with sorting prefixes
- Validation of generated output
- Atomic file writes

---

## File Structure

```
rulesmith/
├── PRD.md                          # This document
├── README.md                       # User documentation
├── pyproject.toml                  # Package config
├── requirements.txt                # Dependencies
├── rulesmith.py                    # CLI entry point
│
├── cli/
│   └── src/
│       ├── main.py                 # Command definitions
│       ├── commands/
│       │   ├── new.py              # NEW: New project command
│       │   ├── init.py             # Existing project command
│       │   ├── status.py
│       │   └── update.py
│       ├── config/
│       │   ├── schema.py           # Pydantic models
│       │   └── manager.py          # Config I/O
│       └── detectors/
│           └── stack_detector.py   # File-based detection
│
├── generator/
│   └── src/
│       ├── orchestrator.py         # Workflow coordinator
│       ├── llm/                    # NEW: LLM integration
│       │   ├── __init__.py
│       │   ├── client.py           # API clients
│       │   ├── prd_generator.py    # PRD generation
│       │   └── prompts/
│       │       ├── system.txt
│       │       └── prd_template.md
│       ├── parser/                 # NEW: PRD parsing
│       │   ├── __init__.py
│       │   ├── prd_parser.py       # Extract structured data
│       │   └── stack_extractor.py  # Identify tech from PRD
│       ├── interview/
│       │   ├── engine.py           # Interactive questioning
│       │   ├── questions.py        # Question definitions
│       │   ├── modes/
│       │   │   ├── new_project.py  # 15-question new project mode
│       │   │   └── existing.py     # 4-question existing mode
│       │   └── adapters.py         # CLI adapters
│       └── assembly/
│           ├── compiler.py         # Rule compilation
│           ├── resolver.py         # Dependency resolution
│           └── context.py          # Context building
│
├── formatters/
│   └── src/
│       ├── base.py                 # Base formatter class
│       ├── registry.py             # Formatter discovery
│       ├── sync.py                 # Multi-formatter sync
│       └── formatters/
│           ├── cursor.py           # .mdc generation
│           ├── claude.py           # CLAUDE.md generation
│           ├── copilot.py          # GitHub Copilot
│           ├── roo.py              # Roo Code
│           └── continue_dev.py     # Continue.dev
│
└── schemas/                        # NEW: Future extensibility
    ├── prd/                        # PRD schemas
    │   ├── v1.json
    │   └── v2.json
    └── rules/                      # Rule validation schemas
        └── rule-v1.json
```

---

## Dependencies

### Core
```
typer>=0.9.0          # CLI framework
pydantic>=2.0.0       # Data validation
pyyaml>=6.0           # YAML parsing
rich>=13.0.0          # Terminal UI
openai>=1.0.0         # OpenAI API
anthropic>=0.8.0      # Anthropic API
jinja2>=3.1.0         # Templating
pathspec>=0.11.0      # Glob patterns
```

### Development
```
pytest>=7.0.0         # Testing
black>=23.0.0         # Formatting
ruff>=0.1.0           # Linting
mypy>=1.0.0           # Type checking
```

---

## Acceptance Criteria

### Mode 1: New Project
- [ ] Accept user prompt as CLI argument
- [ ] Run 10-15 question interview (5 min max)
- [ ] Generate PRD via LLM (GPT-4 or Claude)
- [ ] Parse PRD to extract stack/domain requirements
- [ ] Select appropriate rules from `/rules` library
- [ ] Output PRD.md + AI assistant rules
- [ ] Allow regeneration with different LLM/temperature

### Mode 2: Existing Project
- [ ] Detect stack from project files (10+ techs)
- [ ] Run 3-4 quick context questions
- [ ] Select rules based on detection
- [ ] Output AI assistant rules only
- [ ] Validate output files are correct format

### Both Modes
- [ ] All tests pass (>80% coverage)
- [ ] Support Cursor, Claude, Copilot output formats
- [ ] Config persistence in `.rulesmith/config.json`
- [ ] Library update mechanism from `/rules` folder
- [ ] Documentation complete

---

## Future Enhancements (v2.1+)

### Skills System
- Specialized interviewers for specific domains
- e.g., "API design skill", "Database schema skill"

### Schema Validation
- JSON Schema for PRDs
- Validation before rule generation
- Schema evolution management

### Template Library
- Pre-built PRD templates for common project types
- Community-contributed templates

### Integration
- GitHub Actions for CI/CD rule generation
- IDE plugins (VS Code, JetBrains)
- Web UI for non-technical users

---

## Reference Files

### External Dependencies
- **Rules Library:** `/Users/dars/Development/opencode-projects/experiment/Rules/`
  - Core rules: `core/*.md`
  - Stack rules: `stacks/*.md`
  - Domain rules: `domains/*.md`
- **Library Index:** `/Users/dars/Development/opencode-projects/experiment/rulesmith-library/index.yaml`

### Previous Plans
- **Agent 1:** CLI Foundation (`../agent1-cli-foundation-PLAN.md`)
- **Agent 3:** Generator (`../agent3-generator-PLAN.md`)
- **Agent 4:** Formatters (`../agent4-formatters-PLAN.md`)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-02-03 | Major revamp - Added LLM PRD generation, dual-mode architecture |
| 1.0.0 | 2026-02-03 | Initial PRD - Focus on existing projects only |

---

## Next Steps

1. ✅ Create project structure
2. ✅ Build CLI foundation with commands
3. ✅ Implement stack detection
4. ✅ Build interview engine
5. ⏳ **Add LLM integration for PRD generation**
6. ⏳ **Add PRD parser to extract stack info**
7. ⏳ **Connect Mode 1 workflow**
8. ⏳ Wire formatters to generate actual files
9. ⏳ Add tests
10. ⏳ Create installable package
