---
name: diff-reviewer
description: Adversarial diff reviewer auditing changes across 7 engineering vectors plus an optional 8th scientific-integrity vector. Use when reviewing git diffs, pull requests, commits, or staged changes for bugs, security vulnerabilities, memory leaks, missing tests, and scientific data leakage. Do NOT use when initially drafting architecture before code exists, generating new boilerplate from scratch, or styling UI wireframes.
---

# Diff Reviewer Skill (7+1 Vectors)

Review pull requests, commits, and working tree diffs with adversarial rigor.

## The Review Vectors
1. **Logic Correctness & Edge Cases:** Off-by-one errors, null/undefined safety, empty inputs, unhandled error paths.
2. **Security & Injection:** Parameterized queries, secret handling, input sanitization, safe deserialization.
3. **Reliability & Memory Leaks:** Unbounded in-memory maps/sets, timer cleanup, connection pool release, backpressure.
4. **Test Coverage & Invariants:** Unit and property tests covering boundary edge cases. Never accept tests deleted or assertions weakened to achieve green CI.
5. **Altitude & Root-Cause Depth:** Fix situated at root cause in origin system rather than symptom-masking `if` checks in callers.
6. **Performance & Latency:** Avoid N+1 queries, unindexed searches, synchronous blocking operations in event loops.
7. **Minimalism & SLOC Debloat (Ponytail):** Delete dead code; remove unused wrappers, speculative abstractions, and features nobody asked for.
8. **Scientific Integrity (Active in bio/data codebases):**
   - *Unit consistency:* nm vs. Å (1 nm = 10 Å), kJ/mol vs. kcal/mol (1 kcal = 4.184 kJ), log2 vs. ln.
   - *Indexing & silent broadcasting:* NumPy/Pandas shape mismatches, silent `.dropna()` masking data issues.
   - *Statistical & ML leakage:* Scaling, imputing, or feature selection applied before train/test splitting.
   - *Portability:* Hardcoded user paths (`/home/user`, `C:\Users\...`) and unpinned environment dependencies.

## Workflow
1. Extract the active diff:
   ```bash
   git diff HEAD~1 > patch.diff
   ```
2. Run automated diff static analysis:
   ```bash
   python skills/core/diff-reviewer/scripts/review_diff.py --diff patch.diff --bio
   ```
3. Consult the detailed vector definitions in `references/review_vectors.md`.
4. Synthesize the findings into `assets/review_report.template.md` with an unambiguous verdict (`APPROVED`, `APPROVED WITH WARNINGS`, or `REJECTED`).

## Hard Constraints
- Ground every criticism in explicit lines from the actual git diff.
- Never certify a PR without checking at least one neighboring callsite for ripple regressions.
