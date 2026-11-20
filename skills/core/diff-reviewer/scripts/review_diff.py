#!/usr/bin/env python3
"""
review_diff.py - Automated git diff auditor checking 7 standard vectors
plus optional 8th vector (scientific-integrity).
"""

import sys
import os
import re
import argparse

RULES = [
    # Vector 1: Logic / Currency float
    {
        "id": "V1-FLOAT-MATH",
        "vector": "Logic Correctness",
        "severity": "CRITICAL",
        "pattern": r"\b(price|amount|balance|cost|tax)\s*[\*\/+-]=\s*[\d\.]+",
        "message": "Floating-point arithmetic on currency/balance detected. Use integer minor units or decimal libraries."
    },
    # Vector 2: SQL Injection
    {
        "id": "V2-SQLI",
        "vector": "Security & Injection",
        "severity": "CRITICAL",
        "pattern": r"(SELECT|UPDATE|INSERT|DELETE).*(\$\{.*\}|\+.*req\.|\+.*params)",
        "message": "Possible raw SQL string interpolation. Use parameterized queries."
    },
    # Vector 3: Memory Leaks
    {
        "id": "V3-MEM-LEAK",
        "vector": "Reliability & Memory Leaks",
        "severity": "HIGH",
        "pattern": r"(const|let|var)\s+\w*cache\w*\s*=\s*new\s+(Map|Set)\(\)",
        "message": "Unbounded Map/Set instantiation without TTL or size eviction limit."
    },
    # Vector 7: Speculative TODOs
    {
        "id": "V7-TODO",
        "vector": "Minimalism & SLOC",
        "severity": "LOW",
        "pattern": r"\b(TODO|FIXME|HACK):",
        "message": "Unfinished marker in diff. Complete or eliminate before merging."
    }
]

BIO_RULES = [
    # Vector 8: Scientific Integrity - ML Data Leakage
    {
        "id": "V8-DATA-LEAKAGE",
        "vector": "Scientific Integrity",
        "severity": "CRITICAL",
        "pattern": r"(StandardScaler|MinMaxScaler|SimpleImputer)\(\)\.fit_transform\([A-Za-z0-9_]+\)(?!.*train)",
        "message": "ML Data Leakage: fit_transform applied to whole dataset before train/test splitting."
    },
    # Vector 8: Silent NaN drops
    {
        "id": "V8-SILENT-DROPNA",
        "vector": "Scientific Integrity",
        "severity": "HIGH",
        "pattern": r"\.dropna\(inplace=True\)|\.dropna\(\)(?!.*log)",
        "message": "Silent dropna() removes biological samples or features without logging retained row counts."
    },
    # Vector 8: Hardcoded paths
    {
        "id": "V8-HARDCODED-PATH",
        "vector": "Scientific Integrity",
        "severity": "HIGH",
        "pattern": r"['\"][A-Za-z]:\\[Users|Documents]|['\"]\/home\/[a-zA-Z0-9_-]+\/",
        "message": "Hardcoded local machine path detected. Pipeline will break on cluster nodes or containers."
    },
    # Vector 8: Unit mismatch suspicion
    {
        "id": "V8-UNIT-CONV",
        "vector": "Scientific Integrity",
        "severity": "MEDIUM",
        "pattern": r"(\.distance|\.rmsd|coordinates).*(\*\s*100|\/\s*100)",
        "message": "Suspicious distance multiplier (* 100 or / 100). Verify nm to Angstrom conversion (factor is 10, not 100)."
    }
]

def scan_diff(diff_content: str, is_bio: bool = False):
    findings = []
    active_rules = RULES + (BIO_RULES if is_bio else [])
    
    lines = diff_content.splitlines()
    for line_num, line in enumerate(lines, 1):
        if not line.startswith('+') or line.startswith('+++'):
            continue  # only scan added/modified lines

        added_code = line[1:].strip()
        for rule in active_rules:
            if re.search(rule["pattern"], added_code, re.IGNORECASE):
                findings.append({
                    "line_num": line_num,
                    "code": added_code,
                    **rule
                })
    return findings

def main():
    parser = argparse.ArgumentParser(description="Audit git diff against 7+1 review vectors.")
    parser.add_argument("--diff", required=True, help="Path to git diff or patch file")
    parser.add_argument("--bio", action="store_true", help="Activate Vector 8 (Scientific Integrity)")
    args = parser.parse_args()

    if not os.path.exists(args.diff):
        print(f"[FAIL] Diff file not found: {args.diff}", file=sys.stderr)
        sys.exit(1)

    with open(args.diff, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    findings = scan_diff(content, is_bio=args.bio)

    print("====================================================")
    print(f"DIFF AUDIT RESULTS ({len(findings)} findings)")
    print(f"Scientific Vector 8 Active: {args.bio}")
    print("====================================================\n")

    criticals = [f for f in findings if f["severity"] == "CRITICAL"]
    highs = [f for f in findings if f["severity"] == "HIGH"]

    for f in findings:
        badge = "🔴" if f["severity"] == "CRITICAL" else ("🟠" if f["severity"] == "HIGH" else "🟡")
        print(f"{badge} [{f['severity']}] {f['vector']} ({f['id']}): {f['message']}")
        print(f"    Line in diff: {f['code']}\n")

    if criticals or highs:
        print(f"VERDICT: REJECTED ({len(criticals)} critical, {len(highs)} high)")
        sys.exit(1)
    else:
        print("VERDICT: APPROVED")
        sys.exit(0)

if __name__ == "__main__":
    main()
