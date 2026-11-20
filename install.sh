#!/usr/bin/env bash
# Antigravity Elite Harness POSIX Installer
set -euo pipefail

DRY_RUN=false
for arg in "$@"; do
  if [ "$arg" == "--dry-run" ]; then
    DRY_RUN=true
  fi
done

TARGET_DIR="${HOME}/.gemini/config"
BACKUP_DIR="${HOME}/.gemini/backup_$(date +%Y%m%d_%H%M%S)"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Antigravity Elite Harness Installer ==="
echo "Source: ${REPO_DIR}"
echo "Target: ${TARGET_DIR}"

if [ "$DRY_RUN" = true ]; then
  echo "[DRY RUN] Would backup ${TARGET_DIR} -> ${BACKUP_DIR}"
  echo "[DRY RUN] Would copy hooks, rules, memory, and tasks into ${TARGET_DIR}"
  echo "[DRY RUN] Verification would run via node scripts/validate.js"
  exit 0
fi

if [ -d "${TARGET_DIR}" ]; then
  echo "Backing up existing configuration to ${BACKUP_DIR}..."
  mkdir -p "${BACKUP_DIR}"
  cp -r "${TARGET_DIR}"/* "${BACKUP_DIR}/" 2>/dev/null || true
fi

mkdir -p "${TARGET_DIR}/hooks" "${TARGET_DIR}/rules" "${TARGET_DIR}/memory" "${TARGET_DIR}/tasks" "${TARGET_DIR}/agents"
cp -r "${REPO_DIR}/hooks/"* "${TARGET_DIR}/hooks/"
cp -r "${REPO_DIR}/rules/"* "${TARGET_DIR}/rules/"
cp -r "${REPO_DIR}/memory/"* "${TARGET_DIR}/memory/"
cp -r "${REPO_DIR}/tasks/"* "${TARGET_DIR}/tasks/"
cp -r "${REPO_DIR}/agents/"* "${TARGET_DIR}/agents/"
cp "${REPO_DIR}/hooks/hooks.json" "${TARGET_DIR}/hooks.json"
cp "${REPO_DIR}/SECURITY_ARCHITECTURE.md" "${TARGET_DIR}/SECURITY_ARCHITECTURE.md"

echo "Running verification..."
node "${REPO_DIR}/tests/run-audit.cjs"
echo "Installation completed successfully."
