# GROMACS Physical Sanity Checklist

Audit GROMACS `.mdp` simulation parameters against physical laws and numerical stability bounds:

| Parameter | Recommended Value | Common LLM Hallucination / Failure Mode |
| :--- | :--- | :--- |
| **`dt` (timestep)** | `0.002` ps (2 fs) | Using `0.004` or `0.005` ps without virtual sites; system blows up in 100 steps. |
| **`constraints`** | `all-bonds` or `h-bonds` with `lincs-iter = 1` | `none` with `dt = 0.002` ps. (If unconstrained, `dt` MUST be `<= 0.001` ps). |
| **`tcoupl` (thermostat)** | `v-rescale` or `nose-hoover` | Using `berendsen` for production runs (does not sample true canonical ensemble). |
| **`pcoupl` (barostat)** | `C-rescale` or `Parrinello-Rahman` | Applying `Parrinello-Rahman` directly to raw, un-equilibrated structure (causes box collapse). |
| **`coulombtype`** | `PME` (Particle Mesh Ewald) | Using `Cut-off` for long-range electrostatics in aqueous macromolecular systems. |
| **`rcoulomb` / `rvdw`** | `1.0` to `1.2` nm | Values smaller than `0.9` nm or larger than half the periodic box width. |
| **`pbc`** | `xyz` | Forgetting PBC or failing to unwrap trajectory before computing RMSD. |
