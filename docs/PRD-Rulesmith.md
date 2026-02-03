# PRD-Rulesmith-Complete

**Status**: Draft  
**Last Updated**: 2025-02-02  
**Author**: AI Assistant  
**Stakeholders**: Development Team

---

## 1. Executive Summary

### Project Name
**Rulesmith** - AI-Powered Project Rule Generator

### One-Liner
Rulesmith automatically detects your technology stack, interviews you about project requirements, and generates tailored AI assistant rules for multiple coding tools (Cursor, Claude, Copilot, etc.).

### Problem Statement
Developers waste time repeatedly explaining project conventions, coding standards, and architecture patterns to AI coding assistants. Each tool (Cursor, Claude, Copilot) uses different formats and locations for custom instructions. There's no standardized way to:
1. Auto-detect technology stacks
2. Interview developers about project specifics
3. Generate consistent rules across multiple AI tools
4. Maintain rules as projects evolve

### Solution Overview
A CLI tool that:
1. **Detects** technology stack from project files (package.json, requirements.txt, etc.)
2. **Interviews** developers (quick 5-question or guided 20-question modes)
3. **Compiles** rules from a modular library (core, domain, stack-specific)
4. **Formats** output for 5+ AI tools simultaneously
5. **Syncs** all tools to ensure consistency

### Success Metrics
- Setup time reduced from 2+ hours to <5 minutes
- Rule consistency across tools: 100%
- Auto-detection accuracy: >90%
- Developer satisfaction (would use again): >80%

---

## 2. Context & Background

### Current State
Existing solutions are fragmented:
- **Cursor**: Manual `.cursor/rules/*.mdc` file creation
- **Claude**: Manual `CLAUDE.md` file creation
- **Copilot**: Manual `.github/copilot-instructions.md`
- **No detection**: Developers manually specify stack
- **No standardization**: Each project reinvents conventions
- **No sync**: Rules diverge across tools

### Market Research

**Competitors/Alternatives:**
1. **Manual documentation** - Time-consuming, inconsistent
2. **Template repos** - Generic, not project-specific
3. **AI tool defaults** - Generic, don't know your project
4. **gitingest** - Creates context but not rules

**Inspiration:**
- Django's startproject (but for AI rules)
- eslint --init (interactive setup)
- Yeoman generators (but for rules)

### User Research

#### Primary Persona: Senior Developer (Alex)
- **Role**: Senior Full-Stack Developer
- **Pain Points**: 
  - Spends 30+ minutes explaining project structure to each new AI tool
  - Rules become outdated as project evolves
  - Different rules for Cursor vs Claude cause confusion
- **Goals**: One command to setup all AI tools, consistent experience
- **Technical Skill**: Advanced
- **Usage Context**: New projects, onboarding team members, switching AI tools

#### Secondary Persona: Tech Lead (Maria)
- **Role**: Engineering Manager
- **Pain Points**:
  - Team uses different AI tools
  - No standardization across projects
  - Hard to enforce coding standards via AI
- **Goals**: Standardize team AI assistant behavior, enforce best practices
- **Technical Skill**: Advanced
- **Usage Context**: Team-wide rollouts, project templates

### Technical Context

**Existing Components:**
- CLI framework: Typer + Rich for interactive prompts
- Detection engine: File-based stack detection (package.json scanning)
- Rule library: Modular markdown files with YAML frontmatter
- Formatters: Tool-specific output generators

**Constraints:**
- Must support 10+ technology stacks
- Must work offline (no cloud dependency)
- Must be extensible (easy to add new tools/stacks)
- Must be language-agnostic (works with any project)

### Business Context
**Why build this now:**
- AI coding assistants are becoming standard (Cursor, Claude, Copilot, etc.)
- No existing solution addresses multi-tool consistency
- Growing team needs standardized AI interactions
- Manual setup is error-prone and time-consuming

---

## 3. Goals & Objectives

### Primary Goals (Must-Have for MVP)

1. **Auto-Detection Accuracy >90%**
   - Detect stack from project files
   - Support 10+ major stacks (Next.js, Django, FastAPI, etc.)
   - Confidence score for detection

2. **Quick Mode <2 Minutes**
   - 5-question interview flow
   - Generate basic rules for detected stack
   - Support override if detection wrong

3. **Multi-Tool Output**
   - Generate Cursor (.mdc files)
   - Generate Claude (CLAUDE.md)
   - Generate Copilot (copilot-instructions.md)
   - Format rules correctly for each tool

4. **Modular Rule Library**
   - Core rules (apply to all projects)
   - Domain rules (frontend, backend patterns)
   - Stack rules (Next.js, FastAPI specific)
   - Include/exclude based on interview answers

