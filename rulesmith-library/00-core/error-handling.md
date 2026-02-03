---
description: "Error handling and recovery patterns"
globs: "*"
alwaysApply: true
weight: 80
tags:
  - reliability
---

# Error Handling

## Error Handling Principles

### Fail Fast, Fail Loud
- Validate preconditions early
- Throw/raise on unrecoverable errors
- Don't silently swallow exceptions

### Graceful Degradation
- Provide fallback paths where possible
- Return meaningful error messages
- Log errors with sufficient context

### Recovery Strategies
- Retry with exponential backoff for transient failures
- Circuit breaker pattern for external services
- Dead letter queues for failed background jobs
