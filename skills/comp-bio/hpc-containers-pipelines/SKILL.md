---
name: hpc-containers-pipelines
description: HPC cluster deployment, SLURM batch job validation, and containerized workflow orchestration (Nextflow, Snakemake, Apptainer/Singularity, Docker). Use when configuring SLURM submission scripts, containerizing scientific pipelines, staging I/O to local node scratch disks, configuring GPU/CPU resource limits, and writing checkpointable cluster pipelines. Do NOT use when designing web UI frontend components or performing small local data explorations on toy files.
---

# HPC Containers & Pipelines Skill

Turn fragile one-off lab scripts into reproducible, containerized, and cluster-ready workflows for SLURM, Nextflow, and Snakemake.

## Core Rules

1. **Explicit SLURM Resource Guarantees:** Every batch job MUST declare explicit runtime limits (`--time`), memory allocations (`--mem` or `--mem-per-cpu`), CPU cores (`--cpus-per-task`), and partitioned output logs (`--output`, `--error`).
2. **Scratch Disk I/O Staging:** Heavy I/O operations (reading millions of FASTQ reads or writing intermediate BAMs) must stage data to local node scratch (`$TMPDIR` or `/scratch/$SLURM_JOB_ID`) rather than hammering the shared network filesystem (NFS/Lustre).
3. **Trap Handlers for Scratch Cleanup:** Every submission script must set a bash trap to clean up temporary scratch files on abnormal exit or job cancellation.
4. **Pinned Container Environments:** Package all dependencies into an Apptainer/Singularity definition file (`Singularity.def`) or pinned `conda-lock.yml` / `uv` lockfile. Never rely on the host cluster's default unpinned system Python.
5. **Resume & Checkpointing:** Long pipelines must support incremental resumption (`nextflow run -resume` or `snakemake --rerun-incomplete`).

## Workflow

### 1. Template Adaptation
- Copy the production SLURM submission template from `assets/slurm_template.sh`.
- Adjust partition, time limit, and memory to match your actual compute requirements.

### 2. Automated SLURM Script Validation
- Validate the script before submission with `scripts/validate_slurm.py`:
  ```bash
  python skills/comp-bio/hpc-containers-pipelines/scripts/validate_slurm.py --script assets/slurm_template.sh
  ```

### 3. Container Staging
- Bind fast scratch storage when executing Singularity / Apptainer containers:
  ```bash
  apptainer exec --bind $TMPDIR:/tmp,data/:/data workflow.sif python script.py
  ```

## Hard Constraints
- Submitting SLURM jobs without memory and time limits is strictly prohibited.
- Never write intermediate pipeline temp files directly into shared home directories.
