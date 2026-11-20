---
name: structural-bio-md
description: Structural biology, macromolecular docking, and molecular dynamics simulation guard. Use when modeling protein structures, verifying PDB/mmCIF coordinates, preparing ligands/receptors for docking, configuring GROMACS .mdp simulations, performing PBC unwrapping on MD trajectories, and analyzing AlphaFold pLDDT/PAE metrics. Do NOT use when performing differential gene expression, analyzing tabular RNA-seq counts (use bio-sequence-stats instead), or writing web UI components.
---

# Structural Biology & Molecular Dynamics Skill

Guard against physical and computational pitfalls in protein modeling, docking, and molecular dynamics (GROMACS, BioPython, MDAnalysis).

## Non-Negotiable Physical Rules

1. **PDB Inspection Before Docking:** Never run molecular docking (AutoDock Vina, Smina, GNINA) on raw downloaded PDBs without:
   - Removing alternate conformations (altlocs).
   - Adding missing hydrogens at physiological pH (7.4) via PROPKA / pdb2pqr.
   - Removing water molecules (unless structural catalytic waters are explicitly conserved).
   - Validating coordinates with `scripts/validate_pdb.py`.
2. **PBC Trajectory Unwrapping:** Before computing RMSD, RMSF, radius of gyration (Rg), or SASA across an MD trajectory, you MUST unwrap and center the periodic boundary conditions (PBC). Analyzing raw folded trajectories yields artificial multi-nanometer jumps.
   ```bash
   # Centering & unwrapping in GROMACS
   gmx trjconv -s topol.tpr -f traj.xtc -o traj_centered.xtc -center -pbc mol -ur compact
   ```
3. **GROMACS .mdp Physical Sanity:**
   - 2 fs timestep (`dt = 0.002`) strictly requires `constraints = all-bonds` or `h-bonds` with LINCS.
   - Never use the Parrinello-Rahman barostat in initial NVT or early NPT equilibration (leads to violent pressure crashes). Use Berendsen or C-rescale, then switch to Parrinello-Rahman for production.
4. **AlphaFold Confidence Thresholds:**
   - Residues with pLDDT < 50 are unstructured/disordered; never build active-site docking hypotheses on them.
   - Domain-domain orientations require low Predicted Aligned Error (PAE < 5 Å).

## Workflow
1. Validate incoming coordinate file:
   ```bash
   python skills/comp-bio/structural-bio-md/scripts/validate_pdb.py --pdb protein.pdb
   ```
2. Verify GROMACS simulation parameters against `references/gromacs-sanity-checks.md`.
3. Use validated `.mdp` template from `assets/sample_nvt.mdp`.

## Hard Constraints
- Calculating RMSD on raw, un-centered trajectories is an automatic failure.
- Never model missing loops without energy minimization.
