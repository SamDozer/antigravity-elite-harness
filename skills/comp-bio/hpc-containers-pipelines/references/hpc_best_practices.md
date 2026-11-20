# High-Performance Computing Best Practices

### 1. The I/O Staging Principle
Shared filesystems (NFS, Lustre, GPFS) are designed for large sequential reads/writes, not millions of small random metadata ops.
- Create a localized temporary job directory on compute node SSD:
  ```bash
  SCRATCH_DIR=$(mktemp -d -p "${TMPDIR:-/scratch}" "job_${SLURM_JOB_ID}_XXXX")
  trap 'rm -rf "${SCRATCH_DIR}"' EXIT
  ```
- Copy input files to `${SCRATCH_DIR}`, execute compute locally, and copy final outputs back to shared storage.

### 2. Container Mounting with Apptainer
- Mount host directories explicitly:
  ```bash
  apptainer exec \
    --bind "${SCRATCH_DIR}:/tmp" \
    --bind "${PROJECT_DIR}:/workspace" \
    --nv \
    container.sif python /workspace/pipeline.py
  ```
- Pass `--nv` when requesting GPU nodes.
