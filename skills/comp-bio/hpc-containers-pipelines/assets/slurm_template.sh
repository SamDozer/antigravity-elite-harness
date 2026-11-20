#!/usr/bin/env bash
# ==============================================================================
# Production SLURM Batch Submission Template
# ==============================================================================
#SBATCH --job-name=bio_pipeline
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --mail-type=FAIL
# ==============================================================================

set -euo pipefail

echo "=== JOB STARTED: $(date) ==="
echo "Node:            ${SLURMD_NODENAME}"
echo "Job ID:          ${SLURM_JOB_ID}"
echo "CPUs Allocated:  ${SLURM_CPUS_PER_TASK}"
echo "Memory:          ${SLURM_MEM_PER_NODE:-64G}"

# 1. Staging to Local Scratch Storage
SCRATCH_DIR=$(mktemp -d -p "${TMPDIR:-/scratch}" "job_${SLURM_JOB_ID}_XXXX")
echo "Scratch Directory: ${SCRATCH_DIR}"

# 2. Cleanup Trap
cleanup() {
    local exit_code=$?
    echo "=== CLEANUP TRIGGERED (Exit code: ${exit_code}) ==="
    if [ -d "${SCRATCH_DIR}" ]; then
        rm -rf "${SCRATCH_DIR}"
        echo "Cleaned up scratch: ${SCRATCH_DIR}"
    fi
    echo "=== JOB FINISHED: $(date) ==="
    exit ${exit_code}
}
trap cleanup EXIT INT TERM

# 3. Environment & Modules
# module purge
# module load apptainer/1.2.5

# 4. Pipeline Execution
echo "Executing workload..."
# cp -r inputs/* "${SCRATCH_DIR}/"
# python pipeline.py --workdir "${SCRATCH_DIR}"
# cp "${SCRATCH_DIR}/results.tar.gz" final_output/

echo "Workload completed successfully."
