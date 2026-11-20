#!/usr/bin/env python3
"""
check_state_coverage.py - Inspects frontend components for interaction state coverage:
Loading, Empty, Error, Focus management, and Accessibility announcements.
"""

import sys
import os
import re
import argparse

PATTERNS = {
    "Loading State": r"(isLoading|loading|Skeleton|Spinner|fallback=)",
    "Empty State": r"(isEmpty|empty|length\s*===?\s*0|no\s+results|NoData)",
    "Error State": r"(isError|error|ErrorBoundary|role=['\"]alert['\"]|catch\()",
    "Accessibility/Focus": r"(aria-live|role=['\"]status['\"]|focus\(\)|tabIndex|:focus-visible|onKeyDown)",
    "Optimistic/Rollback": r"(optimistic|rollback|prevData|previousState)"
}

def check_coverage(file_path: str):
    if not os.path.exists(file_path):
        print(f"[FAIL] Target file not found: {file_path}", file=sys.stderr)
        return False

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    detected = {}
    for state_name, pattern in PATTERNS.items():
        match = re.search(pattern, content, re.IGNORECASE)
        detected[state_name] = bool(match)

    print(f"=== COMPONENT INTERACTION STATE COVERAGE: {os.path.basename(file_path)} ===")
    covered_count = 0
    for state, present in detected.items():
        if present:
            print(f"✅ [COVERED] {state}")
            covered_count += 1
        else:
            print(f"⚠️ [MISSING] {state}")

    # Pass if at least Loading, Empty, and Error are handled
    core_ok = detected["Loading State"] and (detected["Empty State"] or detected["Error State"])
    print(f"\nScore: {covered_count}/{len(PATTERNS)} states detected.")
    print(f"Verdict: {'PASS' if core_ok else 'FAIL (Async views must cover loading and empty/error states)'}")
    return core_ok

def main():
    parser = argparse.ArgumentParser(description="Audit frontend component for state coverage.")
    parser.add_argument("--file", required=True, help="Path to component file (tsx, jsx, vue, svelte, html)")
    args = parser.parse_args()

    success = check_coverage(args.file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
