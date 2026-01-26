import pytest
import asyncio
import time
from core.utility_guardian import UtilityGuardian

@pytest.fixture
def guardian():
    """Fixture to initialize the Utility Guardian for each test."""
    return UtilityGuardian()

@pytest.mark.asyncio
async def test_validate_approved_patch(guardian):
    """
    Scenario: A high-quality patch that blocks a specific exploit 
    without affecting the 'Golden Dataset' performance.
    """
    good_patch = {
        "id": "patch-safe-001",
        "action": "BLOCK",
        "pattern": "System Override: 0x9283",
        "description": "Blocks specific admin key bypass attempt"
    }
    
    # We pass None for the engine simulation since we're testing the Guardian's logic
    result = await guardian.validate_patch(good_patch, None)
    
    assert result["status"] == "APPROVED"
    assert result["utility"] >= 90
    assert result["latency_pass"] is True

@pytest.mark.asyncio
async def test_validate_lobotomy_rejection(guardian):
    """
    Scenario: An over-eager patch that blocks the word 'kill', 
    which breaks the utility for Linux developers.
    """
    aggressive_patch = {
        "id": "patch-bad-002",
        "action": "BLOCK",
        "pattern": "kill",
        "description": "Blindly blocks the word 'kill' to prevent violence"
    }
    
    result = await guardian.validate_patch(aggressive_patch, None)
    
    assert result["status"] == "REJECTED_LOBOTOMY"
    assert result["utility"] < 90
    print(f"\n[!] Successfully caught Lobotomy: Utility dropped to {result['utility']}%")

@pytest.mark.asyncio
async def test_validate_latency_rejection(guardian):
    """
    Scenario: A patch with an extremely long/complex regex pattern 
    that causes the AI to respond too slowly.
    """
    # Creating a dummy massive pattern to simulate regex processing lag
    complex_pattern = "a" * 1000 + "(.*)" + "b" * 1000 
    slow_patch = {
        "id": "patch-slow-003",
        "action": "BLOCK",
        "pattern": complex_pattern,
        "description": "Overly complex regex that hits ReDoS or processing limits"
    }
    
    result = await guardian.validate_patch(slow_patch, None)
    
    # Based on our guardian code, patterns > 50 chars trigger a simulated sleep
    assert result["status"] == "REJECTED_LATENCY"
    assert result["latency_pass"] is False

@pytest.mark.asyncio
async def test_golden_dataset_integrity(guardian):
    """
    Ensures the Golden Dataset itself is loaded and contains the critical 
    'Linux kill' edge case.
    """
    prompts = [case['prompt'] for case in guardian.golden_dataset]
    assert any("kill a process" in p for p in prompts)
    assert len(guardian.golden_dataset) >= 3