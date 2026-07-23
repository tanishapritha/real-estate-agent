# app/agents/inventory.py
"""Inventory agent node.
Queries the inventory MCP server for property matches based on the qualification data.
Updates ``state.inventory_matches``.
"""

from typing import Dict, Any, List

from app.mcp.client import call_tool
from app.agents.state import WorkflowState

def run(state: WorkflowState) -> WorkflowState:
    """Execute inventory lookup.
    Expects ``state.qualification`` to contain a ``raw`` JSON string with preferences.
    Returns the updated state.
    """
    # Simple extraction – assume qualification['raw'] is a JSON‑compatible string
    try:
        import json
        prefs = json.loads(state.qualification.get("raw", "{}"))
    except Exception:
        prefs = {}
    query = prefs.get("budget", "") + " " + prefs.get("location", "")
    # Call the mock inventory MCP server
    results: List[Dict[str, Any]] = call_tool("inventory", "search_properties", query=query)
    state.inventory_matches = results
    state.current_node = "inventory"
    return state
