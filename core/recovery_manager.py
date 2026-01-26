import os
import json
import shutil
from datetime import datetime

class RecoveryManager:
    def __init__(self, policy_path="policies/security_manifest.json", backup_dir="backups/"):
        self.policy_path = policy_path
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_snapshot(self, trigger_event: str):
        """Creates a timestamped backup before any automated change."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"manifest_{timestamp}_{trigger_event}.json"
        dest = os.path.join(self.backup_dir, snapshot_name)
        
        shutil.copy2(self.policy_path, dest)
        print(f"[💾] Snapshot created: {snapshot_name}")
        return dest

    def rollback_to_last_known_good(self):
        """Finds the most recent backup and restores it."""
        backups = sorted([f for f in os.listdir(self.backup_dir) if f.endswith(".json")])
        if not backups:
            print("[🚨] CRITICAL: No backups found. Manual intervention required!")
            return False

        last_good = os.path.join(self.backup_dir, backups[-1])
        shutil.copy2(last_good, self.policy_path)
        print(f"[⏪] ROLLBACK SUCCESSFUL: Restored {backups[-1]}")
        
        # In a real 2026 setup, you would also trigger a 'system_restart' MCP tool here
        return True

    def lockdown_mode(self):
        """Hard-resets to a 'Deny-All' safety baseline (The Nuclear Option)."""
        baseline = {
            "version": "baseline-0.0.0",
            "active_rules": [{"id": "emergency_stop", "action": "BLOCK", "pattern": ".*"}],
            "status": "LOCKDOWN"
        }
        with open(self.policy_path, "w") as f:
            json.dump(baseline, f, indent=4)
        print("[☢️] SYSTEM LOCKED: All agentic actions suspended.")