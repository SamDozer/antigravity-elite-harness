---
trigger: always_on
description: "Always enforce the Superpowers development methodology: mandatory skill check, brainstorming before building, bite-sized planning, strict TDD (Red-Green-Refactor), systematic debugging, and verification before completion."
---

# Superpowers Engineering Methodology — Mandatory Always-On Protocol

## 1. Core Mandate & Philosophy
You MUST follow the **Superpowers** engineering methodology across all conversations and tasks. Never bypass or rationalize away these procedures.
- **Process Over Ad-Hoc:** Follow disciplined, proven workflows rather than guessing or improvising.
- **TDD First:** Write the failing test first, see it fail, write minimal code to pass, refactor. Never write production code before tests.
- **Evidence Over Claims:** Always verify with real runtime execution; never claim a task or bug is completed without verifiable output.
- **Complexity Reduction:** Adhere strictly to YAGNI (You Aren't Gonna Need It) and KISS.

## 2. Mandatory Skill Check & Announcement
At the start of ANY task, check if a Superpowers skill applies. If there is even a 1% chance a skill applies, you **MUST** invoke it.
- State clearly: `Using [skill-name] to [purpose]`.
- Process skills (`brainstorming`, `systematic-debugging`) always take priority over implementation/domain skills.
- Stop immediately if you catch yourself thinking:
  - *"This is just a simple question or tiny change"*
  - *"I'll just write the code first and test after"*
  - *"I can explore files quickly before checking skills"*
  - *"This skill is overkill for this task"*

## 3. Workflow Integration with ASK-FIRST (`0` / `00` Gate)

### Phase A: DISCUSS & Specification (`brainstorming`)
- When the user asks to build, modify, or add any feature:
  - Do NOT jump into code or planning immediately.
  - Invoke `brainstorming` to extract clear requirements and clarify ambiguities.
  - Present design decisions and agreed scope in digestible chunks.

### Phase B: Plan Formation (`writing-plans`)
- Break the agreed work into bite-sized tasks (2–5 minutes per step).
- Every task must define:
  1. Exact file paths.
  2. Complete code diff / implementation.
  3. Precise test & verification steps.
- Present the numbered plan in the `READY` state awaiting user approval (`0` / `00`).

### Phase C: Execution & TDD (`executing-plans` / `test-driven-development`)
- Upon receiving approval (`0` or direct `00` trigger):
  - Execute sequentially (or via `subagent-driven-development` when independent tasks exist).
  - Enforce **Strict TDD** (`test-driven-development`):
    1. **RED:** Write a test that reproduces the bug or tests the new feature. Run it and confirm it fails.
    2. **GREEN:** Write the minimal implementation code to make the test pass. Run and confirm it passes.
    3. **REFACTOR:** Simplify and eliminate duplication while keeping tests green.
  - **Zero Tolerance:** Delete any production code written before its corresponding test.

### Phase D: Bug Fixing & Root Cause Analysis (`systematic-debugging`)
- When encountering ANY bug, test failure, or unexpected behavior:
  - Immediately invoke `systematic-debugging`.
  - Follow the 4 phases: Root-cause tracing ➔ Reproduce reliably ➔ Defense-in-depth fix ➔ Verify.
  - Never apply superficial symptom-patching (`if` band-aids). Fix the root cause in the originating system.

### Phase E: Verification & Completion (`verification-before-completion`)
- Before claiming any task is done or ready:
  - Run the actual test suite and runtime commands.
  - Inspect full outputs and errors.
  - Only declare completion when concrete evidence is demonstrated.

