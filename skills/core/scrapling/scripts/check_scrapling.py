#!/usr/bin/env python3
"""Verifies Scrapling installation, Selector parsing, and safe CLI flags."""
import argparse
import re
import sys


def check_command_safety(cmd: str) -> bool:
    if "scrapling extract" in cmd and "--ai-targeted" not in cmd:
        print("[FAIL] scrapling extract commands must include --ai-targeted for prompt-injection protection.")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Verify Scrapling environment and CLI safety.")
    parser.add_argument("--check-env", action="store_true", help="Verify scrapling package and Selector parsing")
    parser.add_argument("--check-cmd", type=str, help="Validate a scrapling CLI command includes --ai-targeted")
    args = parser.parse_args()

    if args.check_cmd:
        if not check_command_safety(args.check_cmd):
            sys.exit(1)
        print("[PASS] Scrapling CLI command safety check passed.")
        return

    if args.check_env:
        try:
            import scrapling
            from scrapling.parser import Selector
        except ImportError as e:
            print(f"[FAIL] Scrapling not installed: {e}")
            sys.exit(1)

        doc = Selector("<html><body><article><h1>Hello Scrapling</h1></article></body></html>")
        title = doc.css("article h1::text").get()
        if title != "Hello Scrapling":
            print(f"[FAIL] Selector returned unexpected text: {title!r}")
            sys.exit(1)
        print(f"[PASS] Scrapling {scrapling.__version__} installed and Selector parsing verified.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