### Secondary Goals (Nice-to-Have)

1. **Guided Mode**
   - 20-question comprehensive interview
   - Detailed requirements document generation
   - Fine-grained control over rule selection

2. **Additional Tools**
   - Roo Code support
   - Continue.dev support
   - Custom tool templates

3. **Update/Refresh**
   - Detect project changes
   - Update rules incrementally
   - Version control integration

4. **Team Sharing**
   - Share rule configurations
   - Team-wide standards
   - Template repositories

### Non-Goals (Out of Scope for MVP)

- Cloud-based rule hosting
- Real-time rule updates
- AI-powered rule generation from codebase analysis
- IDE plugins (VS Code, JetBrains)
- Web UI for configuration
- Rule marketplace/sharing platform
- Automatic rule learning from commits

---

## 4. User Personas & Stories

### Primary Persona: Senior Developer (Alex)

**Demographics:**
- 5+ years experience
- Uses Cursor daily, occasionally Claude
- Works on multiple projects (3-5 at a time)
- Values automation and consistency

**Pain Points:**
1. "I spend 20 minutes setting up Cursor rules for each new project"
2. "My Claude instructions are different from my Cursor rules - confusing"
3. "I forget to update rules when we add new technologies"
4. "Junior devs ask me the same questions AI should know"

**Goals:**
1. One command to setup all AI tools
2. Consistent experience across tools
3. Minimal maintenance
4. Accurate, project-specific guidance

**Technical Context:**
- Comfortable with CLI tools
- Knows project structure well
- Can override auto-detection if needed

### Secondary Persona: Tech Lead (Maria)

**Demographics:**
- 8+ years experience
- Manages team of 6 developers
- Standardizes tools and processes
- Reviews AI-generated code

**Pain Points:**
1. "Team uses Cursor, Claude, and Copilot - no consistency"
2. "Hard to enforce coding standards via AI"
3. "Onboarding new devs takes forever"
4. "No visibility into what AI knows about our projects"

**Goals:**
1. Standardize team AI assistant behavior
2. Enforce best practices automatically
3. Reduce onboarding time
4. Audit AI recommendations

---

### User Stories

#### Story 1: Quick Setup
```
As Alex (senior developer),
I want to run a single command to setup AI rules,
So that I can start coding with context-aware AI assistance in under 5 minutes.

Acceptance Criteria:
- Command: rulesmith init
- Auto-detects my stack (Next.js, FastAPI, etc.)
- Asks 5 quick questions about my project
- Generates rules for Cursor, Claude, and Copilot
- All files created in correct locations
```

#### Story 2: Override Detection
```
As Alex,
I want to correct the auto-detected stack if it's wrong,
So that the rules match my actual technology stack.

Acceptance Criteria:
- Shows detected stack with confidence score
- Option to select different stack from list
- Manual stack selection used for rule generation
- Detection saved for future runs
```

#### Story 3: Multi-Tool Consistency
```
As Maria (tech lead),
I want the same coding standards applied across all AI tools my team uses,
So that we have consistent code quality regardless of which tool a developer chooses.

Acceptance Criteria:
- Rules generated for Cursor (.mdc files)
- Rules generated for Claude (CLAUDE.md)
- Rules generated for Copilot (copilot-instructions.md)
- Core principles consistent across all outputs
- Tool-specific formatting respected
```

#### Story 4: Project-Specific Rules
```
As Alex,
I want rules that understand my project's specific patterns,
So that AI suggestions match our conventions, not generic best practices.

Acceptance Criteria:
- Interview asks about our architecture patterns
- Rules reference our specific stack (e.g., FastAPI, not just Python)
- Includes our testing approach
- Respects our team's preferences (e.g., "ask before major refactors")
```

#### Story 5: Guided Mode for Complex Projects
```
As Maria,
I want a detailed interview for complex projects,
So that we can capture nuanced requirements and constraints.

Acceptance Criteria:
- Option for 20-question guided mode
- Covers architecture, testing, security, performance
- Generates detailed requirements document
- More granular rule selection
```

---

## 5. Functional Requirements

### Feature 1: Stack Detection Engine

**Description:**
Automatically detect technology stack by analyzing project files.

**User Flow:**
1. Developer runs `rulesmith init`
2. System scans project directory
3. Detects signals: package.json, requirements.txt, Cargo.toml, etc.
4. Matches signals to known stacks
5. Returns detected stack with confidence score

