#!/usr/bin/env python3
"""Deterministic structural validator for CLI-Anything agent-harness packages."""
import argparse
import os
import sys


def validate_harness(harness_dir: str) -> list[str]:
    errors = []
    if not os.path.isdir(harness_dir):
        return [f"Harness directory does not exist: {harness_dir}"]

    setup_py = os.path.join(harness_dir, "setup.py")
    if not os.path.isfile(setup_py):
        errors.append("Missing setup.py at agent-harness root.")
    else:
        setup_txt = open(setup_py, encoding="utf-8", errors="replace").read()
        if "find_namespace_packages" not in setup_txt:
            errors.append("setup.py must use find_namespace_packages for PEP 420 cli_anything.* namespace.")

    ns_root = os.path.join(harness_dir, "cli_anything")
    if not os.path.isdir(ns_root):
        errors.append("Missing cli_anything/ namespace directory.")
        return errors

    if os.path.exists(os.path.join(ns_root, "__init__.py")):
        errors.append("cli_anything/__init__.py must NOT exist (PEP 420 namespace package rule).")

    pkgs = [d for d in os.listdir(ns_root) if os.path.isdir(os.path.join(ns_root, d)) and not d.startswith("__")]
    if not pkgs:
        errors.append("No software subpackage found under cli_anything/.")
        return errors

    pkg_dir = os.path.join(ns_root, pkgs[0])
    cli_py = os.path.join(pkg_dir, f"{pkgs[0]}_cli.py")
    if not os.path.isfile(cli_py):
        errors.append(f"Missing main CLI entrypoint: cli_anything/{pkgs[0]}/{pkgs[0]}_cli.py")
    else:
        cli_txt = open(cli_py, encoding="utf-8", errors="replace").read()
        if "--json" not in cli_txt:
            errors.append(f"{pkgs[0]}_cli.py missing mandatory --json machine-readable output flag.")

    test_md = os.path.join(pkg_dir, "tests", "TEST.md")
    if not os.path.isfile(test_md):
        errors.append(f"Missing test plan: cli_anything/{pkgs[0]}/tests/TEST.md")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate a CLI-Anything agent-harness directory.")
    parser.add_argument("--path", required=True, help="Path to <software>/agent-harness")
    args = parser.parse_args()

    errors = validate_harness(args.path)
    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        sys.exit(1)
    print(f"[PASS] CLI-Anything harness structure verified: {args.path}")


if __name__ == "__main__":
    main()
