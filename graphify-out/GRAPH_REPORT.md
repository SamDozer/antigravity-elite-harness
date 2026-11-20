# Knowledge Graph Architectural Report: Antigravity Elite Harness

Generated at: 2026-11-20T05:22:00.000Z

## Executive Summary
- **Total Graph Nodes:** 128
- **Total Edges:** 48
- **Detected Functional Communities:** 10

---

## Functional Communities

### 1. Technical Documentation & Whitepapers (6 components)
- `docs/architecture.md` (System overview, 5 failure modes, execution lifecycle)
- `docs/security-architecture.md` (Three-tier defense, hook IPC specifications)
- `docs/memory-and-beads.md` (Cross-session memory bank and Beads task DAG)
- `docs/rbab-and-ci.md` (Role-based boundaries, 8 specialized agents, CI/CD pipeline)
- `docs/comp-bio-provenance.md` (Bioinformatics workflows, Snakemake, and cryptographic ledgers)
- `docs/assets/ui-comparison.png` (Visual before/after UI contrast proof)

### 2. Quality & CI/CD (12 components)
- `.github/workflows/ci.yml` (Zero-dependency GitHub Actions quality gate)
- `.github/pull_request_template.md`
- `scripts/validate.js` (Schema, token budget, and supply-chain auditor)
- `scripts/validate_skills.py` (Claude-grade 4-layer architecture validator)
- `tests/run-audit.cjs` (Comprehensive runtime verification suite)
- `templates/ci-cd/pull_request_template.md`
- `templates/ci-cd/semgrep.yml`
- `templates/testing/fast-check.example.ts`
- `templates/testing/hypothesis_example.py`
- `templates/testing/mutmut.ini.template`
- `evals/eval_runner.js`
- `evals/eval_cases.json`

### 3. Core Engine & Packaging (8 components)
- `package.json` (Unifed test/verify/audit entrypoints)
- `plugin.json` (Official Antigravity plugin manifest)
- `LICENSE` (MIT License)
- `.gitattributes` (Linguist language filtering)
- `install.sh` (POSIX multi-profile installer with rollback)
- `install.ps1` (PowerShell multi-profile installer with rollback)
- `CHANGELOG.md` (v1.0.0 release notes)
- `README.md` (Scannable landing page with visual proof)

### 4. Agent Roles & Boundaries (RBAB) (10 components)
- `agents/agents.json`
- `agents/ROLES_AND_BOUNDARIES.md`
- `agents/architect.md`
- `agents/developer.md`
- `agents/qa-engineer.md`
- `agents/security-auditor.md`
- `agents/debugger.md`
- `agents/performance-engineer.md`
- `agents/researcher.md`
- `agents/bio-specialist.md`

### 5. Security & Lifecycle Hooks (3 components)
- `hooks/hooks.json` (Lifecycle event registrations)
- `hooks/pre-tool-guard.cjs` (AST command inspection & credential protection)
- `hooks/post-tool-audit.cjs` (Execution auditing & telemetry)

### 6. Persistent Memory & State (3 components)
- `memory/memory-bank.cjs` (Zero-API TF-IDF retrieval engine)
- `memory/memory-bank.jsonl`
- `tasks/beads-tracker.cjs` (Context-resilient task DAG engine)

### 7. Core Skills (9 components)
- `skills/core/architect-planner/` (Spec schema, validation, implementation planning)
- `skills/core/diff-reviewer/` (`review_diff.py` 8-vector AST pull request reviewer)

### 8. Frontend UI Skills (22 components)
- `skills/frontend/app-ui-system/` (CSS design tokens, responsive typography)
- `skills/frontend/web-editorial-design/` (Editorial typography & marketing presets)
- `skills/frontend/frontend-interaction-states/` (Loading, empty, error, disabled states)
- `skills/frontend/data-viz-ui/` (Single-axis palettes, accessible data viz)
- `skills/frontend/ui-visual-qa/` (`visual_audit.mjs` WCAG 2.2 AA contrast auditor)

### 9. Computational Biology Skills (25 components)
- `skills/comp-bio/bio-orchestrator/` (`inspect_biofile.py` binary magic byte parser)
- `skills/comp-bio/structural-bio-md/` (`validate_pdb.py` pLDDT & structure validator)
- `skills/comp-bio/bio-sequence-stats/` (`stats_guard.py` Benjamini-Hochberg FDR corrector)
- `skills/comp-bio/hpc-containers-pipelines/` (`slurm_template.sh` GPU cluster script)
- `skills/comp-bio/scientific-figures/` (`pub_style.mplstyle` Nature publication styles)
- `skills/comp-bio/bio-literature-grounding/` (`verify_ids.py` UniProt/PDB/Ensembl/PubMed validator)

### 10. Science Templates & Provenance (5 components)
- `templates/science-provenance/Snakefile.template`
- `templates/science-provenance/dvc.yaml.template`
- `templates/science-provenance/params.yaml.template`
- `templates/science-provenance/provenance_tracker.py`
- `templates/science-provenance/SCIENTIFIC_PROVENANCE_GUIDE.md`

---

## God Nodes / Central Architectural Hubs
1. **`tests/run-audit.cjs`** (Centrality Degree: 17) — Coordinates runtime verification across memory, tasks, hooks, and domain tools.
2. **`scripts/validate_skills.py`** (Centrality Degree: 13) — Validates architectural rules across all 13 modular skills.
3. **`scripts/validate.js`** (Centrality Degree: 8) — CI schema and token budget verification anchor.
4. **`tasks/beads-tracker.cjs`** (Centrality Degree: 6) — Context-resilient task coordination DAG.

---

## Suggested Graph Explorations
* Query 1: *"How does `pre-tool-guard.cjs` intercept and block destructive bash commands before execution?"*
* Query 2: *"What is the dependency chain between `inspect_biofile.py`, `stats_guard.py`, and `provenance_manifest.json` in computational biology pipelines?"*
