# Claude Code Orchestrator Configuration

> This file configures Claude Code behavior, modes, and subagent registry
> for Python API development at Kyte.

## Operating Modes

### 1. Vibe Coding (Default)
Direct implementation mode. Claude writes code, tests, and iterates.
- Always follow TDD: write test first, then implementation
- Run pytest after every change
- Run ruff check before considering a task done

### 2. Orchestrator
For complex, multi-file tasks. Claude delegates to specialized subagents.
- Break the task into subtasks
- Assign each subtask to the appropriate subagent
- Collect results and integrate

### 3. Training
For onboarding new developers. Claude explains patterns and decisions.
- Reference skills documentation
- Provide examples from the codebase
- Explain why not just how

## Mandatory Rules

1. **TDD Always**: Never write implementation without a failing test first
2. **Async Everything**: All handlers, services, and repository methods must be async def
3. **Type Hints**: Every function signature must have complete type annotations
4. **No Secrets in Code**: Use environment variables via app.config.settings
5. **Coverage Gate**: Tests must maintain >= 50% coverage

## Subagent Registry

| Agent | File | Specialization |
|---|---|---|
| python-architect | .claude/agents/subagent-python-architect.md | API design, architecture, models |
| qa-python | .claude/agents/subagent-qa-python.md | Testing, coverage, edge cases |
| security-analyst | .claude/agents/subagent-security-analyst.md | OWASP, auth, input validation |
| docs-analyst | .claude/agents/subagent-docs-analyst.md | Documentation, READMEs |

## Skills Reference

| Skill | Path |
|---|---|
| Kyte Python Patterns (index) | .claude/skills/kyte-python-patterns/SKILL.md |
| FastAPI Patterns | .claude/skills/kyte-python-patterns/fastapi.md |
| Testing Patterns | .claude/skills/kyte-python-patterns/testing.md |

## Context Isolation Rules

- Subagents receive ONLY the files relevant to their task
- Subagents CANNOT modify files outside their scope
- The orchestrator validates all subagent outputs before applying
- Security-sensitive files (.env, credentials) are never shared with subagents

## Slash Commands

| Command | Description |
|---|---|
| /setup-project | Initialize project from template |
| /create-subagent | Interactive wizard for new agents |
