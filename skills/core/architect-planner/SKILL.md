---
name: architect-planner
description: Read-only architectural planning, task decomposition into Beads DAG, and interface contract specification. Use when designing system architecture, breaking down complex multi-step features into dependency-ordered tasks, creating implementation_plan.md before coding, or establishing module contracts. Do NOT use when actively writing production code, debugging a single-line bug, reviewing a pull request diff, or executing trivial one-step file edits.
---

# Architect Planner Skill

Decompose ambitious system requirements into robust, minimal, and dependency-mapped implementation plans.

## Operational Boundaries
- **Strictly Read-Only:** The architect role inspects code, schemas, and git history. It never writes or edits production application code directly.
- **Contract-First:** Interface boundaries (TypeScript types, Pydantic models, JSON schemas) must be explicitly specified before implementation tasks are generated.
- **Durable Task Graph:** Tasks must be organized as a directed acyclic graph (DAG) via Beads (`tasks/beads-tracker.cjs`), with clear `depends_on` relationships.

## Workflow

### 1. Context & Prior Art Recall
- Query cross-session memory for historical lessons and architecture decisions:
  ```bash
  node memory/memory-bank.cjs recall --query "<feature domain>"
  ```
- Inspect `gotchas.md` in the target project root for documented edge cases.

### 2. Interface Specification
- Draft concrete data schemas and function signatures before breaking down work.
- Keep data structures aligned with platform-native conventions (avoid premature wrappers or speculative abstractions).

### 3. Task Decomposition (Beads DAG)
- Formulate tasks using the starter template at `assets/implementation_plan.template.md`.
- Ensure each task represents 2 to 15 minutes of developer effort.
- Every task MUST contain:
  1. Target file paths.
  2. Input contracts and expected output behavior.
  3. Precise, executable verification commands (e.g. `npm test`, `pytest tests/test_core.py`).

### 4. Deterministic Plan Validation
- Run the plan validation script before handing off to developers:
  ```bash
  python skills/core/architect-planner/scripts/validate_plan.py --plan implementation_plan.md
  ```
- The validator enforces that objectives, architecture contracts, Beads tasks, verification gates, and rollback plans are present.

## Hard Constraints
- No task may depend on an unverified or cyclic dependency.
- Deletion beats addition: prioritize reusing existing helpers over introducing new dependencies.
- Plan verification must be grounded in executable test commands, not prose assurances.
