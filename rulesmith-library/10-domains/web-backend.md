---
description: "Backend API development patterns"
globs: "**/api/**/*.{ts,js,py,go,rs}"
alwaysApply: false
weight: 70
tags:
  - backend
  - api
  - server
---

# Web Backend

## API Design Principles

### RESTful Standards
- Use proper HTTP methods
- Consistent URL patterns
- Proper status codes

### Request/Response
- Validate input with schemas
- Consistent error response format
- Pagination for list endpoints

### Security
- Rate limiting
- Input sanitization
- Authentication on all routes except public
