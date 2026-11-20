# Global Rule — Aggressive Code Debloating & Goal-SLOC Protocol (maxim-saplin/goal-sloc)

## Core Mandate
Source Lines of Code (SLOC) and structural compactness are primary engineering constraints. You MUST actively resist code expansion, proactively de-bloat existing files, and write the minimal code necessary to solve the problem reliably, cleanly, and maintainably.

---

## 1. Anti-Metric Gaming Rules (No Cheap Tricks)
Do NOT "game" line counts or metric targets through superficial formatting hacks:
- ❌ NEVER combine multiple statements onto a single line (e.g. `if (x) { doA(); doB(); return; }`).
- ❌ NEVER delete essential docstrings, public API documentation, or license headers just to reduce line count.
- ❌ NEVER compress readable JSX/HTML or multi-line object definitions into unreadable single-line strings.
- ❌ NEVER replace readable descriptive variable names with single-letter abbreviations to make expressions fit on fewer lines.

Reductions must be **structurally real**, not visual illusions.

---

## 2. Honest Structural Reduction Hierarchy
When writing new features or refactoring existing code, apply debloating in this strict order:

1. **Delete Dead & Zombie Code:**
   - Eradicate unused functions, abandoned feature flags, dead branches, commented-out code blocks, and redundant imports.
2. **Reuse Platform Built-ins & Existing Dependencies:**
   - Replace hand-rolled algorithms, custom string/date/array helpers, or mini-parsers with standard library methods (`Array.prototype.*`, `itertools`, `Pathlib`, `re`, etc.) or already-installed dependencies.
3. **Flatten Deep Nesting via Guard Clauses:**
   - Convert nested `if-else` pyramids into early returns / guard clauses. Eliminates indentation and redundant `else` blocks.
4. **Eliminate Intermediate Pass-Through State:**
   - Remove redundant local variables that are declared only to be immediately returned or passed to a single function call.
   - Streamline data pipelines: chain operations cleanly rather than creating intermediate accumulation variables.
5. **Consolidate Duplicate & Parallel Logic:**
   - Unify copy-pasted switch/case or conditional blocks into declarative lookup tables, maps, or unified handlers.

---

## 3. Preflight & Verification Safety Net
Whenever undertaking a debloating or refactoring pass:
1. **Preflight Baseline:** Inspect the existing surface, confirm existing tests pass (or understand expected runtime contracts).
2. **Surgical Diff:** Apply reductions in logical units; never perform untestable mass deletions across unrelated modules simultaneously.
3. **Behavioral Integrity:** Every cut must preserve 100% of runtime behavior, contracts, and edge-case resilience.
4. **Post-Reduction Verification:** Execute tests or verify runtime commands immediately to confirm no regression was introduced.

---

## 4. Clear Stop Conditions & Escalation
- **Do not spin indefinitely:** Once all genuine structural bloat, dead code, and redundant abstractions have been removed, STOP.
- If further SLOC reduction would require sacrificing readability, type safety, or architectural clarity, escalate to the user and explain the trade-off rather than forcing unnatural compression.