**Acceptance Criteria:**
- [x] Scan for package.json (Node.js stacks)
- [x] Scan for requirements.txt, pyproject.toml (Python)
- [x] Scan for Cargo.toml (Rust)
- [x] Scan for go.mod (Go)
- [x] Scan for Gemfile (Ruby)
- [x] Scan for composer.json (PHP)
- [x] Scan for pubspec.yaml (Flutter)
- [x] Return StackResult with primary stack and confidence
- [x] Support 10+ major stacks with accuracy >90%

**Detection Logic:**
```
Next.js: package.json contains "next" in dependencies
FastAPI: requirements.txt contains "fastapi"
Django: requirements.txt contains "django"
React SPA: package.json contains "react" but not "next"
```

**Edge Cases:**
- Monorepo with multiple stacks: Detect primary or ask user
- No recognizable files: Report "unknown" with 0% confidence
- Ambiguous signals (multiple frameworks): Show top 3 options

---

### Feature 2: Interview Engine

**Description:**
Interactive interview system to gather project requirements.

**User Flow:**
1. Confirm or override detected stack
2. Answer 5 questions (quick mode) or 20 questions (guided mode)
3. Questions adapt based on previous answers
4. Results stored for rule compilation

**Acceptance Criteria:**
- [x] Support multiple question types: text, choice, multiple_choice, confirm, path
- [x] Rich CLI interface with formatting
- [x] Skip questions based on conditions (e.g., skip "state_management" if backend-only)
- [x] Validate required questions
- [x] Store answers in structured format
- [x] Support quick mode (5 questions, <2 min)
- [x] Support guided mode (20 questions, comprehensive)

**Quick Mode Questions:**
1. Confirm detected stack (confirm)
2. Project purpose (choice: SaaS, E-commerce, API, etc.)
3. Team size (choice: Solo, Small, Medium, Large)
4. Priority constraint (choice: Performance, Security, DX, etc.)
5. AI tools used (multiple_choice: Cursor, Claude, Copilot, etc.)

**Question Format:**
```yaml
id: "confirm_stack"
type: "confirm"
text: "Detected: {detected_stack}. Is this correct?"
default: true
```

**Edge Cases:**
- User skips required question: Re-ask with validation message
- Invalid input type: Show error and re-prompt
- Interview interrupted: Support resume (future feature)

---

### Feature 3: Rule Compilation Engine

**Description:**
Compile rules from library based on stack and interview answers.

**User Flow:**
1. Load library index.yaml
2. Select core rules (alwaysApply: true)
3. Select stack-specific rules based on detected stack
4. Select domain rules based on interview answers
5. Resolve dependencies (includes field)
6. Sort by weight
7. Personalize with interview answers (template substitution)

**Acceptance Criteria:**
- [x] Load rules from YAML frontmatter + Markdown
- [x] Always include core rules (communication, security, error-handling)
- [x] Include stack rules for detected stack
- [x] Include domain rules based on answers (e.g., testing-unit if TDD)
- [x] Resolve includes recursively
- [x] Sort by weight (highest first)
- [x] Personalize rule content with {{template}} substitution
- [x] Return list of CompiledRule objects

**Rule Selection Logic:**
```
If testing_approach == "TDD":
  Select testing-unit, testing-integration
  
If performance_critical == true:
  Select performance-optimization
  
If security_compliance != "None":
  Select security-compliance
```

**Edge Cases:**
- Rule file missing: Skip gracefully, log warning
- Circular includes: Detect and break cycle
- Missing template variable: Leave placeholder as-is

---

### Feature 4: Multi-Tool Formatters

**Description:**
Format compiled rules for different AI tools.

**User Flow:**
1. Receive compiled rules and project context
2. For each target tool:
   a. Format according to tool specification
   b. Write to correct location
   c. Validate output
3. Report success/failure for each tool

**Acceptance Criteria:**
- [x] Cursor formatter: Generate .cursor/rules/*.mdc files
  - YAML frontmatter: description, globs, alwaysApply
  - Filename prefix by weight (00-core-, 10-high-, 20-medium-)
  - Project summary file
- [x] Claude formatter: Generate CLAUDE.md
  - Single comprehensive file
  - Sections: Overview, Core Principles, Stack Guidelines, Domain Patterns
  - No YAML frontmatter
- [x] Copilot formatter: Generate .github/copilot-instructions.md
  - Markdown format
  - Sections: Context, Standards, Guidelines
- [x] Roo formatter: Generate .roo/rules/*.md (future)
- [x] ContinueDev formatter: Generate .continuerules (future)
- [x] Validate all outputs (check file exists, format correct)

**Cursor Output Format:**
```markdown
---
description: Security best practices
globs: "**/*"
alwaysApply: true
---

# Security Baseline

