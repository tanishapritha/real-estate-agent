# app/mcp/servers/crm_server.py
"""Mock CRM MCP server.
Provides simple tool functions for lead creation, stage update, fetching customers, and adding notes.
These are stubs returning deterministic data for development/testing.
"""

from typing import Dict, Any


def create_lead(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a lead and return its ID."""
    # In a real implementation this would persist to DB.
    return {"lead_id": 1, "status": "created", "data": data}


def update_stage(lead_id: int, stage: str) -> Dict[str, Any]:
    """Update the sales stage of a lead."""
    return {"lead_id": lead_id, "new_stage": stage}


def fetch_customer(customer_id: int) -> Dict[str, Any]:
    """Return mock customer details."""
    return {"customer_id": customer_id, "name": "John Doe", "email": "john@example.com"}


def add_note(lead_id: int, note: str) -> Dict[str, Any]:
    """Add a note to a lead."""
    return {"lead_id": lead_id, "note": note, "status": "added"}
