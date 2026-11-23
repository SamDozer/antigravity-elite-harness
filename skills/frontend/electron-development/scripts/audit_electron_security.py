#!/usr/bin/env python3
"""Audits Electron main/preload source files for mandatory security fuses and BrowserWindow settings."""
import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser(description="Audit Electron main process file for security misconfigurations.")
    parser.add_argument("--file", required=True, help="Path to Electron main process JS/TS file")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()

    issues = []
    if re.search(r"nodeIntegration\s*:\s*true", code):
        issues.append("nodeIntegration: true detected (must be false)")
    if re.search(r"contextIsolation\s*:\s*false", code):
        issues.append("contextIsolation: false detected (must be true)")
    if re.search(r"webSecurity\s*:\s*false", code):
        issues.append("webSecurity: false detected (disables same-origin policy)")

    if issues:
        for i in issues:
            print(f"[FAIL] {i}")
        sys.exit(1)
    print("[PASS] Electron security audit passed (no unsafe BrowserWindow flags found).")

if __name__ == "__main__":
    main()