Content here...
```

**Edge Cases:**
- Output directory doesn't exist: Create it
- File already exists: Update in place, report as "updated"
- Permission denied: Report error, don't crash
- Invalid rule format: Skip rule, log error

---

### Feature 5: Sync Engine

**Description:**
Coordinate all formatters and sync them together.

**User Flow:**
1. Developer specifies target tools (or use defaults)
2. SyncEngine initializes formatters
3. Runs each formatter
4. Collects results
5. Validates outputs
6. Reports summary

**Acceptance Criteria:**
- [x] Support multiple target tools in one call
- [x] Run formatters in sequence (or parallel)
- [x] Collect detailed results (files created, updated, errors)
- [x] Validate all outputs
- [x] Return structured results per tool

**API:**
```python
sync = SyncEngine(
    compiled_rules=rules,
    project_context=context,
    project_root=Path("./my-project"),
    target_tools=["cursor", "claude", "copilot"]
)

results = sync.sync_all()
# {
#   "cursor": {"success": True, "files_created": [...]},
#   "claude": {"success": True, "files_created": [...]},
# }
```

**Edge Cases:**
- One formatter fails: Continue with others, report error
- All formatters fail: Return failure status
- Unknown tool ID: Raise ValueError with helpful message

---

### Feature 6: Rule Library Management

**Description:**
Organized, modular rule library with clear structure.

**Structure:**
```
Rules/
├── core/           # Universal rules (alwaysApply)
│   ├── communication.md
│   ├── security-baseline.md
│   ├── error-handling.md
│   ├── documentation.md
│   ├── code-review.md
│   ├── prd-driven-development.md
│   ├── code-organization.md
│   └── formatting-standards.md
├── domains/        # Domain-specific
│   ├── web-frontend.md
│   └── web-backend.md
├── stacks/         # Technology-specific
│   ├── nextjs.md
│   └── fastapi-python.md
├── frameworks/     # Framework patterns
│   └── pipeline-architecture.md
├── testing/        # Testing rules
│   ├── testing-standards.md
│   └── testing-day1.md
└── performance/    # Performance rules
    └── performance-optimization.md
```

**Acceptance Criteria:**
- [x] Each rule has YAML frontmatter
- [x] Core rules marked alwaysApply: true
- [x] Stack rules use includes for dependencies
- [x] Weight-based prioritization (100 = highest)
- [x] Clear, actionable content
- [x] Examples where applicable

**Rule Format:**
```markdown
---
description: Brief description
globs: "**/*"
alwaysApply: true/false
weight: 1-100
includes:
  - other-rule-id
---

# Title

Content in Markdown...
```

---

## 6. Technical Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Rulesmith CLI                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │   CLI Layer  │   │   Generator  │   │  Formatters  │    │
│  │   (Typer)    │──▶│  (Orchestrator)│──▶│   (Sync)     │    │
│  └──────────────┘   └──────────────┘   └──────────────┘    │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │Stack Detector│   │Interview Eng │   │ Cursor       │    │
│  │              │   │  Quick/Guided│   │ Claude       │    │
│  └──────────────┘   └──────────────┘   │ Copilot      │    │
│                                        │ Roo          │    │
│                                        │ Continue     │    │
│                                        └──────────────┘    │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │              Rules Library (YAML+MD)                    ││
│  │  core/ • domains/ • stacks/ • testing/ • performance/   ││
│  └────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Component 1: CLI Layer

**Purpose:**
Command-line interface for user interaction.

**Responsibilities:**
1. Parse command-line arguments
2. Invoke appropriate commands (init, update, status)
3. Display progress and results
4. Handle errors gracefully

**Interfaces:**
- Input: CLI arguments, interactive prompts
- Output: Console output (Rich formatting), files on disk
- Events: None

**Dependencies:**
- StackDetector
- GeneratorOrchestrator
- ConfigManager

**Technology:**
- Typer: CLI framework
- Rich: Terminal formatting and prompts

---

#### Component 2: Stack Detector

**Purpose:**
Detect technology stack from project files.

**Responsibilities:**
1. Scan project directory for signal files
2. Parse configuration files (package.json, etc.)
3. Match signals to known stacks
4. Return detection result with confidence

**Interfaces:**
- Input: Path (project directory)
- Output: StackResult (primary, confidence, all_signals)
- Events: None

**Dependencies:**
- File system access
- JSON/TOML/YAML parsers

**Technology:**
- Standard library: json, tomllib
- PyYAML for YAML parsing

**Detection Algorithm:**
```python
def detect(project_path: Path) -> StackResult:
    signals = scan_for_files(project_path)
    scores = {}
    
    if "next" in signals.package_json.dependencies:
        scores["nextjs-fullstack"] = 100
    elif "fastapi" in signals.requirements:
        scores["fastapi-python"] = 90
    # ... more patterns
    
    primary = max(scores, key=scores.get)
    confidence = scores[primary] / 100
    
    return StackResult(primary, confidence, signals)
