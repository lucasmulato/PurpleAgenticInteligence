#!/bin/bash
# PAI Emergency Kill-Switch
# PAI_DRY_RUN=1 executa apenas a restauração do manifesto em ambiente isolado.
set -euo pipefail

DRY_RUN="${PAI_DRY_RUN:-0}"
POLICY_PATH="${PAI_POLICY_PATH:-policies/security_manifest.json}"
BACKUP_DIR="${PAI_BACKUP_DIR:-backups/}"

echo "--- PAI EMERGENCY ROLLBACK (dry_run=${DRY_RUN}) ---"

if [ "$DRY_RUN" != "1" ]; then
  echo "[1/3] Terminating all PAI processes..."
  pkill -f "mcp_red_server.py" || true
  pkill -f "mcp_blue_server.py" || true
  pkill -f "orchestrator.py" || true
else
  echo "[1/3] DRY RUN: process kill skipped"
fi

echo "[2/3] Restoring Security Manifest..."
PAI_POLICY_PATH="$POLICY_PATH" PAI_BACKUP_DIR="$BACKUP_DIR" \
  python3 -c "from core.recovery_manager import RecoveryManager; raise SystemExit(0 if RecoveryManager().rollback_to_last_known_good() else 1)"

if [ "$DRY_RUN" != "1" ]; then
  echo "[3/3] Purging temporary memory caches..."
  rm -rf memory/temp_cache/*
else
  echo "[3/3] DRY RUN: cache purge skipped"
fi

echo "--- System reset to last known good state ---"
