# Implementation Plan: Session Rate-Limiting & Memory Storage

**Status:** READY FOR HUMAN SIGN-OFF  
**Assigned Agent:** Architect (Read-Only)  
**Beads Task Graph ID:** `TASK-RATE-LIMIT-01`

---

## 1. User Review Required (Blockers & Decisions)
> [!IMPORTANT]
> - **Storage Backend Decision:** Should rate limits be stored in local memory (`memory-bank.jsonl`) or an atomic in-memory sliding log? *(Default: in-memory sliding log with persistent fallback)*.
> - **Rate Limit Quota:** Proposed 60 requests/minute per IP with a burst limit of 10. Confirm if higher capacity is needed for enterprise workloads.

---

## 2. Open Questions & Risk Assessment
- **Q1:** How does the rate limiter behave during upstream redis network timeouts?
  - *Risk:* Failing closed blocks valid users; failing open allows quota abuse.
  - *Resolution:* Enforce local memory-fallback sliding window if remote cache disconnects.
- **Q2:** Clock Skew in distributed containers:
  - *Mitigation:* Use UTC monotonic timestamps (`process.hrtime.bigint()`).

---

## 3. Proposed Changes (Minimal Diff Scope)

### Component: Rate Limiter Middleware
- **Path:** `src/middleware/rate-limiter.ts`
- **Action:** Create new minimal pure function.
- **Contract:**
  ```typescript
  export interface RateLimitResult {
    allowed: boolean;
    remaining: number;
    resetTimeMs: number;
  }
  export function checkRateLimit(key: string, nowMs: number, windowMs: number, maxHits: number): RateLimitResult;
  ```

### Component: Unit & Invariant Tests
- **Path:** `tests/middleware/rate-limiter.test.ts`
- **Action:** Write failing tests first (Red -> Green -> Refactor).
- **Invariants Tested:**
  1. Monotonicity: Remaining hits strictly decreases within window.
  2. Window Reset: Hits return to `maxHits` after `windowMs` elapses.
  3. Boundary fuzzing: 500 concurrent requests must never exceed `maxHits`.

---

## 4. Verification Plan & Quality Gate Criteria
- [ ] Unit tests pass: `npm test -- tests/middleware/rate-limiter.test.ts`
- [ ] Stryker Mutation Score $ge 80%$ killed mutants.
- [ ] Memory leak audit: 10,000 requests must not leak memory references in sliding window map.
- [ ] Semgrep SAST scan: Zero findings for unvalidated IP parameter injection.
