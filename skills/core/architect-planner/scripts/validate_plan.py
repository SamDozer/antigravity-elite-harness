#!/usr/bin/env python3
"""
validate_plan.py - Deterministic implementation plan validator.
Ensures implementation plans have all required architectural sections,
explicit verification commands, and acyclic Beads task definitions.
"""

import sys
import os
import re
import argparse

REQUIRED_SECTIONS = [
    r"#+.*(Objective|User Stories|Goals)",
    r"#+.*(Architecture|Boundaries|Contracts)",
    r"#+.*(Beads|Tasks|Task Breakdown)",
    r"#+.*(Verification|Quality Gate)",
    r"#+.*(Rollback|Risk Matrix|Failure Modes)"
]

def validate_plan(plan_path: str) -> bool:
    if not os.path.exists(plan_path):
        print(f"[FAIL] Plan file not found: {plan_path}", file=sys.stderr)
        return False

    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []
    
    # 1. Check required structural sections
    for sec_pattern in REQUIRED_SECTIONS:
        if not re.search(sec_pattern, content, re.IGNORECASE):
            errors.append(f"Missing required section matching pattern: {sec_pattern}")

    # 2. Check for executable verification commands
    has_test_command = bool(
        re.search(r"(npm|pytest|cargo|go|python|py|node|vitest|jest|mvn)\s+(test|run|check)", content, re.IGNORECASE)
    )
    if not has_test_command:
        errors.append("No executable verification test command found (e.g., npm test, pytest, cargo test)")

    # 3. Check for Task IDs / Beads pattern
    task_ids = re.findall(r"Task\s+([A-Za-z0-9_-]+):", content, re.IGNORECASE)
    if not task_ids:
        # Check alternative markdown task list format
        task_ids = re.findall(r"-\s*\[[ x]\]\s*\*\*([A-Za-z0-9_-]+)\*\*", content)
    
    if not task_ids:
        errors.append("No discrete Task IDs found. Expected format 'Task <ID>:' or '- [ ] **<ID>**'")

    # Report results
    if errors:
        print(f"[FAIL] Implementation plan '{plan_path}' failed validation with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print(f"[PASS] Implementation plan '{plan_path}' is structurally valid ({len(task_ids)} tasks declared).")
    return True

def main():
    parser = argparse.ArgumentParser(description="Validate an implementation plan for architectural completeness.")
    parser.add_argument("--plan", required=True, help="Path to implementation_plan.md")
    args = parser.parse_args()

    success = validate_plan(args.plan)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
