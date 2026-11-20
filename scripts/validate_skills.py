#!/usr/bin/env python3
"""
validate_skills.py - CI Gate & Validator for Antigravity Progressive Skills Architecture.
Audits:
1. Frontmatter validity (name, description).
2. Explicit trigger boundaries (must contain both 'Use when' and 'Do NOT use when').
3. Line count limit (SKILL.md <= 350 lines).
4. 4-layer architecture compliance (SKILL.md, scripts/, references/, assets/).
5. Internal relative link / referenced path resolution (no broken references).
6. Token/context budget (< 15 KB).
"""

import sys
import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKILLS_DIR = os.path.join(REPO_ROOT, 'skills')

def parse_frontmatter(content: str):
    """Extracts yaml frontmatter dict from file content, supporting multiline strings."""
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", content)
    if not match:
        return None
    fm_text = match.group(1)
    fm = {}
    current_key = None
    for line in fm_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if ':' in line and not line.startswith(' '):
            parts = line.split(':', 1)
            current_key = parts[0].strip()
            val = parts[1].strip()
            if val in ('>', '|'):
                val = ''
            fm[current_key] = val
        elif current_key:
            fm[current_key] = (fm[current_key] + ' ' + stripped).strip()
    return fm

def audit_skill(skill_dir: str):
    skill_name = os.path.basename(skill_dir)
    skill_file = os.path.join(skill_dir, 'SKILL.md')

    errors = []
    warnings = []

    if not os.path.exists(skill_file):
        return [f"Missing SKILL.md in {skill_dir}"]

    with open(skill_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        lines = content.splitlines()

    # 1. Line count check (<= 350 lines)
    if len(lines) > 350:
        errors.append(f"SKILL.md has {len(lines)} lines (budget limit: <= 350 lines). Move deep reference material into references/.")

    # 2. File size check (< 15 KB)
    size_kb = len(content.encode('utf-8')) / 1024
    if size_kb > 15.0:
        errors.append(f"SKILL.md size is {size_kb:.2f} KB (budget limit: <= 15 KB).")

    # 3. YAML Frontmatter check
    fm = parse_frontmatter(content)
    if not fm:
        errors.append("Missing or malformed YAML frontmatter (expected opening and closing '---').")
    else:
        name = fm.get('name')
        desc = fm.get('description', '')

        if not name:
            errors.append("Frontmatter missing 'name' property.")
        elif name != skill_name:
            warnings.append(f"Frontmatter name '{name}' does not match directory name '{skill_name}'.")

        if not desc:
            errors.append("Frontmatter missing 'description' property.")
        else:
            # 4. Trigger boundaries check
            has_use_when = bool(re.search(r"\buse\s+when\b", desc, re.IGNORECASE))
            has_do_not_use = bool(re.search(r"\bdo\s+not\s+use\b|\bdon't\s+use\b", desc, re.IGNORECASE))

            if not has_use_when:
                errors.append("Description missing explicit 'Use when...' trigger boundary.")
            if not has_do_not_use:
                errors.append("Description missing explicit 'Do NOT use when...' anti-trigger boundary.")

    # 5. Four-Layer Directory Checks
    scripts_dir = os.path.join(skill_dir, 'scripts')
    refs_dir = os.path.join(skill_dir, 'references')
    assets_dir = os.path.join(skill_dir, 'assets')

    has_scripts = os.path.exists(scripts_dir) and len(os.listdir(scripts_dir)) > 0
    has_refs = os.path.exists(refs_dir) and len(os.listdir(refs_dir)) > 0
    has_assets = os.path.exists(assets_dir) and len(os.listdir(assets_dir)) > 0

    if not has_scripts:
        warnings.append(f"Missing or empty scripts/ directory in {skill_name}")
    if not has_refs:
        warnings.append(f"Missing or empty references/ directory in {skill_name}")
    if not has_assets:
        warnings.append(f"Missing or empty assets/ directory in {skill_name}")

    # 6. Check internal referenced paths
    # Look for patterns like scripts/foo.py, references/bar.md, assets/baz.css
    ref_matches = re.findall(r"['\"`\s]((?:scripts|references|assets)\/[a-zA-Z0-9_\-\.]+)", content)
    for ref_path in set(ref_matches):
        full_target = os.path.join(skill_dir, ref_path.replace('/', os.sep))
        if not os.path.exists(full_target):
            errors.append(f"Broken internal reference in SKILL.md: '{ref_path}' does not exist on disk.")

    return errors, warnings

def main():
    print("====================================================")
    print("ANTIGRAVITY SKILLS ARCHITECTURE CI VALIDATOR")
    print("====================================================\n")

    if not os.path.exists(SKILLS_DIR):
        print(f"❌ [FAIL] Skills directory not found at {SKILLS_DIR}", file=sys.stderr)
        sys.exit(1)

    skill_dirs = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        if 'SKILL.md' in files:
            skill_dirs.append(root)

    print(f"Discovered {len(skill_dirs)} skills to validate across {SKILLS_DIR}\n")

    total_errors = 0
    total_warnings = 0

    for sdir in sorted(skill_dirs):
        rel_path = os.path.relpath(sdir, REPO_ROOT)
        errors, warnings = audit_skill(sdir)

        if not errors:
            status = "✅ PASS"
            if warnings:
                status += f" (with {len(warnings)} warning(s))"
            print(f"{status}: {rel_path}")
            for w in warnings:
                print(f"    ⚠️  [WARN] {w}")
        else:
            print(f"❌ FAIL: {rel_path}")
            for e in errors:
                print(f"    🔴 [ERROR] {e}")
            for w in warnings:
                print(f"    ⚠️  [WARN] {w}")

        total_errors += len(errors)
        total_warnings += len(warnings)

    print("\n====================================================")
    print(f"SKILLS VALIDATION SUMMARY: {len(skill_dirs)} skills audited")
    print(f"Errors: {total_errors} | Warnings: {total_warnings}")
    print("====================================================")

    if total_errors > 0:
        print("❌ VALIDATION FAILED. Fix errors before committing.", file=sys.stderr)
        sys.exit(1)
    else:
        print("🎉 ALL SKILLS SATISFY CLAUDE-GRADE ARCHITECTURE GATES!")
        sys.exit(0)

if __name__ == "__main__":
    main()
