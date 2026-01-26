#!/bin/bash
# PAI Emergency Kill-Switch

echo "--- 🚨 PAI EMERGENCY ROLLBACK INITIATED ---"

# 1. Kill any running MCP Servers and the Orchestrator
echo "[1/3] Terminating all PAI processes..."
pkill -f "mcp_red_server.py"
pkill -f "mcp_blue_server.py"
pkill -f "orchestrator.py"

# 2. Run the Python recovery tool to restore manifest
echo "[2/3] Restoring Security Manifest..."
python3 -c "from core.recovery_manager import RecoveryManager; RecoveryManager().rollback_to_last_known_good()"

# 3. Clear transient vector memory (prevent re-infection)
echo "[3/3] Purging temporary memory caches..."
rm -rf memory/temp_cache/*

echo "--- ✅ System Reset to Last Known Good State ---"