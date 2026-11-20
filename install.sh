#!/usr/bin/env bash
# Antigravity Elite Harness POSIX Installer
set -euo pipefail

DRY_RUN=false
PROFILE="full"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --profile=*)
      PROFILE="${1#*=}"
      shift
      ;;
    frontend|bio|comp-bio|all|full)
      PROFILE="$1"
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

TARGET_DIR="${HOME}/.gemini/config"
BACKUP_DIR="${HOME}/.gemini/backup_$(date +%Y%m%d_%H%M%S)"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Antigravity Elite Harness Installer ==="
echo "Source:  ${REPO_DIR}"
echo "Target:  ${TARGET_DIR}"
echo "Profile: ${PROFILE}"

SKILL_SUBDIRS=("core")
case "${PROFILE}" in
  all|full)
    SKILL_SUBDIRS+=("frontend" "comp-bio")
    ;;
  frontend)
    SKILL_SUBDIRS+=("frontend")
    ;;
  bio|comp-bio)
    SKILL_SUBDIRS+=("comp-bio")
    ;;
  *)
    echo "Unknown profile: ${PROFILE}. Expected: frontend, bio, or full."
    exit 1
    ;;
esac

if [ "$DRY_RUN" = true ]; then
  echo "[DRY RUN] Would backup ${TARGET_DIR} -> ${BACKUP_DIR}"
  echo "[DRY RUN] Would copy hooks, rules, memory, tasks, agents, and skills (${SKILL_SUBDIRS[*]})"
  echo "[DRY RUN] Verification would run via tests/run-audit.cjs"
  exit 0
fi

if [ -d "${TARGET_DIR}" ]; then
  echo "Backing up existing configuration to ${BACKUP_DIR}..."
  mkdir -p "${BACKUP_DIR}"
  cp -r "${TARGET_DIR}"/* "${BACKUP_DIR}/" 2>/dev/null || true
fi

mkdir -p "${TARGET_DIR}/hooks" "${TARGET_DIR}/rules" "${TARGET_DIR}/memory" "${TARGET_DIR}/tasks" "${TARGET_DIR}/agents" "${TARGET_DIR}/skills"
cp -r "${REPO_DIR}/hooks/"* "${TARGET_DIR}/hooks/"
cp -r "${REPO_DIR}/rules/"* "${TARGET_DIR}/rules/"
cp -r "${REPO_DIR}/memory/"* "${TARGET_DIR}/memory/"
cp -r "${REPO_DIR}/tasks/"* "${TARGET_DIR}/tasks/"
cp -r "${REPO_DIR}/agents/"* "${TARGET_DIR}/agents/"

for sub in "${SKILL_SUBDIRS[@]}"; do
  src_sub="${REPO_DIR}/skills/${sub}"
  if [ -d "${src_sub}" ]; then
    for skill_path in "${src_sub}"/*; do
      if [ -d "${skill_path}" ]; then
        skill_name="$(basename "${skill_path}")"
        dest_skill="${TARGET_DIR}/skills/${skill_name}"
        mkdir -p "${dest_skill}"
        cp -r "${skill_path}/"* "${dest_skill}/"
        echo "Installed skill: ${skill_name} (from ${sub})"
      fi
    done
  fi
done

cp "${REPO_DIR}/hooks/hooks.json" "${TARGET_DIR}/hooks.json"
cp "${REPO_DIR}/SECURITY_ARCHITECTURE.md" "${TARGET_DIR}/SECURITY_ARCHITECTURE.md"

echo "Running verification..."
node "${REPO_DIR}/tests/run-audit.cjs"
echo "Installation completed successfully with profile '${PROFILE}'."
