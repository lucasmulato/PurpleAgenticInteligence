"""Fase 2: modo de autonomia, trava de patches, política executável e rollback."""
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from core.autonomy import load_mode
from core.patch_control import PatchController
from core.policy_patch import render_safe_ai_policy, write_safe_ai_policy
from core.recovery_manager import RecoveryManager

ROOT = Path(__file__).resolve().parents[1]
FIXED = datetime(2026, 11, 24, 12, 0, tzinfo=timezone.utc)


def test_default_mode_is_propose_only():
    with tempfile.TemporaryDirectory() as tmp:
        assert load_mode(str(Path(tmp) / "missing.yaml")) == "propose_only"
        cfg = Path(tmp) / "autonomy.yaml"
        cfg.write_text("autonomy: auto\n", encoding="utf-8")
        assert load_mode(str(cfg)) == "auto"
        cfg.write_text("autonomy: bogus\n", encoding="utf-8")
        assert load_mode(str(cfg)) == "propose_only"


def test_patch_depth_lock_and_24h_window():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = str(Path(tmp) / "ledger.jsonl")
        controller = PatchController(ledger, max_per_24h=2, now_fn=lambda: FIXED)
        assert controller.can_patch()[0] is True
        controller.record("patch-1")
        controller.record("patch-2")
        assert controller.can_patch()[0] is False
        try:
            controller.record("patch-3")
            raise AssertionError("trava não funcionou")
        except RuntimeError:
            pass

        old = (FIXED - timedelta(hours=25)).isoformat()
        Path(ledger).write_text(
            json.dumps({"id": "old", "timestamp": old}) + "\n", encoding="utf-8"
        )
        assert controller.can_patch()[0] is True


def test_policy_is_loadable_by_safe_ai_shape():
    patch = {"id": "p1", "action": "BLOCK", "commands": ["curl", "wget"]}
    text = render_safe_ai_policy(patch)
    parsed = yaml.safe_load(text)
    assert set(parsed) == {"permit", "ask_human", "reject"}
    assert parsed["reject"] == ["curl", "wget"]
    assert parsed["permit"] == []


def test_policy_file_is_written():
    with tempfile.TemporaryDirectory() as tmp:
        target = write_safe_ai_policy(
            {"id": "p2", "action": "FLAG", "commands": ["rm"]},
            str(Path(tmp) / "nested" / "policy.yaml"),
        )
        assert target.exists()
        assert yaml.safe_load(target.read_text())["ask_human"] == ["rm"]


def test_rollback_dry_run_restores_manifest_in_disposable_dir():
    with tempfile.TemporaryDirectory() as tmp:
        policy = Path(tmp) / "manifest.json"
        policy.write_text('{"version": "original"}', encoding="utf-8")
        backups = Path(tmp) / "backups"
        original = {"version": "original"}
        RecoveryManager(str(policy), str(backups)).create_snapshot("test")
        policy.write_text('{"version": "tampered"}', encoding="utf-8")

        env = dict(os.environ)
        env.update(
            {
                "PAI_DRY_RUN": "1",
                "PAI_POLICY_PATH": str(policy),
                "PAI_BACKUP_DIR": str(backups),
                "PYTHONPATH": str(ROOT),
            }
        )
        result = subprocess.run(
            ["bash", str(ROOT / "rollback.sh")],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
        assert "DRY RUN" in result.stdout
        assert json.loads(policy.read_text()) == original
        assert (backups / "manifest_").exists() or any(backups.iterdir())


def test_orchestrator_default_does_not_write_policy():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = Path(tmp) / "autonomy.yaml"
        cfg.write_text("autonomy: propose_only\n", encoding="utf-8")
        env = dict(os.environ)
        env.update(
            {
                "PAI_AUTONOMY_CONFIG": str(cfg),
                "PAI_PATCH_LEDGER": str(Path(tmp) / "ledger.jsonl"),
                "PYTHONPATH": str(ROOT),
            }
        )
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import asyncio; from core.orchestrator import PurpleOrchestrator; "
                "asyncio.run(PurpleOrchestrator().run_self_healing_loop())",
            ],
            cwd=tmp,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
        assert "propose_only" in result.stdout
        assert not (Path(tmp) / "drafts").exists()
