---
name: find-skills
description: "Discovers and installs open agent skills via npx skills, skills.sh, and agenticskills.io when users ask how to do a task, search for capabilities, or want to extend agent tooling. Use when searching for installable skills, checking skill registries, or installing verified packages with npx skills add. Do NOT use when auditing a suspicious skill's code directly (use skill-audit) or authoring a new skill from scratch (use agent-skill-craft)."
source_repo: vercel-labs/skills
license: MIT
risk: safe
---

# Find Skills

Discover, vet, and install modular agent skills from the open agent skills ecosystem (`skills.sh`, `agenticskills.io`, and GitHub).

## When to Use This Skill

- User asks "how do I do X", "find a skill for X", or "is there a skill that can..."
- User wants to extend agent capabilities with a specialized workflow, tool, or framework skill
- User wants to search `skills.sh` / `agenticskills.io` or run `npx skills find` / `npx skills add`

## Skills CLI (`npx skills`)

- `npx skills find [query] [--owner <owner>]` — Search skills interactively or by keyword
- `npx skills add <owner/repo@skill> -g -y` — Install a skill globally without prompts
- `npx skills update` — Update installed skills
- `npx skills init <name>` — Scaffold a new skill when no match exists

Browse leaderboards and catalogs at `https://skills.sh/` and `https://agenticskills.io/`.

## Mandatory Pre-Install Verification Workflow

1. **Search:** Run `npx skills find <query>` or check `references/skills_ecosystem.md` for trusted sources (`vercel-labs`, `anthropics`, `microsoft`).
2. **Validate Package Spec & Reputation:** Run `scripts/check_skill_source.py --spec <owner/repo@skill>` to verify valid slug format and repository metadata.
3. **Security Audit Before Trusting:** Always pair with `skill-audit` and `assets/install_checklist.md` before installing third-party skills into `~/.gemini/config/skills/`.
4. **Install & Verify:** Run `npx skills add <owner/repo@skill> -g -y` (or integrate into `antigravity-elite-harness` and run `npm run verify`).

## When No Skills Are Found

Acknowledge no existing skill matched, offer to solve the task directly, or offer to scaffold a custom skill with `npx skills init` / `agent-skill-craft`.
