# Three-Tier Defense-in-Depth Security Model

This specification details the security boundaries, hook IPC contracts, and sandboxing infrastructure for the **Antigravity Elite AI Engineering Harness**.

---

## 1. Executive Security Architecture

AI coding agents require robust boundaries to prevent accidental or malicious actions. A common architectural failure is treating application-level hooks as operating system boundaries. 

The harness enforces a **Three-Tier Security Architecture**:

```mermaid
flowchart TD
    subgraph Tier1[Tier 1: Application-Level Hooks (Intent & Policy)]
        H1[plugin.json Lifecycle Hooks]
        H2[pre-tool-guard.cjs - AST & Command Filter]
        H3[post-tool-audit.cjs - Telemetry & Audit Log]
    end

    subgraph Tier2[Tier 2: Antigravity Process Sandbox (Harness Boundary)]
        S1[Workspace Isolation]
        S2[Artifact & Brain Directory Scoping]
        S3[Default Network Egress Restrictions]
    end

    subgraph Tier3[Tier 3: OS & Virtualization Boundary (Kernel Enforcement)]
        C1[Docker & DevContainers]
        C2[Linux Namespaces & UID Remapping]
        C3[cgroup Hardware Caps (4GB RAM, 2 CPUs)]
        C4[Read-Only System Mounts (:ro)]
    end

    Agent[AI Agent / LLM Turn] --> Tier1
    Tier1 -- Allowed Call --> Tier2
    Tier2 -- Subshell Invocation --> Tier3
    Tier3 -- Hard Kernel Isolation --> HostOS[Host Operating System]
```

---

## 2. Tier Details & Responsibilities

### Tier 1: Application & Lifecycle Hook Layer
* **Components:** `plugin.json`, `hooks/pre-tool-guard.cjs`, `hooks/post-tool-audit.cjs`.
* **Purpose:** Fast semantic filtering, policy injection, and early rejection before tool execution begins.
* **Mechanism:** Intercepts `PreToolUse` and `PostToolUse` events via Node.js IPC.
* **Critical Boundary Limitation:** Hooks execute within the agent harness process. If a hook script encounters an unhandled exception or times out, agent harnesses may fail open. **Hooks are policy guards, NOT OS security boundaries.**

### Tier 2: Antigravity Sandbox Layer
* **Components:** Built-in Antigravity Sandbox (`BypassSandbox: false`).
* **Purpose:** Restricts the executing subshell to designated workspace directories.
* **Enforcement:**
  * File read/write access is restricted to the active workspace and temporary scratch spaces.
  * Direct read/write access to host operating system roots (`C:\Windows`, `/etc`, user home credentials) is rejected.
  * Only explicitly approved tools with `BypassSandbox: true` execute outside this sandbox.

### Tier 3: Operating System & Container Isolation Layer
* **Components:** Docker containers (`templates/Dockerfile.sandbox`, `docker-compose.sandbox.yml`), DevContainers, WSL2.
* **Purpose:** Hardware and kernel-level isolation that the agent process physically cannot escape.
* **Enforcement:**
  * **Filesystem Isolation:** Host filesystems are mounted read-only (`:ro`) except for the dedicated project workspace directory.
  * **Zero Host Secret Exposure:** Directories containing credentials (`~/.ssh`, `~/.aws`, `~/.kube`, token stores) are NEVER mounted into the container.
  * **Resource cgroups:** Capped at 4 GB RAM and 2 CPU cores to prevent runaway memory exhaustion or fork-bombs.
  * **Non-Root Execution:** Runs as an unprivileged user (UID 1000) with all capabilities dropped (`cap_drop: ALL`).

---

## 3. Hook IPC Specification (`pre-tool-guard.cjs`)

The `pre-tool-guard.cjs` script intercepts tool calls via standard I/O IPC.

### Request Payload Schema
```json
{
  "toolName": "run_command",
  "toolInput": {
    "CommandLine": "cat ~/.ssh/id_rsa",
    "toolSummary": "Inspect key"
  },
  "context": {
    "workspace": "/path/to/project",
    "role": "Developer"
  }
}
```

### Response Exit Codes
| Exit Code | Decision | Harness Action |
| :--- | :--- | :--- |
| **`0`** | `ALLOW` | Tool proceeds immediately to execution. |
| **`1`** | `ASK` / `WARN` | Harness pauses and prompts user for explicit manual confirmation. |
| **`2`** | `DENY` | Execution is aborted immediately with an explanation returned to the agent. |

### Interception Rules Matrix
| Target Pattern | Action | Reason |
| :--- | :--- | :--- |
| Reading `~/.ssh/id_*`, `id_ed25519` | `DENY (2)` | Credential exfiltration prevention. |
| Reading Windows SAM / SYSTEM hives | `DENY (2)` | Host OS security boundary protection. |
| `rm -rf /` or recursive drive deletion | `DENY (2)` | Catastrophic host damage prevention. |
| `git push --force` or branch overwrites | `ASK (1)` | Destructive history rewrite requires user sign-off. |
| High blast-radius operations (`DROP DATABASE`) | `ASK (1)` | Irreversible data mutation requires confirmation. |
| Committing unencrypted `.env` or API keys | `DENY (2)` | Secret leak prevention before landing on disk. |

---

## 4. Operational Security Checklist

1. **Keep `BypassSandbox: false` as Default:** Never grant sandbox bypass unless interacting with explicit, trusted local development servers.
2. **Never Mount Host Credentials:** Container templates must mount only the active project directory.
3. **Audit Pre-Commit Gates:** Ensure secret scanners (`gitleaks`, `detect-secrets`) are executed before any git commit is generated.
4. **Enforce Role-Based Boundaries (RBAB):** Architectural, research, and review roles must remain strictly read-only with shell execution disabled.
