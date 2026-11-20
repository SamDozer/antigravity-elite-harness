# Autonomous Agent Engineering Harness

A structured engineering architecture for autonomous coding agents, providing lifecycle policy enforcement, persistent cross-session memory, durable task dependency tracking, specialized multi-agent coordination, and computational provenance.

---

## 1. System Overview

Most AI coding setups suffer from context window degradation, unbounded tool permissions, and unverified code generation. This harness establishes deterministic control layers around agent execution.

```mermaid
flowchart TD
    User(["Developer / Coordinator"]) --> Router["Agent Dispatcher"]
    
    subgraph MultiAgent["Multi-Agent Roles (Scoped Permissions)"]
        Arch["Architect (Read-Only)"]
        Dev["Developer (TDD)"]
        QA["QA Engineer (Verification)"]
        Sec["Security Auditor (Read-Only)"]
        Sci["Scientific Reviewer (Domain Data)"]
    end
    
    Router --> MultiAgent
    MultiAgent --> TaskEngine["Beads Task DAG Engine"]
    TaskEngine --> MemBank["Intelligent Memory Bank"]
    
    subgraph DefenseDepth["3-Tier Security Architecture"]
        T1["Tier 1: Lifecycle Policy Hooks"]
        T2["Tier 2: Workspace Sandbox"]
        T3["Tier 3: OS Container Boundary"]
    end
    
    MultiAgent --> DefenseDepth
    DefenseDepth --> TargetSystem["Target Codebase & Workspace"]
```

---

## 2. Three-Tier Security Model

Lifecycle hooks provide early intent checks, while sandboxes and virtualization provide hard isolation.

```mermaid
flowchart LR
    subgraph T1["Tier 1: Intent & Policy Hooks"]
        H1["hooks.json"]
        H2["pre-tool-guard.cjs"]
        H3["post-tool-audit.cjs"]
    end

    subgraph T2["Tier 2: Agent Sandbox"]
        S1["Workspace File Boundaries"]
        S2["Default Egress Restriction"]
    end

    subgraph T3["Tier 3: Container / OS Boundary"]
        C1["Docker / DevContainer"]
        C2["Resource Limits (cgroups)"]
        C3["Read-Only System Mounts"]
    end

    ToolReq["Agent Tool Request"] --> T1
    T1 -- Allowed --> T2
    T2 -- Sandboxed Run --> T3
    T3 --> OS["Operating System"]
```

- **Tier 1 (Policy Hooks):** Inspects incoming tool commands before execution. Blocks credential reads (SSH keys, system stores) and requests confirmation for destructive file deletions and forced history rewrites.
- **Tier 2 (Harness Sandbox):** Constrains standard execution to designated workspaces and blocks untracked outbound network requests.
- **Tier 3 (Container Isolation):** Restricts physical memory, CPU usage, and filesystem access via container namespaces and non-root users.

---

## 3. Persistent Memory System

Agents frequently lose historical context between sessions. The memory bank provides indexed cross-session discovery without third-party API dependencies.

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Autonomous Agent
    participant Mem as Memory Bank (memory-bank.cjs)
    participant Store as Local JSONL Store
    participant Doc as Human Gotchas (gotchas.md)

    Agent->>Mem: Query relevant past lessons (--query "git max path")
    Mem->>Store: Lexical ranking & scoring
    Store-->>Mem: Filtered results
    Mem-->>Agent: Relevant gotchas & architectural records
    Note over Agent: Executes task with known constraints
    Agent->>Mem: Record new resolved limitation or bug root cause
    Mem->>Store: Append verified record
    Mem->>Doc: Sync human-readable summary
```

---

## 4. Durable Task Management (DAG Engine)

Context window compaction causes loss of active planning state. The task engine tracks a persistent Directed Acyclic Graph (DAG) in `tasks.json`.

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> InProgress: Dependencies Met
    InProgress --> Blocked: Blocker Encountered
    Blocked --> InProgress: Blocker Resolved
    InProgress --> ReadyForReview: Implementation Complete
    ReadyForReview --> Verified: Quality Gate Sign-Off
    Verified --> Closed: Evidence Confirmed
    Closed --> [*]
```

### Dependency Resolution Workflow

```mermaid
graph TD
    T1["T1: Architectural Contract (Architect)"] --> T2["T2: Core Implementation (Developer)"]
    T2 --> T3["T3: Boundary & Mutation Tests (QA)"]
    T2 --> T4["T4: Security Scan (Security Auditor)"]
    T3 --> T5["T5: Release & Integration"]
    T4 --> T5
```

- Tasks cannot be picked up until all prerequisite dependencies reach `closed` or `verified` status.
- Tasks cannot be marked `closed` without recorded verification evidence.

---

## 5. Multi-Agent Coordination & Boundaries

Unrestricted agents create chaotic edits. Clear roles establish separation of concerns.

```mermaid
flowchart TD
    subgraph PlanningPhase["1. Planning Phase"]
        A1["Architect"] -->|Outputs Specification & Contract| A2["Tasks DAG"]
    end

    subgraph ImplementationPhase["2. Implementation Phase"]
        A2 -->|Unblocked Task| D1["Developer"]
        D1 -->|TDD: Red-Green-Refactor| D2["Code Diff & Unit Tests"]
    end

    subgraph VerificationPhase["3. Verification & Clearance"]
        D2 --> Q1["QA Engineer"]
        D2 --> S1["Security Auditor"]
        D2 --> SC1["Scientific Reviewer"]
        Q1 -->|Property & Mutation Score >= 75%| V1["Quality Clearance"]
        S1 -->|Semgrep / Secret Audit Pass| V2["Security Clearance"]
        SC1 -->|Provenance & Data Grounding| V3["Domain Clearance"]
    end

    V1 & V2 & V3 --> Done["Task Verified & Merged"]
```

