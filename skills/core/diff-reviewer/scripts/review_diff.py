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
        "pattern": r"(?:SELECT|UPDATE|INSERT|DELETE).*(?:\$\{.*\}|\+.*(?:req\.|params|input|userId|user_id)|f['\"].*\{[a-zA-Z0-9_]+\})",
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
        "pattern": r"(?:StandardScaler|MinMaxScaler|RobustScaler|SimpleImputer|SelectKBest|PCA)\(\)\.fit(?:_transform)?\((?!\s*(?:X_|df_)?train\b)[A-Za-z0-9_.]+\)",
        "message": "ML Data Leakage: fit/fit_transform applied across dataset without restricting to training split."
    },
    # Vector 8: Silent NaN drops
    {
        "id": "V8-SILENT-DROPNA",
        "vector": "Scientific Integrity",
        "severity": "HIGH",
        "pattern": r"\.dropna\([^)]*\)(?!.*(?:log|print|len))",
        "message": "Silent dropna() removes biological samples or features without logging retained row counts."
    },
    # Vector 8: Hardcoded paths
    {
        "id": "V8-HARDCODED-PATH",
        "vector": "Scientific Integrity",
        "severity": "HIGH",
        "pattern": r"['\"][A-Za-z]:[\\/]+(?:Users|Documents|home)[\\/]|['\"]/(?:home|Users)/[a-zA-Z0-9_.-]+/",
        "message": "Hardcoded local machine path detected. Pipeline will break on cluster nodes or containers."
    },
    # Vector 8: Unpinned dependencies
    {
        "id": "V8-UNPINNED-DEP",
        "vector": "Scientific Integrity",
        "severity": "HIGH",
        "pattern": r"(?:pip\s+install|conda\s+install)\s+[a-zA-Z0-9_-]+(?:\s*$|\s+&&)(?![=<>])|RUN\s+pip\s+install\s+[a-zA-Z0-9_-]+(?:\s*$|\s+&&)(?![=<>])",
        "message": "Unpinned dependency installation detected. Pin exact versions for reproducible container/HPC runs."
    },
    # Vector 8: Unit mismatch - Distance (nm vs Angstrom)
    {
        "id": "V8-UNIT-DIST",
        "vector": "Scientific Integrity",
        "severity": "MEDIUM",
        "pattern": r"(\.distance|\.rmsd|coordinates).*(\*\s*100\b|\/\s*100\b)",
        "message": "Suspicious distance multiplier (* 100 or / 100). Verify nm to Angstrom conversion (factor is 10, not 100)."
    },
    # Vector 8: Unit mismatch - Energy (kJ/mol vs kcal/mol)
    {
        "id": "V8-UNIT-ENERGY",
        "vector": "Scientific Integrity",
        "severity": "MEDIUM",
        "pattern": r"(?:kcal|kJ|kj|free_energy|delta_g|potential).*[\*\/]\s*(?:1000\b|4\.2\b|4\.184\b)",
        "message": "Energy conversion detected. Verify 1 kcal = 4.184 kJ factor and unit consistency (kJ/mol vs. kcal/mol)."
    },
    # Vector 8: Unit mismatch - Log2 vs Natural Log in fold-change
    {
        "id": "V8-UNIT-LOG",
        "vector": "Scientific Integrity",
        "severity": "HIGH",
        "pattern": r"\b(?:log2fc|fold_change|log_fc|lfc)\s*=\s*.*np\.log\(",
        "message": "Natural log np.log() used for fold change calculation instead of base-2 np.log2()."
    },
    # Vector 8: Indexing & Silent Broadcasting
    {
        "id": "V8-BROADCASTING",
        "vector": "Scientific Integrity",
        "severity": "MEDIUM",
        "pattern": r"\.reshape\(-1,\s*1\)(?!.*assert)",
        "message": "Unchecked array reshape(-1, 1). Verify dimension compatibility to prevent silent broadcasting errors."
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
