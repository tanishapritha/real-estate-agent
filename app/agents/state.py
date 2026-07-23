# app/agents/state.py
"""Typed workflow state used by LangGraph nodes.
All agents read/write this object; it is persisted as JSON in checkpoints.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class WorkflowState(BaseModel):
    # Core entities
    lead_id: Optional[int] = None
    customer_id: Optional[int] = None
    property_id: Optional[int] = None

    # Conversation and messages
    conversation_id: Optional[int] = None
    messages: List[Dict[str, Any]] = Field(default_factory=list)

    # Agent‑specific interim data
    qualification: Dict[str, Any] = Field(default_factory=dict)
    inventory_matches: List[Dict[str, Any]] = Field(default_factory=list)
    recommendation: Dict[str, Any] = Field(default_factory=dict)
    followup_actions: List[Dict[str, Any]] = Field(default_factory=list)

    # Execution metadata
    workflow_status: str = "running"  # could be running, paused, completed, failed
    current_node: Optional[str] = None
    pending_tasks: List[Dict[str, Any]] = Field(default_factory=list)
    tool_history: List[Dict[str, Any]] = Field(default_factory=list)
    decision_history: List[Dict[str, Any]] = Field(default_factory=list)
    checkpoint_id: Optional[str] = None
    execution_id: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
