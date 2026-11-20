# Knowledge Graph Architectural Report: Antigravity Elite Harness

Generated at: 2026-11-20T03:42:30.480Z

## Executive Summary
- **Total Graph Nodes:** 63
- **Total Edges:** 16
- **Detected Functional Communities:** 7

## Functional Communities
### Security & Lifecycle (4 components)
- `hooks/hooks.json`
- `hooks/post-tool-audit.cjs`
- `hooks/pre-tool-guard.cjs`
- `SECURITY_ARCHITECTURE.md`

### Memory & Context (2 components)
- `memory/memory-bank.cjs`
- `memory/memory-bank.jsonl`

### Task Orchestration (1 components)
- `tasks/beads-tracker.cjs`

### Agent Roles (RBAB) (10 components)
- `agents/agents.json`
- `agents/architect.md`
- `agents/debugger.md`
- `agents/developer.md`
- `agents/performance-engineer.md`
- `agents/qa-engineer.md`
- `agents/researcher.md`
- `agents/ROLES_AND_BOUNDARIES.md`
- *...and 2 more*

### Quality & CI/CD (10 components)
- `.github/pull_request_template.md`
- `.github/workflows/agent-pipeline.yml`
- `templates/ci-cd/.github/workflows/agent-pipeline.yml`
- `templates/ci-cd/pull_request_template.md`
- `templates/ci-cd/semgrep.yml`
- `templates/testing/fast-check.example.ts`
- `templates/testing/hypothesis_example.py`
- `templates/testing/mutmut.ini.template`
- *...and 2 more*

### Science & Provenance (5 components)
- `templates/science-provenance/dvc.yaml.template`
- `templates/science-provenance/params.yaml.template`
- `templates/science-provenance/provenance_tracker.py`
- `templates/science-provenance/SCIENTIFIC_PROVENANCE_GUIDE.md`
- `templates/science-provenance/Snakefile.template`

### Observability & Rules (31 components)
- `.gitignore`
- `evals/promptfoo.yaml`
- `observability/local-ports-registry.json`
- `observability/LOCAL_PORTS_DIRECTORY.md`
- `observability/port-guard.ps1`
- `observability/trace-analyzer.cjs`
- `README.md`
- `rules/adaptive-responsive-ui.md`
- *...and 23 more*

## God Nodes / Central Architectural Hubs
- **`tasks/beads-tracker.cjs`** (Centrality Degree: 4)
- **`tests/run-audit.cjs`** (Centrality Degree: 4)
- **`hooks/pre-tool-guard.cjs`** (Centrality Degree: 3)
- **`memory/memory-bank.cjs`** (Centrality Degree: 3)
- **`hooks/hooks.json`** (Centrality Degree: 2)

## Suggested Graph Explorations
1. **Trace security isolation:** `hooks/hooks.json` -> `hooks/pre-tool-guard.cjs` -> `SECURITY_ARCHITECTURE.md`
2. **Trace task execution:** `agents/ROLES_AND_BOUNDARIES.md` -> `tasks/beads-tracker.cjs` -> `memory/memory-bank.cjs`
3. **Trace science provenance:** `templates/science-provenance/Snakefile.template` -> `templates/science-provenance/provenance_tracker.py`