```

---

#### Component 3: Interview Engine

**Purpose:**
Conduct interactive interviews with users.

**Responsibilities:**
1. Display questions with Rich formatting
2. Collect and validate answers
3. Support conditional question skipping
4. Maintain interview state

**Interfaces:**
- Input: List[Question], Console
- Output: Dict[str, Any] (answers)
- Events: Question displayed, answer recorded

**Dependencies:**
- Rich (Console, Prompt, Panel)
- Question definitions

**Technology:**
- Rich for interactive CLI
- Pydantic for question models

**Question Types:**
- TEXT: Free text input
- CHOICE: Single selection from list
- MULTIPLE_CHOICE: Multiple selections
- CONFIRM: Yes/No
- PATH: File path with validation

---

#### Component 4: Rule Compiler

**Purpose:**
Compile rules from library based on context.

**Responsibilities:**
1. Load library index
2. Select rules by criteria (alwaysApply, stack, domain)
3. Resolve dependencies (includes)
4. Personalize content with template substitution
5. Sort by weight

**Interfaces:**
- Input: library_path, selected_stack, interview_answers
- Output: List[CompiledRule]
- Events: None

**Dependencies:**
- YAML parser
- File system access
- Regex for template substitution

**Technology:**
- PyYAML for frontmatter parsing
- Standard library: re, pathlib

**Algorithm:**
```python
def compile(stack, answers):
    index = load_index()
    
    # Select rules
    core = [r for r in index.core if r.alwaysApply]
    stack_rules = get_stack_rules(index, stack)
    domain = select_domain_rules(index, answers)
    
    # Resolve dependencies
    all_rules = resolve_includes(core + stack_rules + domain)
    
    # Load and personalize
    compiled = []
    for rule_id in all_rules:
        rule = load_rule(rule_id)
        personalized = substitute_templates(rule, answers)
        compiled.append(personalized)
    
    # Sort by weight
    return sorted(compiled, key=lambda r: r.weight, reverse=True)
```

---

#### Component 5: Formatters

**Purpose:**
Format rules for specific AI tools.

**Responsibilities:**
1. Convert CompiledRule to tool-specific format
2. Write to correct file locations
3. Validate output
4. Report file operations

**Interfaces:**
- Input: List[CompiledRule], project_context, output_dir
- Output: FormatterResult (files created/updated/errors)
- Events: File written, validation passed/failed

**Dependencies:**
- File system access
- Tool-specific formatting logic

**Technology:**
- Jinja2 for templates (if needed)
- PyYAML for Cursor frontmatter

**Formatter Implementations:**

**CursorFormatter:**
```python
def format_rules(rules, context, output_dir):
    output_path = output_dir / ".cursor" / "rules"
    
    for rule in sorted_rules:
        filename = generate_filename(rule)  # 00-core-xxx.mdc
        content = format_single_rule(rule)  # YAML frontmatter + MD
        write_file(output_path / filename, content)
```

**ClaudeFormatter:**
```python
def format_rules(rules, context, output_dir):
    output_path = output_dir / "CLAUDE.md"
    content = generate_single_file(rules, context)
    write_file(output_path, content)
```

---

#### Component 6: Sync Engine

**Purpose:**
Coordinate all formatters.

**Responsibilities:**
1. Initialize formatters for target tools
2. Run each formatter
3. Collect and report results
4. Validate all outputs

**Interfaces:**
- Input: compiled_rules, project_context, target_tools
- Output: Dict[str, dict] (results per tool)
- Events: Formatter started, completed, failed

**Dependencies:**
- Formatter registry
- All formatter implementations

**Technology:**
- Python standard library

---

### Data Model

#### Entity 1: ProjectConfig
```python
class ProjectConfig:
    project_name: str
    project_root: Path
    detected_stack: str
    stack_confidence: float
    detected_signals: Dict[str, Any]
    generation_mode: str  # "quick" or "guided"
    selected_stack: Optional[str]
    created_at: datetime
    updated_at: datetime
    library_updated_at: Optional[datetime]
```

#### Entity 2: CompiledRule
```python
class CompiledRule:
    id: str
    description: str
    globs: str = "**/*"
    alwaysApply: bool = False
    weight: int = 50
    content: str  # Markdown body
    frontmatter: Dict[str, Any]
    category: Optional[str]  # "core", "stack", "domain"
