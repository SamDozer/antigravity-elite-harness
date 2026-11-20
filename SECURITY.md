# Security Policy & Operational Boundaries

## 1. Supported Versions
| Harness Version | Security Support |
| :--- | :--- |
| **1.0.x** | ✅ Active security patching |

## 2. Threat Model & Mechanical Boundaries
This harness enforces defense-in-depth across three tiers:
1. **Tier 1 (Application Hooks):** `pre-tool-guard.cjs` mechanically denies private credential reads (`~/.ssh/id_*`, SAM files) and requires interactive confirmation for destructive commands (`rm -rf /`, `git push --force`).
2. **Tier 2 (Harness Sandbox):** Constrains execution to the active workspace. Out-of-workspace writes and unapproved egress are blocked.
3. **Tier 3 (Container Isolation):** Docker containers enforce 4GB RAM limits and non-root user execution (`UID 1000`).

## 3. Supply-Chain Hygiene
- **Zero Unpinned Runtime Downloads:** No script in this harness downloads unpinned binaries, executes `curl | sh`, or runs arbitrary `npx` commands during tool invocations.
- **Audited Dependencies:** Local utilities (`memory-bank.cjs`, `beads-tracker.cjs`, `pre-tool-guard.cjs`) are written in native, standard Node.js with **zero external npm dependencies**.

## 4. Reporting a Security Vulnerability
If you discover a security vulnerability or sandbox bypass, please report it privately via GitHub Security Advisories or email `security@antigravity.local`. We respond within 24 hours.
