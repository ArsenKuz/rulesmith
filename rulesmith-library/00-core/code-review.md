---
description: "Self-review checklist before submitting code"
globs: "*"
alwaysApply: false
weight: 40
---

# Code Review

## Self-Review Checklist

Before considering code complete:

- [ ] All tests pass
- [ ] No console.log/debugger statements left
- [ ] Error handling covers edge cases
- [ ] Documentation updated if needed
- [ ] Security implications considered
- [ ] Performance impact assessed
- [ ] Backward compatibility maintained (or intentional break documented)

## Quality Gates
- Code coverage doesn't decrease
- No new linting errors
- Complexity metrics within bounds
