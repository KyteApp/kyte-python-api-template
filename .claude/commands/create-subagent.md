---
name: create-subagent
description: Interactive wizard to create a new Claude Code subagent
---

# /create-subagent

Create a new specialized subagent for this project.

## Steps

1. **Ask for agent details**:
   - Name (kebab-case, e.g., `api-designer`)
   - Description (one line)
   - Specialization area
   - Allowed tools (from: Read, Grep, Glob, Write, Bash, WebSearch)

2. **Generate the agent file** at `.claude/agents/subagent-<name>.md`:
   ```markdown
   ---
   name: <name>
   description: <description>
   tools:
     - <tool1>
     - <tool2>
   ---

   # <Title> Subagent

   You are a <specialization> specialist at Kyte.

   ## Expertise
   - <area 1>
   - <area 2>

   ## Responsibilities
   1. <responsibility 1>
   2. <responsibility 2>

   ## Constraints
   - <constraint 1>
   - <constraint 2>
   ```

3. **Register in .claude/CLAUDE.md**:
   Add a row to the Subagent Registry table.

4. **Confirm** the agent was created and registered.

## Guidelines

- Agent names should be descriptive of their role
- Keep tool permissions minimal (principle of least privilege)
- Each agent should have a clear, non-overlapping scope
- Write detailed expertise and responsibilities sections
