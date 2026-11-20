# Contributing to Antigravity Elite Harness

We welcome contributions! To maintain senior engineering rigor and protect agents from context bloat, all contributions must adhere to these standards:

## 1. Context Budget Rule (Strict)
- **Always-on Rules:** Any rule added to `rules/` MUST NOT exceed **3.5 KB (~800 tokens)**.
- **Heavy Guidelines:** Extensive domain guidelines (e.g., UI component libraries, deep review rubrics) must be packaged as **lazy-loaded skills**, not always-on rules.

## 2. Dependency Rule
- Core utilities (`hooks/`, `memory/`, `tasks/`) MUST use standard Node.js APIs. **Do not add npm dependencies to core runtime utilities.**

## 3. Pull Request Requirements
- Run validation: `node scripts/validate.js`
- Run test suite: `node tests/run-audit.cjs` (must pass 100%)
- Include runtime evidence in your PR description.
