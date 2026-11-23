#!/usr/bin/env python3
"""Audits an agent claim ledger JSON against required witnesses and evidence refs."""
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Audit agent run claim ledger.")
    parser.add_argument("--ledger", required=True, help="Path to claim ledger JSON")
    args = parser.parse_args()

    with open(args.ledger, "r", encoding="utf-8") as f:
        data = json.load(f)

    claims = data.get("claims", [])
    if not claims:
        print("[FAIL] Empty claim ledger: 0 claims provided.")
        sys.exit(1)

    unproven = []
    for c in claims:
        cid = c.get("claim_id", "UNKNOWN")
        refs = c.get("evidence_refs", [])
        counter = c.get("counterevidence_refs", [])
        if counter:
            c["verdict"] = "contradicted"
            unproven.append((cid, "contradicted"))
        elif not refs:
            c["verdict"] = "not_proven"
            unproven.append((cid, "not_proven"))
        else:
            c["verdict"] = "proven"

    print(f"[AUDIT] Evaluated {len(claims)} claims.")
    if unproven:
        for cid, status in unproven:
            print(f"  [REJECTED] {cid}: {status}")
        sys.exit(1)
    print("[APPROVED] All claims backed by non-contradicted evidence references.")

if __name__ == "__main__":
    main()
