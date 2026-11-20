#!/usr/bin/env python3
"""
validate_slurm.py - Linter and validator for SLURM batch submission scripts.
Enforces resource bounds, logging directives, trap cleanup, and scratch staging.
"""

import sys
import os
import re
import argparse

REQUIRED_DIRECTIVES = [
    (r"#SBATCH\s+(--job-name|-J)\b", "Job name (--job-name / -J)"),
    (r"#SBATCH\s+(--time|-t)\b", "Time limit (--time / -t)"),
    (r"#SBATCH\s+(--mem|--mem-per-cpu)\b", "Memory allocation (--mem / --mem-per-cpu)"),
    (r"#SBATCH\s+(--cpus-per-task|-c)\b", "CPU core allocation (--cpus-per-task / -c)"),
    (r"#SBATCH\s+(--output|-o)\b", "Output log path (--output / -o)"),
    (r"#SBATCH\s+(--error|-e)\b", "Error log path (--error / -e)")
]

def validate_slurm(script_path: str):
    if not os.path.exists(script_path):
        print(f"[FAIL] Script not found: {script_path}", file=sys.stderr)
        return False

    with open(script_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    errors = []
    warnings = []
    passes = []

    # 1. Check Shebang
    if not content.startswith('#!'):
        errors.append("Missing shebang line (expected #!/usr/bin/env bash or #!/bin/bash).")

    # 2. Check Required Directives
    for pattern, desc in REQUIRED_DIRECTIVES:
        if re.search(pattern, content):
            passes.append(f"Declared {desc}")
        else:
            errors.append(f"Missing mandatory directive: {desc}")

    # 3. Check for Scratch Staging ($TMPDIR or /scratch)
    if re.search(r"(\$TMPDIR|\/scratch)", content):
        passes.append("Uses fast scratch storage ($TMPDIR or /scratch)")
    else:
        warnings.append("No scratch directory ($TMPDIR or /scratch) reference found. Shared filesystem may suffer high I/O latency.")

    # 4. Check for Exit Trap
    if re.search(r"trap\s+.*EXIT", content):
        passes.append("Configured bash trap handler for temporary cleanup on EXIT.")
    else:
        warnings.append("No 'trap ... EXIT' cleanup handler found. Abnormal termination may leak scratch disk files.")

    print(f"=== SLURM BATCH SCRIPT AUDIT: {os.path.basename(script_path)} ===")
    for p in passes:
        print(f"✅ [PASS] {p}")
    for w in warnings:
        print(f"⚠️ [WARN] {w}")
    for e in errors:
        print(f"❌ [FAIL] {e}")

    success = len(errors) == 0
    print(f"\nVerdict: {'APPROVED' if success else 'REJECTED'}")
    return success

def main():
    parser = argparse.ArgumentParser(description="Validate SLURM submission script.")
    parser.add_argument("--script", required=True, help="Path to SLURM script (.sh / .sbatch)")
    args = parser.parse_args()

    success = validate_slurm(args.script)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
