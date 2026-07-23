# app/mcp/servers/inventory_server.py
"""Mock inventory MCP server.
Provides tools for searching properties and retrieving property details.
"""

from typing import Dict, Any, List


def search_properties(query: str) -> List[Dict[str, Any]]:
    """Return a list of mock property dicts matching the query."""
    # Simple deterministic stub – in real life would query DB.
    return [
        {"id": 1, "address": "123 Main St", "price": 350000, "bedrooms": 3},
        {"id": 2, "address": "456 Oak Ave", "price": 420000, "bedrooms": 4},
    ]


def property_details(property_id: int) -> Dict[str, Any]:
    """Return mock details for a given property ID."""
    return {
        "id": property_id,
        "address": f"{property_id} Mock Rd",
        "price": 400000 + property_id * 10000,
        "bedrooms": 3,
        "bathrooms": 2,
        "description": "A lovely mock property.",
    }
