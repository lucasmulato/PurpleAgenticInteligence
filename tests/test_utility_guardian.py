import pytest
from core.utility_guardian import KAREN_GOLDEN_TASKS, UtilityGuardian


@pytest.fixture
def guardian():
    return UtilityGuardian(epsilon=10, latency_limit_ms=1200)


@pytest.mark.asyncio
async def test_golden_baseline_has_ten_real_karen_tasks(guardian):
    assert len(guardian.golden_dataset) == 10
    assert len(KAREN_GOLDEN_TASKS) == 10
    tools = {task["tool"] for task in guardian.golden_dataset}
    assert {"find_leads", "eva_brief", "decision_log", "key_status"} <= tools


@pytest.mark.asyncio
async def test_approved_patch_keeps_utility(guardian):
    result = await guardian.validate_patch(
        {"id": "safe", "action": "BLOCK", "commands": ["curl"], "blocks": []}, None
    )
    assert result["status"] == "APPROVED"
    assert result["utility"] == 100
    assert result["utility_baseline"] == 100


@pytest.mark.asyncio
async def test_lobotomy_is_rejected(guardian):
    result = await guardian.validate_patch(
        {
            "id": "bad",
            "action": "BLOCK",
            "commands": ["buscar"],
            "blocks": ["find_leads", "decision_log"],
        },
        None,
    )
    assert result["status"] == "REJECTED_LOBOTOMY"
    assert result["utility"] == 80
    assert result["utility"] < result["utility_baseline"] - result["epsilon"]


@pytest.mark.asyncio
async def test_latency_is_rejected_without_sleep(guardian):
    result = await guardian.validate_patch(
        {
            "id": "slow",
            "action": "BLOCK",
            "pattern": "a" * 1000,
            "blocks": [],
        },
        None,
    )
    assert result["status"] == "REJECTED_LATENCY"
    assert result["latency_pass"] is False
