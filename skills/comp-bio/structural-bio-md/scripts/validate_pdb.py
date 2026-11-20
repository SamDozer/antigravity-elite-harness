#!/usr/bin/env python3
"""
validate_pdb.py - Macromolecular PDB coordinate validator.
Checks chain IDs, alternate conformations (altloc), missing CA backbone atoms,
occupancies, and average B-factors (or AlphaFold pLDDT scores).
"""

import sys
import os
import argparse

def validate_pdb(pdb_path: str, min_plddt: float = None):
    if not os.path.exists(pdb_path):
        print(f"[FAIL] PDB file not found: {pdb_path}", file=sys.stderr)
        return False

    chains = set()
    altlocs = set()
    atom_count = 0
    hetatm_count = 0
    ca_count = 0
    b_factors = []
    zero_occupancy_count = 0

    with open(pdb_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            record = line[0:6].strip()
            if record in ('ATOM', 'HETATM'):
                atom_count += (1 if record == 'ATOM' else 0)
                hetatm_count += (1 if record == 'HETATM' else 0)

                # Chain ID is col 22 (0-indexed 21)
                chain_id = line[21].strip() if len(line) > 21 else ''
                if chain_id:
                    chains.add(chain_id)

                # Altloc is col 17 (0-indexed 16)
                altloc = line[16].strip() if len(line) > 16 else ''
                if altloc:
                    altlocs.add(altloc)

                # Atom name is col 13-16 (0-indexed 12-16)
                atom_name = line[12:16].strip() if len(line) > 15 else ''
                if atom_name == 'CA':
                    ca_count += 1

                # Occupancy is col 55-60 (0-indexed 54-60)
                if len(line) >= 60:
                    try:
                        occ = float(line[54:60].strip())
                        if occ == 0.0:
                            zero_occupancy_count += 1
                    except ValueError:
                        pass

                # B-factor / pLDDT is col 61-66 (0-indexed 60-66)
                if len(line) >= 66:
                    try:
                        bf = float(line[60:66].strip())
                        b_factors.append(bf)
                    except ValueError:
                        pass

    if atom_count == 0:
        print(f"[FAIL] No ATOM records found in {pdb_path}", file=sys.stderr)
        return False

    avg_bfactor = sum(b_factors) / len(b_factors) if b_factors else 0.0
    is_alphafold = len(b_factors) > 0 and all(0.0 <= b <= 100.0 for b in b_factors[:100]) and avg_bfactor > 30.0

    print("====================================================")
    print(f"PDB STRUCTURE AUDIT: {os.path.basename(pdb_path)}")
    print("====================================================")
    print(f"ATOM Records:       {atom_count:,}")
    print(f"HETATM Records:     {hetatm_count:,}")
    print(f"Chains Found:       {sorted(list(chains)) if chains else 'None declared'}")
    print(f"CA Backbone Atoms:  {ca_count:,}")
    print(f"Alternate Confs:    {list(altlocs) if altlocs else 'None (Clean Single Pose)'}")
    print(f"Zero Occupancies:   {zero_occupancy_count}")
    print(f"Average B-Factor:   {avg_bfactor:.2f} ({'Likely AlphaFold pLDDT' if is_alphafold else 'Crystallographic B-factor'})")

    warnings = []
    errors = []

    if is_alphafold and b_factors:
        v_high = sum(1 for b in b_factors if b >= 90.0)
        conf = sum(1 for b in b_factors if 70.0 <= b < 90.0)
        low = sum(1 for b in b_factors if 50.0 <= b < 70.0)
        disordered = sum(1 for b in b_factors if b < 50.0)
        total = len(b_factors)
        print("\nAlphaFold pLDDT Confidence Breakdown:")
        print(f"  Very High (>90):   {v_high:,} atoms ({v_high/total*100:.1f}%)")
        print(f"  Confident (70-90): {conf:,} atoms ({conf/total*100:.1f}%)")
        print(f"  Low (50-70):       {low:,} atoms ({low/total*100:.1f}%)")
        print(f"  Disordered (<50):  {disordered:,} atoms ({disordered/total*100:.1f}%)")

        if disordered / total > 0.3:
            warnings.append(f"{disordered/total*100:.1f}% of residues are predicted disordered (pLDDT < 50). Avoid active-site docking.")

        if min_plddt is not None:
            if avg_bfactor < min_plddt:
                errors.append(f"Structure average pLDDT ({avg_bfactor:.2f}) fails minimum threshold ({min_plddt:.2f}).")
            else:
                print(f"✅ [PASS] Structure average pLDDT ({avg_bfactor:.2f}) satisfies threshold >= {min_plddt:.2f}.")

    if altlocs:
        warnings.append(f"Contains {len(altlocs)} alternate location flags. Strip altlocs before docking.")
    if not chains:
        warnings.append("Missing chain identifier column. Assign chains before multi-chain analysis.")
    if zero_occupancy_count > 0:
        warnings.append(f"{zero_occupancy_count} atoms have 0.00 occupancy.")

    if warnings:
        print("\n⚠️ WARNINGS:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("\n❌ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        print("====================================================")
        print("VERDICT: REJECTED (Failed quality threshold)")
        return False

    print("====================================================")
    print("VERDICT: PASS (Coordinates parsed successfully)")
    return True

def main():
    parser = argparse.ArgumentParser(description="Audit PDB coordinate file for structural anomalies and pLDDT confidence.")
    parser.add_argument("--pdb", required=True, help="Path to PDB file")
    parser.add_argument("--min-plddt", type=float, default=None, help="Minimum acceptable average pLDDT score")
    args = parser.parse_args()

    success = validate_pdb(args.pdb, min_plddt=args.min_plddt)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
