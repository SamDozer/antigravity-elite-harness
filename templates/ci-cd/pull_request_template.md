## Summary of Changes
<!-- Provide a clear, concise summary of the problem and the minimal solution. -->

- **Beads Task ID:** `T-XX` (or N/A)
- **Role:** [Architect / Developer / Debugger / QA Engineer / Security Auditor]

## Methodology & Verification Checklist
- [ ] **Ponytail Check:** Is this the smallest complete change that solves the issue? No speculative abstractions.
- [ ] **TDD Verification:** Was the failing test written first (Red -> Green -> Refactor)?
- [ ] **Runtime Verification:** Were real CLI commands, API calls, or UI states driven and verified with demonstrable output?
- [ ] **Regression & Adjacent Check:** Was at least one neighboring behavior or adjacent callsite checked?
- [ ] **Secret & Security Check:** No hardcoded tokens, API keys, or unsanitized shell inputs.
- [ ] **Could Not Verify List:** Declared explicitly if any path could not be verified in this environment.

## Demonstrable Evidence
```text
<!-- Paste actual test runner, linter, or CLI output proving the change works -->
```