```

#### Entity 3: Question
```python
class Question:
    id: str
    type: QuestionType  # TEXT, CHOICE, MULTIPLE_CHOICE, CONFIRM, PATH
    text: str
    description: Optional[str]
    options: Optional[List[str]]
    default: Optional[Any]
    required: bool = True
    skip_if: Optional[str]  # Condition for skipping
```

#### Entity 4: StackResult
```python
class StackResult:
    primary: str  # Detected stack ID
    confidence: float  # 0.0 to 1.0
    all_signals: Dict[str, Any]  # Raw detection data
```

---

### API Specifications

None - this is a CLI tool, not a service. However, internal module APIs:

#### StackDetector.detect()
```python
def detect(project_path: Path) -> StackResult:
    """
    Detect technology stack from project files.
    
    Args:
        project_path: Path to project root directory
        
    Returns:
        StackResult with primary stack and confidence
        
    Raises:
        FileNotFoundError: If project_path doesn't exist
    """
```

#### GeneratorOrchestrator.run()
```python
def run() -> Dict[str, Any]:
    """
    Execute full generation workflow.
    
    Returns:
        Dict containing:
        - interview_answers: Dict[str, Any]
        - selected_stack: str
        - compiled_rules: List[CompiledRule]
        - requirements_document: str
    """
```

#### SyncEngine.sync_all()
```python
def sync_all() -> Dict[str, dict]:
    """
    Generate rules for all target tools.
    
    Returns:
        Dict mapping tool_id to result dict:
        {
            "cursor": {
                "success": bool,
                "files_created": List[str],
                "files_updated": List[str],
                "errors": List[str]
            }
        }
    """
