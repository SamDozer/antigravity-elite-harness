---
name: cli-anything
description: "Turns any GUI desktop application, web app, or source repository into an agent-native Python CLI harness with Click subcommands, --json output, interactive REPL (ReplSkin), unit/E2E tests, and CLI-Hub discovery. Use when building, refining, testing, validating, or discovering CLI-Anything harnesses for existing software. Do NOT use when building standalone web UIs, Electron renderers from scratch, or running general git/CI tasks."
source_repo: HKUDS/CLI-Anything
license: Apache-2.0
risk: safe
---

# CLI-Anything: Making All Software Agent-Native

Build stateful, agent-ready Python CLIs (`cli-anything-<software>`) for any GUI or desktop application, or discover and install pre-built harnesses via CLI-Hub.

## Read the Full Methodology First

Before writing code, consult the vendored methodology in `references/`:

1. Read `references/HARNESS.md` for the complete 7-phase SOP (Codebase Analysis → Architecture → Implementation → `TEST.md` Planning → Test Implementation → Packaging → `SKILL.md` Generation).
2. Read the matching command mode under `references/commands/`:
   - `references/commands/cli-anything.md` — Build a new CLI harness
   - `references/commands/refine.md` — Expand an existing harness
   - `references/commands/test.md` — Run real-backend unit + E2E tests
   - `references/commands/validate.md` — Run the full validation checklist
   - `references/commands/list.md` — Discover installed/generated harnesses
3. Load `references/guides/` on demand (`session-locking.md`, `mcp-backend.md`, `preview-methodology.md`, `skill-generation.md`, `auto-save-dry-run.md`, `pypi-publishing.md`).
4. To discover or install pre-built CLIs (`pip install cli-anything-hub`), read `references/cli-hub.md`.

## Required Harness Structure

```text
<software>/
└── agent-harness/
    ├── <SOFTWARE>.md
    ├── setup.py                  # PEP 420 namespace package: cli_anything.<software>
    └── cli_anything/
        └── <software>/
            ├── README.md
            ├── __init__.py       # Optional if namespace package
            ├── __main__.py
            ├── <software>_cli.py # Click group with --json & default REPL
            ├── core/             # Data model, session, undo/redo
            ├── utils/            # Backend wrapper + scripts/repl_skin.py
            ├── skills/SKILL.md   # Generated via scripts/skill_generator.py
            └── tests/            # TEST.md + test_core.py + test_full_e2e.py
```

## Non-Negotiable Rules

- **Dual Output Mode:** Every command must support both human-readable output and `--json` machine-readable output.
- **Default REPL:** Invoking `cli-anything-<software>` with no subcommand must enter the interactive REPL using `scripts/repl_skin.py`.
- **Real Backend Integration:** Never mock away the target software in E2E tests; invoke the real binary or fail loudly with install instructions.
- **Namespace Packaging:** Use PEP 420 `find_namespace_packages(include=['cli_anything.*'])` in `setup.py` with no `cli_anything/__init__.py`.
- **Template & Skill Generation:** Generate the target CLI's `SKILL.md` using `scripts/skill_generator.py` and `assets/SKILL.md.template`.

## Deterministic Verification

Before declaring a CLI-Anything harness complete, run the structural validator:

```bash
python scripts/validate_harness.py --path <software>/agent-harness
```
