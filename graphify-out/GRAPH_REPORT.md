# Knowledge Graph Architectural Report: Antigravity Elite Harness

Generated at: 2026-11-26T18:08:03.475Z

## Executive Summary
- **Total Graph Nodes:** 250
- **Total Edges:** 68
- **Detected Functional Communities:** 10

## Functional Communities
### Quality & CI/CD (11 components)
- `.github/pull_request_template.md`
- `.github/workflows/agent-pipeline.yml`
- `templates/ci-cd/.github/workflows/agent-pipeline.yml`
- `templates/ci-cd/pull_request_template.md`
- `templates/ci-cd/semgrep.yml`
- `templates/testing/fast-check.example.ts`
- `templates/testing/hypothesis_example.py`
- `templates/testing/mutmut.ini.template`
- *...and 3 more*

### Observability & Rules (32 components)
- `.gitignore`
- `evals/promptfoo.yaml`
- `observability/local-ports-registry.json`
- `observability/LOCAL_PORTS_DIRECTORY.md`
- `observability/port-guard.ps1`
- `observability/trace-analyzer.cjs`
- `README.md`
- `rules/adaptive-responsive-ui.md`
- *...and 24 more*

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

### Science & Provenance (5 components)
- `templates/science-provenance/dvc.yaml.template`
- `templates/science-provenance/params.yaml.template`
- `templates/science-provenance/provenance_tracker.py`
- `templates/science-provenance/SCIENTIFIC_PROVENANCE_GUIDE.md`
- `templates/science-provenance/Snakefile.template`

### Skills: CompBio (60 components)
- `skills/comp-bio/bio-literature-grounding/assets/verified_identifiers_cache.json`
- `skills/comp-bio/bio-literature-grounding/references/database_apis.md`
- `skills/comp-bio/bio-literature-grounding/scripts/verify_ids.py`
- `skills/comp-bio/bio-literature-grounding/SKILL.md`
- `skills/comp-bio/bio-orchestrator/assets/provenance_manifest.json`
- `skills/comp-bio/bio-orchestrator/references/bio_data_standards.md`
- `skills/comp-bio/bio-orchestrator/scripts/inspect_biofile.py`
- `skills/comp-bio/bio-orchestrator/scripts/__pycache__/inspect_biofile.cpython-314.pyc`
- *...and 52 more*

### Skills: Core (85 components)
- `skills/core/architect-planner/assets/implementation_plan.template.md`
- `skills/core/architect-planner/references/plan_rubric.md`
- `skills/core/architect-planner/scripts/validate_plan.py`
- `skills/core/architect-planner/SKILL.md`
- `skills/core/diff-reviewer/assets/review_report.template.md`
- `skills/core/diff-reviewer/references/review_vectors.md`
- `skills/core/diff-reviewer/scripts/review_diff.py`
- `skills/core/diff-reviewer/scripts/__pycache__/review_diff.cpython-314.pyc`
- *...and 77 more*

### Skills: Frontend (40 components)
- `skills/frontend/app-ui-system/assets/tokens.css`
- `skills/frontend/app-ui-system/references/font-pairings.md`
- `skills/frontend/app-ui-system/references/palettes.md`
- `skills/frontend/app-ui-system/scripts/check_contrast.py`
- `skills/frontend/app-ui-system/SKILL.md`
- `skills/frontend/data-viz-ui/assets/colorblind_palettes.json`
- `skills/frontend/data-viz-ui/references/dataviz_heuristics.md`
- `skills/frontend/data-viz-ui/scripts/export_viz_helper.js`
- *...and 32 more*

## God Nodes / Central Architectural Hubs
- **`tests/run-audit.cjs`** (Centrality Degree: 30)
- **`scripts/validate_skills.py`** (Centrality Degree: 26)
- **`tasks/beads-tracker.cjs`** (Centrality Degree: 4)
- **`hooks/pre-tool-guard.cjs`** (Centrality Degree: 3)
- **`memory/memory-bank.cjs`** (Centrality Degree: 3)
- **`hooks/hooks.json`** (Centrality Degree: 2)

## Suggested Graph Explorations
1. **Trace skills architecture validation:** `scripts/validate_skills.py` -> `skills/frontend/ui-visual-qa/SKILL.md` -> `skills/frontend/ui-visual-qa/scripts/visual_audit.mjs`
2. **Trace biological data governance:** `rules/global-core.md` -> `skills/comp-bio/bio-orchestrator/scripts/inspect_biofile.py` -> `skills/comp-bio/bio-sequence-stats/scripts/stats_guard.py`
3. **Trace 8-vector diff review:** `skills/core/diff-reviewer/scripts/review_diff.py` -> `tests/run-audit.cjs` -> `hooks/pre-tool-guard.cjs`