```

---

## 7. Directory Structure

### Project Layout

```
rulesmith/                      # Main project directory
├── cli/                        # Agent 1: CLI interface
│   ├── src/
│   │   ├── commands/          # CLI commands
│   │   │   ├── init.py        # Initialize project
│   │   │   ├── update.py      # Update rules
│   │   │   └── status.py      # Check status
│   │   ├── detectors/         # Stack detection
│   │   │   └── stack_detector.py
│   │   ├── config/            # Configuration management
│   │   │   ├── manager.py
│   │   │   └── schema.py
│   │   ├── utils/             # Utilities
│   │   └── main.py            # CLI entry point
│   ├── requirements.txt
│   └── setup.py
├── generator/                  # Agent 3: Rule generation
│   ├── src/
│   │   ├── modes/             # Interview modes
│   │   │   ├── quick.py       # 5-question mode
│   │   │   └── guided.py      # 20-question mode
│   │   ├── interview/         # Interview engine
│   │   │   ├── engine.py
│   │   │   └── questions.py
│   │   ├── assembly/          # Rule compilation
│   │   │   └── compiler.py
│   │   ├── requirements/      # PRD generation
│   │   │   └── generator.py
│   │   ├── models/            # Data models
│   │   │   ├── interview.py
│   │   │   ├── assembly.py
│   │   │   └── requirements.py
│   │   └── orchestrator.py    # Main orchestrator
│   └── requirements.txt
├── formatters/                 # Agent 4: Multi-tool output
│   ├── src/
│   │   ├── formatters/        # Tool formatters
│   │   │   ├── cursor.py      # .cursor/rules/*.mdc
│   │   │   ├── claude.py      # CLAUDE.md
│   │   │   ├── copilot.py     # copilot-instructions.md
│   │   │   ├── roo.py         # .roo/rules/
│   │   │   └── continue_dev.py # .continuerules
│   │   ├── base.py            # Base formatter interface
│   │   ├── registry.py        # Formatter registry
│   │   └── sync.py            # Sync engine
│   └── requirements.txt
├── Rules/                      # Standard rule library
│   ├── core/                  # Universal rules (alwaysApply)
│   │   ├── communication.md
│   │   ├── security-baseline.md
│   │   ├── error-handling.md
│   │   ├── documentation.md
│   │   ├── code-review.md
│   │   ├── prd-driven-development.md
│   │   ├── code-organization.md
│   │   └── formatting-standards.md
│   ├── domains/               # Domain-specific
│   │   ├── web-frontend.md
│   │   └── web-backend.md
│   ├── stacks/                # Technology-specific
│   │   ├── nextjs.md
│   │   └── fastapi-python.md
│   ├── frameworks/            # Framework patterns
│   │   └── pipeline-architecture.md
│   ├── testing/               # Testing rules
│   │   ├── testing-standards.md
│   │   └── testing-day1.md
│   ├── performance/           # Performance rules
│   │   └── performance-optimization.md
│   └── README.md              # Library documentation
├── rulesmith-library/          # Legacy/backup library
│   ├── index.yaml             # Rule index (example)
│   └── validate.py            # Validation script
├── docs/                       # Project documentation
│   ├── PRD-TEMPLATE.md        # PRD template
│   └── PRD-Rulesmith.md       # This document
└── README.md                   # Project README
```

### File Organization Principles

1. **Agent Separation**: Each major component (CLI, Generator, Formatters) is self-contained
2. **Modular Rules**: Rules organized by category (core, domains, stacks, etc.)
3. **Clear Interfaces**: Each module exports clean API
4. **Test Parity**: Tests mirror source structure
5. **Configuration Centralized**: Config schemas in one place

---

## 8. Non-Functional Requirements

### Performance

**Detection Speed:**
- Target: <1 second for stack detection
- Scan only necessary files (stop after match found)
- Cache detection results

**Interview Speed:**
- Quick mode: <2 minutes total
- Guided mode: <10 minutes total
- Instant question transitions

**Rule Compilation:**
- Target: <3 seconds to compile 50 rules
- Lazy load rule files
- Optimize dependency resolution

**Formatting Speed:**
- Target: <2 seconds per tool
- Parallel formatting for multiple tools

### Scalability

**Rule Library:**
- Support 100+ rules without performance degradation
- Support 20+ technology stacks
- Modular loading (only load needed rules)

**Project Size:**
- Handle monorepos with 10+ packages
- Handle projects with 1000+ files (detection)

### Reliability

**Error Handling:**
- Graceful degradation (one formatter fails, others continue)
- Clear error messages
- Recovery suggestions

**Data Integrity:**
- Validate all rule files on load
- Check for circular dependencies
- Verify output format compliance

### Security

**Input Validation:**
- Validate all file paths (prevent path traversal)
- Sanitize user input in interviews
- Validate YAML frontmatter

**Output Safety:**
- Never overwrite without confirmation (unless --force)
- Atomic file writes (write temp, then rename)
- Backup existing files before update

### Monitoring

**Metrics to Track:**
- Detection accuracy by stack
- Interview completion rate
- Formatter success rate by tool
- Time to generate rules
- Error rates

---

## 9. Implementation Plan

### Phase 1: Foundation (Week 1)

**Sprint Goal:** Basic CLI that detects stack and generates rules for one tool

**Tasks:**
- [x] Day 1: CLI structure with Typer (2 hours)
  - Project setup, command structure
- [x] Day 1: Stack detection for 5 major stacks (4 hours)
  - Next.js, FastAPI, Django, React, Python
- [x] Day 2: Interview engine foundation (4 hours)
  - Question types, Rich integration
- [x] Day 2: Quick mode questions (2 hours)
  - 5 questions defined
- [x] Day 3: Rule compiler basics (4 hours)
  - Load rules, select by stack
- [x] Day 3: Cursor formatter (4 hours)
  - Generate .mdc files
- [x] Day 4-5: Integration and testing (8 hours)
  - End-to-end flow
  - Basic error handling

**Deliverable:**
- `rulesmith init` works for 5 stacks
- Generates Cursor rules
- Basic tests pass

### Phase 2: Core Features (Week 2)

**Sprint Goal:** Full multi-tool support and comprehensive rule library

**Tasks:**
- [x] Day 1: Expand stack detection (4 hours)
  - Add 5 more stacks (Rust, Go, Vue, Laravel, etc.)
- [x] Day 1: Claude formatter (4 hours)
  - Generate CLAUDE.md
- [x] Day 2: Copilot formatter (4 hours)
  - Generate copilot-instructions.md
- [x] Day 2: Sync engine (4 hours)
  - Coordinate multiple formatters
- [x] Day 3-4: Expand rule library (12 hours)
  - Core rules (8 files)
  - Domain rules (2 files)
  - Stack rules (2 files)
- [x] Day 5: Guided mode (4 hours)
  - 20-question interview
  - Requirements doc generation

**Deliverable:**
- Supports 10+ stacks
- Generates 3+ tool formats
- 17 rule files
- Quick and guided modes

### Phase 3: Polish & Integration (Week 3)

**Sprint Goal:** Production-ready with full documentation

**Tasks:**
- [ ] Day 1-2: Testing (8 hours)
  - Unit tests (80%+ coverage)
  - Integration tests
  - E2E tests with sample projects
- [ ] Day 3: Error handling & edge cases (4 hours)
  - Graceful failures
  - Validation
  - User-friendly errors
- [ ] Day 4: Documentation (4 hours)
  - README
  - Usage guide
  - Rule library docs
- [ ] Day 5: Packaging & distribution (4 hours)
  - PyPI package
  - Installation instructions
  - CI/CD pipeline

**Deliverable:**
- All tests passing
- Documentation complete
- Published to PyPI
- Production ready

### Milestones

| Date | Milestone | Success Criteria |
|------|-----------|------------------|
| Week 1 Fri | Skeleton Build | `rulesmith init` works end-to-end for 5 stacks, generates Cursor rules |
| Week 2 Fri | Core Complete | 10+ stacks, 3+ tools, 17 rules, both interview modes |
| Week 3 Fri | Launch Ready | 80%+ test coverage, docs complete, published to PyPI |

---

## 10. Testing Strategy

### Unit Testing

**Coverage Targets:**
- StackDetector: 90%+
- InterviewEngine: 85%+
- RuleCompiler: 90%+
- Formatters: 80%+

**Critical Paths:**
- Detection scoring algorithm
- Question skip logic
- Rule dependency resolution
- Template substitution
- File naming conventions

### Integration Testing

**Test Scenarios:**
1. End-to-end flow for each major stack
2. Multi-tool generation
3. Rule library loading
4. Configuration save/load

**Test Projects:**
- Next.js project
- FastAPI project
- Django project
- React SPA

### E2E Testing

**Critical User Journeys:**
1. Quick mode setup
2. Guided mode setup
3. Override detected stack
4. Update existing rules

**Test Matrix:**
- Python 3.10, 3.11, 3.12
- macOS, Linux, Windows (if possible)
- 5 different project types

### Test Data

**Fixtures:**
- Sample package.json files for each stack
- Sample requirements.txt files
- Complete interview answer sets
- Expected rule outputs

---

## 11. Definition of Done (DoD)

- [ ] All acceptance criteria from Section 5 met
- [ ] Code reviewed and approved
- [ ] Unit test coverage 80%+
- [ ] Integration tests passing
- [ ] E2E tests passing for 5+ stacks
- [ ] Documentation complete (README, usage guide, rule docs)
- [ ] No critical or high-priority bugs
- [ ] Performance targets met (detection <1s, compilation <3s)
- [ ] Security review complete (path validation, input sanitization)
- [ ] Published to PyPI
- [ ] Installation tested on clean environment
- [ ] Backward compatibility considered (N/A for v1)

---

## 12. Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AI tools change format | High | High | Design formatters to be easily updateable; monitor tool changelogs |
| Detection accuracy <90% | Medium | High | Allow manual override; improve detection algorithm; provide feedback loop |
| Rule library becomes unwieldy | Medium | Medium | Organize by category; lazy loading; community contributions |
| Performance with 100+ rules | Low | Medium | Benchmark and optimize; consider caching; lazy loading |
| Dependencies conflict | Low | High | Pin dependency versions; use lockfiles; test in isolation |
| Users don't understand interview | Medium | Medium | Provide examples; add help text; allow skipping/review |

---

## 13. Open Questions

1. Should we support custom rule repositories (remote URLs)?
2. How should we handle versioning of rules (updates)?
3. Should we support plugin architecture for custom formatters?
4. How do we handle private/sensitive rules (not in public library)?
5. Should we integrate with CI/CD to auto-update rules?
6. How do we handle rule conflicts between different sources?

---

## 14. References

### Related PRDs
- N/A (this is the foundational PRD)

### Technical RFCs
- N/A

### Design Documents
- Cursor Rule Format: https://cursor.com/rules
- Claude Code: https://docs.anthropic.com/claude-code

### External Resources
- Typer documentation: https://typer.tiangolo.com
- Rich documentation: https://rich.readthedocs.io
- Pydantic documentation: https://docs.pydantic.dev

---

## Appendix A: Current Implementation Status

### ✅ Completed (Week 1-2)

**CLI:**
- [x] Project structure
- [x] Stack detector (10+ stacks)
- [x] Config manager
- [x] Init command

**Generator:**
- [x] Interview engine
- [x] Quick mode
- [x] Guided mode
- [x] Rule compiler
- [x] Requirements generator
- [x] Orchestrator

**Formatters:**
- [x] Base formatter interface
- [x] Cursor formatter
- [x] Claude formatter
- [x] Copilot formatter
- [x] Roo formatter (basic)
- [x] ContinueDev formatter (basic)
- [x] Sync engine

**Rules:**
- [x] 8 core rules
- [x] 2 domain rules
- [x] 2 stack rules
- [x] 1 framework rule
- [x] 2 testing rules
- [x] 1 performance rule

### 🚧 In Progress

- Testing (partial)
- Documentation (partial)

### ⏳ Not Started

- PyPI packaging
- CI/CD pipeline
- Update command
- Additional formatters (Windsurf, etc.)

---

**End of PRD**