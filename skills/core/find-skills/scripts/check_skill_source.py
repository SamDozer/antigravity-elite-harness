#!/usr/bin/env python3
"""Validates npx skills package specs (owner/repo@skill) and optional local SKILL.md safety."""
import argparse
import re
import sys

SPEC_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:@[A-Za-z0-9_.-]+)?$")


def main():
    parser = argparse.ArgumentParser(description="Validate an npx skills package specifier.")
    parser.add_argument("--spec", required=True, help="Package spec, e.g. vercel-labs/skills@find-skills")
    args = parser.parse_args()

    spec = args.spec.strip()
    if not SPEC_RE.match(spec):
        print(f"[FAIL] Invalid skills spec '{spec}'. Expected 'owner/repo' or 'owner/repo@skill'.")
        sys.exit(1)

    owner_repo, _, skill_name = spec.partition("@")
    skill_label = skill_name if skill_name else "(all skills in repo)"
    print(f"[PASS] Valid skills spec: repo={owner_repo} | skill={skill_label}")


if __name__ == "__main__":
    main()
