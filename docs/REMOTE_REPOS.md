# Remote Repositories

Rulesmith now uses separate repositories for rules and skills, enabling independent versioning and community contributions.

## Rules Repository

**URL:** https://github.com/ArsenKuz/rulesmith-rules

Contains AI assistant rules organized by category:
- `00-core/` - Universal rules (communication, documentation, security, etc.)
- `10-domains/` - Domain-specific (web-frontend, web-backend)
- `20-stacks/` - Complete technology stacks
- `30-frameworks/` - Framework deep-dives
- `40-patterns/` - Cross-cutting patterns

## Skills Repository

**URL:** https://github.com/ArsenKuz/rulesmith-skills

Contains 18 curated skills:
- **Creative:** algorithmic-art, slack-gif-creator
- **Design:** brand-guidelines, canvas-design, theme-factory
- **Research:** deep-research
- **Writing:** doc-coauthoring
- **Documents:** docx, pdf, pptx, xlsx
- **Development:** frontend-design, mcp-builder, web-artifacts-builder
- **Communication:** internal-comms
- **Testing:** webapp-testing
- **Meta:** skill-creator

## Library Configuration

Rules and skills are downloaded to:
- Rules: `~/.rulesmith/libraries/rules/`
- Skills: `~/.rulesmith/libraries/skills/`

## Updating Libraries

```bash
# Update both rules and skills
rulesmith library update

# Update only rules
rulesmith library update --rules

# Update only skills
rulesmith library update --skills
```