| Role | Permissions | Responsibilities |
| :--- | :--- | :--- |
| **Architect** | Read-Only | System structure, typed interface contracts, task DAG generation. |
| **Developer** | Workspace Write | Surgical edits, test-first implementations, minimal code changes. |
| **QA Engineer** | Tests Directory Write | Property-based testing, boundary edge-cases, mutation scoring. |
| **Security Auditor** | Read-Only | Static security analysis, secret scanning, dependency CVE audits. |
| **Scientific Reviewer** | Science Tooling | Database cross-referencing, biological/chemical validation. |
| **Debugger** | Read-Only / Repro | Root-cause tracing, minimal isolated reproduction test cases. |
| **Performance Engineer** | Profiling Tools | Bottleneck analysis, memory leak audits, complexity debloating. |

---

## 6. Scientific Reproducibility & Provenance

For computational biology, chemistry, and data pipelines, reproducibility requires deterministic tracking.

```mermaid
flowchart LR
    RawData["Raw Sequences / Datasets"] --> Hasher["SHA-256 Checksum Engine"]
    Hasher --> Provenance["run_provenance.json"]
    
    subgraph Pipeline["Orchestrated Pipeline (Snakemake / DVC)"]
        Stage1["Step 1: Feature Extraction"]
        Stage2["Step 2: Model Inference / Calculation"]
        Stage3["Step 3: Verification & Reporting"]
        Stage1 --> Stage2 --> Stage3
    end
    
    RawData --> Pipeline
    Params["params.yaml (Fixed Seeds & Releases)"] --> Pipeline
    Pipeline --> Artifacts["Deterministic Result Reports"]
    Artifacts --> Provenance
```

- **Database Anchoring:** Enforces exact release versions (e.g. UniProt, ChEMBL, AlphaFold) rather than dynamic endpoints.
- **Data Hashing:** Tracks SHA-256 signatures of all input files and intermediate features.
- **Fixed Seeds:** Enforces deterministic configuration across execution runs.

---

## 7. Automated CI/CD Quality Pipeline

Every proposed change passes automated multi-stage verification before merging.

```mermaid
flowchart TD
    Commit["Agent Pull Request"] --> PreFlight["Security Pre-Flight"]
    
    subgraph SecurityChecks["Stage 1: Security Scans"]
        G1["Gitleaks Secret Detection"]
        S1["Semgrep SAST Ruleset"]
        O1["OSV Dependency Audit"]
    end
    
    PreFlight --> SecurityChecks
    
    subgraph QualityGate["Stage 2: Code Quality & Testing"]
        L1["Linter & Typecheck"]
        T1["Unit Tests + Coverage"]
        M1["Mutation Testing (Stryker / Mutmut)"]
    end
    
    SecurityChecks -- Pass --> QualityGate
    QualityGate -- Score >= 75% --> Merge["Approved for Merge"]
```

---

## 8. Directory Organization

```text
.
├── .github/
│   ├── workflows/agent-pipeline.yml   # Multi-stage CI/CD workflow
│   └── pull_request_template.md       # Evidence-driven PR review template
├── agents/                            # Role definitions and permissions matrix
│   ├── ROLES_AND_BOUNDARIES.md        # Master delegation matrix
│   └── *.md                           # Individual agent prompts
├── hooks/                             # Lifecycle policy guards
│   ├── hooks.json                     # PreToolUse / PostToolUse bindings
│   ├── pre-tool-guard.cjs             # Credential & command filter
│   └── post-tool-audit.cjs            # Secret leakage inspector
├── memory/                            # Cross-session knowledge persistence
│   ├── memory-bank.cjs                # Memory query and storage engine
│   └── memory-bank.jsonl              # Persistent memory log
├── tasks/                             # Context-loss resilient DAG engine
│   └── beads-tracker.cjs              # Dependency tracker and graph visualizer
├── observability/                     # Session trace telemetry and port allocator
│   ├── trace-analyzer.cjs             # Transcript step & error parser
│   └── port-guard.ps1                 # Local port registry & conflict preventer
├── rules/                             # Curated operational guidelines
│   └── GEMINI.md                      # Unified engineering standard
├── templates/                         # Reproducible configuration templates
│   ├── sandbox/                       # Docker & DevContainer isolation
│   ├── git-security/                  # Pre-commit & secret config
│   ├── testing/                       # Property and mutation test setups
│   └── science-provenance/            # Snakemake, DVC, and provenance scripts
└── tests/
    └── run-audit.cjs                  # Runtime verification test runner
```

---

## 9. Quickstart Guide

### 1. Initialize Task Graph
```bash
node tasks/beads-tracker.cjs init --project "my-project"
node tasks/beads-tracker.cjs add --id "T1" --title "Core Contract" --role "architect"
node tasks/beads-tracker.cjs next
```

### 2. Query Project Memory
```bash
node memory/memory-bank.cjs recall --query "port allocation"
```

### 3. Record a Discovered Gotcha
```bash
node memory/memory-bank.cjs record \
  --project "my-project" \
  --category "api_gotcha" \
  --title "Header Encoding Issue" \
  --content "Upstream proxy requires explicit Latin-1 header encoding." \
  --verified
```

### 4. Run Self-Verification
```bash
node tests/run-audit.cjs
```
