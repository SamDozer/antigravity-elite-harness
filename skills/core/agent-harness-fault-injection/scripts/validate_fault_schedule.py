#!/usr/bin/env python3
"""Validates a deterministic fault injection schedule JSON for agent harness recovery testing."""
import argparse
import json
import sys

VALID_KINDS = {"timeout", "restart", "partial_failure", "sandbox_denial", "stale_checkpoint", "memory_loss"}

def main():
    parser = argparse.ArgumentParser(description="Validate fault injection schedule.")
    parser.add_argument("--schedule", required=True, help="Path to fault schedule JSON")
    args = parser.parse_args()

    with open(args.schedule, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("seed"):
        print("[FAIL] Fault schedule missing deterministic 'seed'.")
        sys.exit(1)

    faults = data.get("faults", [])
    if not faults:
        print("[FAIL] Fault schedule contains 0 faults.")
        sys.exit(1)

    for idx, fault in enumerate(faults):
        kind = fault.get("kind")
        ordinal = fault.get("ordinal")
        if kind not in VALID_KINDS:
            print(f"[FAIL] Fault #{idx} has unsupported kind '{kind}'.")
            sys.exit(1)
        if not isinstance(ordinal, int) or ordinal < 1:
            print(f"[FAIL] Fault #{idx} must specify positive integer 'ordinal'.")
            sys.exit(1)

    print(f"[PASS] Fault schedule verified (seed={data['seed']}, faults={len(faults)}).")

if __name__ == "__main__":
    main()
