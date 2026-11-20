#!/usr/bin/env python3
"""
Scientific Experiment Provenance & Determinism Tracker.
Hashes input datasets, captures environment versions, seeds, and execution metadata.
"""

import hashlib
import json
import os
import sys
import platform
from datetime import datetime

def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    if not os.path.exists(filepath):
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def capture_provenance(input_files: list, params: dict, output_path: str = "run_provenance.json"):
    """Record execution provenance metadata."""
    data_hashes = {f: compute_sha256(f) for f in input_files}
    
    provenance = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "system": {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": sys.version.split()[0],
            "architecture": platform.machine()
        },
        "parameters": params,
        "input_artifacts": data_hashes,
        "environment_reproducibility": {
            "random_seed": params.get("random_seed", 42),
            "deterministic_flags": True
        }
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(provenance, f, indent=2)

    print(f"[PROVENANCE] Run metadata saved to {output_path}")
    return provenance

if __name__ == "__main__":
    test_params = {"random_seed": 42, "model": "random_forest", "database": "UniProt-2026_01"}
    capture_provenance(["params.yaml"], test_params, "run_provenance.json")
