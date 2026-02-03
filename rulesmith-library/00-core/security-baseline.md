---
description: "Security best practices for all code"
globs: "*"
alwaysApply: true
weight: 90
tags:
  - security
---

# Security Baseline

## Security Requirements

### Input Validation
- Never trust user input
- Validate at system boundaries
- Sanitize before use in queries/commands

### Secrets Management
- Never commit secrets to version control
- Use environment variables for configuration
- Rotate credentials regularly

### Authentication & Authorization
- Always check permissions before actions
- Use principle of least privilege
- Implement proper session management
