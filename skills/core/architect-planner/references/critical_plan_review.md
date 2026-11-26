# Critical Plan Review (Adversarial Red-Teaming)

Run this stage in a **fresh context or separate subagent** after `implementation_plan.md` is drafted for any `Architectural` task (> 3 files, unnamed files, or schema/API changes).

## Review Directives
1. **Read Actual Target Code & `gotchas.md`:** Never judge a plan from plan prose alone. Inspect the real files and `gotchas.md` / `memory-bank.cjs` first.
2. **Challenge Unsupported Assumptions:** Hunt for race conditions, missing timeouts, non-idempotent retries, missing rollback steps, and breaking caller contracts.
3. **Apply the YAGNI Brake:** Distinguish real failure modes from speculative over-engineering; delete unnecessary abstractions.
4. **Findings or Proof:** List concrete findings by severity (`Critical`, `Major`, `Minor`), or explicitly state what files/contracts were verified rather than rubber-stamping "looks solid".

## Required Verdict
- `APPROVED` / `CHANGES REQUESTED` / `REJECTED` + corrected plan + residual unverified risks.
