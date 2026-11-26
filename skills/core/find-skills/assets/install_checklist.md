# Pre-Install Skill Checklist

Before running `npx skills add <owner/repo@skill> -g -y`:

- [ ] Package spec validated via `scripts/check_skill_source.py --spec <owner/repo@skill>`
- [ ] Source repository checked for stars, activity, and license (`MIT` / `Apache-2.0`)
- [ ] `SKILL.md` and bundled scripts scanned with `skill-audit` (no instruction overrides, pipe-to-shell, or credential reads)
- [ ] Trigger boundaries (`Use when` / `Do NOT use when`) verified not to hijack existing skills
