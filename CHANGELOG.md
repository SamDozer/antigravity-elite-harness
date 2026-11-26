# Changelog

All notable changes to this project will be documented in this file.

## [1.4.0] - 2026-11-26
### Added
- **`scrapling` 4-Layer Core Skill (from `D4Vinci/Scrapling`):** Default web scraping framework with `--ai-targeted` prompt-injection protection, `check_scrapling.py` verifier, 18 domain references (`fetching/`, `parsing/`, `spiders/`), and Python starter examples.
- **Scraping-First Operational Rule (`rules/global-core.md`):** Mandates using `scrapling` whenever scraping or extracting data from websites.
- **Verification Coverage:** Added `check_scrapling.py` check to `tests/run-audit.cjs` (26/26 modular skills passing 4-layer CI gates).

## [1.3.0] - 2026-11-26
### Added
- **`find-skills` 4-Layer Core Skill (from `vercel-labs/skills`):** Integrates `npx skills`, `skills.sh`, and `agenticskills.io` discovery with `scripts/check_skill_source.py` slug validation, `references/skills_ecosystem.md`, and `assets/install_checklist.md` paired with `skill-audit`.
- **Verification Coverage:** Added `check_skill_source.py` check to `tests/run-audit.cjs` (25/25 modular skills passing 4-layer CI gates).

## [1.2.0] - 2026-11-26
### Added
- **`cli-anything` 4-Layer Core Skill (from `HKUDS/CLI-Anything`):** Full 7-phase GUI-to-CLI harness methodology (`HARNESS.md`, 5 command modes, 8 implementation guides, `cli-hub.md` discovery), bundled Python stdlib tools (`repl_skin.py`, `preview_bundle.py`, `skill_generator.py`, `validate_harness.py`), and `SKILL.md.template` asset.
- **Verification Coverage:** Added `validate_harness.py` runtime check to `tests/run-audit.cjs` (24/24 modular skills passing 4-layer CI gates).

## [1.1.0] - 2026-11-23
### Added
- **10 Audited Skills from `sickn33/agentic-awesome-skills` (Upgraded to 4-Layer Architecture):**
  - **Core Agent Engineering (+4):** `break-ai-fix-loops` (`fingerprint.py`), `audit-agent-run-evidence` (`audit_evidence.py`), `agent-harness-fault-injection` (`validate_fault_schedule.py`), and `review-multi-agent-orchestration` (`check_orchestration_dag.py`).
  - **Frontend, Desktop & Browser QA (+3):** `electron-development` (`audit_electron_security.py` + `preload.template.ts`), `ghost-qa` (`check_responsive_css.py` + 8-trap viewport matrix), and `tailwind-design-system` (`audit_tailwind_tokens.py` + `tokens.tailwind.css`).
  - **Computational Biology & Scientific Reasoning (+3):** `biopython` (`seq_stats.py` N50/GC% calculator + 8 domain references), `scanpy` (`qc_analysis.py` single-cell AnnData `.h5ad` workflow), and `falsify` (`score_ledger.py` Bayesian posterior & Brier score calculator).
- **Expanded Runtime Audit Suite (`tests/run-audit.cjs`):** Added Suite #7 verifying deterministic CLI scripts across all newly integrated skills (7/7 suites, 23/23 skills passing).

## [1.0.0] - 2026-11-20
### Added
- **Three-Tier Security Architecture:** Formal separation of Lifecycle Hooks (Tier 1), Workspace Sandbox (Tier 2), and Docker cgroups boundaries (Tier 3).
- **Persistent Intelligent Memory Bank:** Local zero-API TF-IDF memory store (`memory-bank.cjs`) with two-way `gotchas.md` synchronization.
- **Beads DAG Task Scheduler:** Context-resilient Directed Acyclic Graph engine (`beads-tracker.cjs`) with automated dependency resolution.
- **Role-Based Agent Boundaries (RBAB):** 8 specialized subagent definitions with strict permission matrices.
- **Scientific Reproducibility Layer:** Snakemake pipeline, DVC data tracking, parameter pinning, and SHA-256 data hasher (`provenance_tracker.py`).
- **Advanced Testing Templates:** Stryker mutation configuration ($ge 75%$ kill rate) and `fast-check` / `hypothesis` property-based test suites.
- **Antigravity Plugin Manifest:** Official `plugin.json` enabling native `agy plugin install .`.
- **Cross-Platform Safe Installers:** POSIX `install.sh` and PowerShell `install.ps1` with `--dry-run` and automated configuration backup.
