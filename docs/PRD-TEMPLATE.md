# Super PRD Framework

A comprehensive framework for writing in-depth Product Requirements Documents.

## Document Structure

### 1. Executive Summary
- **Project Name**: Clear, descriptive name
- **One-Liner**: Elevator pitch (1 sentence)
- **Problem Statement**: What pain point does this solve?
- **Solution Overview**: High-level approach
- **Success Metrics**: How do we know it worked?

### 2. Context & Background
- **Current State**: What exists today? What's broken?
- **Market Research**: Competitors, alternatives, inspiration
- **User Research**: Who are the users? What do they need?
- **Technical Context**: Existing systems, constraints
- **Business Context**: Why build this now?

### 3. Goals & Objectives

#### Primary Goals (Must-Have)
1. Goal 1 with measurable outcome
2. Goal 2 with measurable outcome

#### Secondary Goals (Nice-to-Have)
1. Stretch goal 1
2. Stretch goal 2

#### Non-Goals (Explicitly Out of Scope)
- What we are NOT building
- Future phase items

### 4. User Personas & Stories

#### Persona 1: [Name]
- **Role**: Job title/role
- **Pain Points**: Top 3 frustrations
- **Goals**: What they want to achieve
- **Technical Skill**: Beginner/Intermediate/Advanced
- **Usage Context**: When/where/how they use it

#### User Stories
```
As a [persona],
I want to [action],
So that [benefit]
```

### 5. Functional Requirements

#### Feature 1: [Name]
**Description**: What does this feature do?

**User Flow**:
1. Step 1
2. Step 2
3. Step 3

**Acceptance Criteria**:
- [ ] Criteria 1 (given/when/then)
- [ ] Criteria 2 (given/when/then)
- [ ] Criteria 3 (given/when/then)

**API/UI Requirements**:
- Endpoints/components needed
- Input/output specifications
- Error scenarios

**Edge Cases**:
- Edge case 1: Expected behavior
- Edge case 2: Expected behavior

---

#### Feature 2: [Name]
[Same structure...]

### 6. Technical Architecture

#### System Overview
- High-level architecture diagram
- Component interaction
- Data flow

#### Component Breakdown

##### Component 1: [Name]
**Purpose**: What does this component do?

**Responsibilities**:
1. Responsibility 1
2. Responsibility 2

**Interfaces**:
- Input: What it receives
- Output: What it produces
- Events: What it emits/listens to

**Dependencies**:
- Internal dependencies
- External dependencies

**Technology Choices**:
- Language/Framework
- Libraries
- Rationale

---

##### Component 2: [Name]
[Same structure...]

#### Data Model

##### Entity 1: [Name]
```
- id: uuid (primary key)
- field1: type (constraints)
- field2: type (constraints)
- relationships
```

**Validation Rules**:
1. Rule 1
2. Rule 2

---

##### Entity 2: [Name]
[Same structure...]

#### API Specifications

##### Endpoint 1: [METHOD] /path
**Description**: What does this endpoint do?

**Request**:
```json
{
  "field1": "type (required/optional)",
  "field2": "type (required/optional)"
}
```

**Response (200)**:
```json
{
  "data": {},
  "meta": {}
}
```

**Error Responses**:
- 400: Validation error
- 401: Authentication error
- 404: Not found

**Rate Limiting**: X requests per minute

---

##### Endpoint 2: [METHOD] /path
[Same structure...]

### 7. Directory Structure

```
project-root/
├── folder1/                    # Purpose
│   ├── subfolder1/            # Purpose
│   └── file1.ext              # Purpose
├── folder2/                    # Purpose
└── file2.ext                   # Purpose
```

**File Organization Principles**:
1. Principle 1
2. Principle 2

### 8. User Interface (if applicable)

#### Wireframes/Mockups
- [Link to designs]
- Key screens description

#### Interaction Patterns
- Pattern 1: Behavior
- Pattern 2: Behavior

#### Accessibility Requirements
- WCAG compliance level
- Keyboard navigation
- Screen reader support

### 9. Non-Functional Requirements

#### Performance
- Response time targets (P50, P95, P99)
- Throughput requirements
- Resource usage limits

#### Scalability
- Expected load (users, requests, data)
- Scaling strategy
- Bottlenecks and mitigation

#### Reliability
- Uptime targets (SLA)
- Backup/recovery procedures
- Disaster recovery plan

#### Security
- Authentication method
- Authorization model
- Data encryption (at rest/in transit)
- Compliance requirements (GDPR, SOC2, etc.)

#### Monitoring
- Key metrics to track
- Alerting thresholds
- Dashboard requirements

### 10. Implementation Plan

#### Phase 1: Foundation (Weeks 1-2)
- Task 1 (estimated: X hours)
- Task 2 (estimated: X hours)
- Deliverable: [What will exist]

#### Phase 2: Core Features (Weeks 3-4)
- Task 3 (estimated: X hours)
- Task 4 (estimated: X hours)
- Deliverable: [What will exist]

#### Phase 3: Polish & Launch (Weeks 5-6)
- Task 5 (estimated: X hours)
- Task 6 (estimated: X hours)
- Deliverable: [What will exist]

#### Milestones
| Date | Milestone | Success Criteria |
|------|-----------|------------------|
| Week 1 | Skeleton build | End-to-end flow works |
| Week 3 | Core complete | All primary features work |
| Week 5 | Launch ready | All tests pass, docs complete |

### 11. Testing Strategy

#### Unit Testing
- Coverage target: 80%+
- Critical paths to test
- Mocking strategy

#### Integration Testing
- Component interaction tests
- API contract tests
- Database integration tests

#### E2E Testing
- Critical user journeys
- Browser/device matrix
- Performance tests

#### Test Data
- Fixtures/factories needed
- Production-like test scenarios

### 12. Definition of Done (DoD)

- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Unit tests written and passing (80%+ coverage)
- [ ] Integration tests passing
- [ ] Documentation complete (code + user)
- [ ] No critical/high bugs
- [ ] Performance targets met
- [ ] Security review complete (if required)
- [ ] Accessibility review complete (if UI)
- [ ] Deployed to staging and tested

### 13. Risks & Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Risk 1 | High/Med/Low | High/Med/Low | Strategy |
| Risk 2 | High/Med/Low | High/Med/Low | Strategy |

### 14. Open Questions

1. Question 1?
2. Question 2?

### 15. References

- Related PRDs
- Technical RFCs
- Design documents
- External resources

---

## Writing Guidelines

### Do
- Be specific and measurable
- Include examples and code snippets
- Define acceptance criteria clearly
- Consider edge cases
- Review with stakeholders

### Don't
- Use vague language ("fast", "user-friendly")
- Skip technical details
- Assume context is known
- Over-engineer prematurely
- Ignore non-functional requirements

## Review Checklist

Before finalizing:
- [ ] All sections complete
- [ ] Clear to implement without asking questions
- [ ] Acceptance criteria are testable
- [ ] Technical approach is sound
- [ ] Risks are identified
- [ ] Timeline is realistic
- [ ] Stakeholders have reviewed