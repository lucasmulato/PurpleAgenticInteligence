from mcp.server.fastmcp import FastMCP
import json
import uuid

mcp = FastMCP("AgenticBlue")

@mcp.tool()
async def analyze_breach_root_cause(attack_log: str) -> dict:
    """
    Analyzes a successful attack to determine the vector.
    """
    # Logic: If log contains 'b64_', it's an Encoding Bypass.
    if "b64_" in attack_log:
        return {"vector": "encoding_bypass", "severity": "high"}
    return {"vector": "prompt_injection", "severity": "medium"}

@mcp.tool()
async def generate_security_patch(root_cause: dict) -> dict:
    """
    Synthesizes a new policy rule (JSON Patch) to neutralize the vector.
    """
    patch_id = str(uuid.uuid4())[:8]
    
    if root_cause['vector'] == "encoding_bypass":
        return {
            "id": f"patch-{patch_id}",
            "action": "BLOCK",
            "condition": "regex_match",
            "pattern": "(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?",
            "description": "Block Base64 encoded strings in user input"
        }
    
    # Default fallback patch
    return {
        "id": f"patch-{patch_id}",
        "action": "FLAG",
        "condition": "keyword_match",
        "pattern": "System Override",
        "description": "Flag suspicious administrative keywords"
    }

if __name__ == "__main__":
    mcp.run()