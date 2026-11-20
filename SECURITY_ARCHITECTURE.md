# Antigravity Three-Tier Defense-in-Depth Security Model

## Overview
AI coding agents require robust boundaries to prevent accidental or malicious actions. A common misconception is treating application-level hooks as operating system boundaries. 
Antigravity enforces a strict **Three-Tier Security Architecture**:

`mermaid
flowchart TD
    subgraph Tier1[Tier 1: Application-Level Hooks (Intent & Policy)]
        H1[hooks.json Lifecycle]
        H2[pre-tool-guard.cjs]
        H3[post-tool-audit.cjs]
    end

    subgraph Tier2[Tier 2: Antigravity Process Sandbox (Harness Boundary)]
        S1[Standard Sandbox Mode (BypassSandbox: false)]
        S2[Workspace & Artifact Isolation]
        S3[Network Egress Deny Default]
    end

    subgraph Tier3[Tier 3: OS & Virtualization Boundary (Kernel Enforcement)]
        C1[Docker / DevContainers]
        C2[WSL2 / Linux Namespaces]
        C3[cgroup Resource Caps (RAM/CPU)]
        C4[Read-Only System Mounts]
    end

    Agent[AI Agent / LLM Turn] --> Tier1
    Tier1 -- Allow Tool Call --> Tier2
    Tier2 -- Subshell Execution --> Tier3
    Tier3 -- Hard Kernel Boundary --> HostOS[Host System / Windows OS]
`

---

## The Three Tiers Explained

### Tier 1: Application & Lifecycle Hook Layer
- **Components:** hooks.json, pre-tool-guard.cjs, post-tool-audit.cjs.
- **Purpose:** Fast semantic filtering, policy injection, and early rejection before tool execution.
- **Enforcement Mechanisms:**
  - un_command inspection: blocks private SSH key reading (~/.ssh), SAM database extraction, and unconfirmed m -rf / or git push --force.
  - write_file/edit_file inspection: scans for exposed API keys and credentials before files land on disk.
- **Crucial Boundary Limitation:** Hooks run within the agent harness process. If a hook script encounters an unhandled exception or times out, agent runners may fail open to prevent deadlock. **Hooks are policy guards, NOT OS security boundaries.**

### Tier 2: Antigravity Sandbox Layer
- **Components:** Built-in Antigravity Sandbox (BypassSandbox: false).
- **Purpose:** Restricts the executing subshell to designated workspace directories.
- **Enforcement Mechanisms:**
  - Default network egress is blocked for sandboxed commands.
  - Read/write access is restricted to the active workspace, rain/<conversation-id>/, and temporary scratch spaces.
  - Access to arbitrary host directories (C:\Windows, user profile roots) fails with permission denied.
- **Bypass Rule:** Only explicitly approved tools with BypassSandbox: true run outside this sandbox.

### Tier 3: Operating System & Container Isolation Layer
- **Components:** Docker containers (Dockerfile.sandbox, docker-compose.sandbox.yml), DevContainers, WSL2.
- **Purpose:** Hardware and kernel-level isolation that the agent process physically cannot escape.
- **Enforcement Mechanisms:**
  - **Filesystem Isolation:** Host filesystems are mounted read-only (:ro) except for the dedicated workspace directory. Host SSH directories (~/.ssh) and cloud tokens are NEVER mounted into the container.
  - **Resource Cgroups:** Capped at 4GB RAM and 2 CPU cores to physically prevent runaway memory exhaustion or fork-bombs.
  - **Process Isolation:** Runs as a non-privileged sandboxuser (UID 1000), disabling root capabilities (cap_drop: ALL).
  - **Network Namespaces:** Network access is isolated and can be disabled (
etwork_mode: none) for offline builds and tests.

---

## Operational Security Checklist for Developers

1. **Never mount host secret paths** (~/.aws, ~/.ssh, ~/.kube) into agent execution environments.
2. **Always test sandboxed first** (BypassSandbox: false). Only escalate when network or elevated host tools are required.
3. **Commit pre-commit hooks** (gitleaks, semgrep) to repositories so commits created by agents are validated before leaving the local machine.
4. **Enforce the Principle of Least Privilege** across subagents: read-only roles (Architect, Security Auditor) must never have shell execution or write access.