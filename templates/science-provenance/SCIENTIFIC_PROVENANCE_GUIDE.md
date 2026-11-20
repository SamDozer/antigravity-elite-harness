# Scientific Reproducibility & Experiment Provenance Guide

## 1. Core Principles of Computational Science in AI
In computational biology, cheminformatics, and machine learning, an experiment that cannot be reproduced is not scientific. AI coding agents often introduce hidden nondeterminism:
- Floating-point discrepancies across OS platforms.
- Unfixed random seeds (`random.random()`, `numpy.random`).
- Dynamic remote API changes (unversioned database queries).
- Untracked raw datasets.

---

## 2. Mandatory Provenance Protocol

Every scientific workflow executed by Antigravity must enforce:
1. **Explicit Version Pinning:** Always state database releases (e.g. `UniProt 2026_01`, `ChEMBL 33`, `PDB release 2026`).
2. **Fixed Random Seeds:** Set seeds at script initialization (`random_seed: 42`).
3. **Cryptographic Artifact Hashing:** All input FASTA files, SMILES tables, and feature tensors must have their SHA-256 hashes recorded via `provenance_tracker.py`.
4. **Pipeline Chaining:** Use `Snakemake` or `DVC` so intermediate data transformations are cached, verified, and replayable.
