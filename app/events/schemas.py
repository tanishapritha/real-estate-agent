# app/events/schemas.py
"""Pydantic schemas for internal event bus.
All events inherit from BaseModel for validation and JSON (de)serialization.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

class BaseEvent(BaseModel):
    """Common fields for every event."""

    event_id: str = Field(default_factory=lambda: "evt_" + datetime.utcnow().strftime("%Y%m%d%H%M%S%f"))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

class LeadCreated(BaseEvent):
    lead_id: int
    source: Optional[str] = None

class LeadQualified(BaseEvent):
    lead_id: int
    qualification: dict

class InventoryMatched(BaseEvent):
    lead_id: int
    matches: List[dict]

class RecommendationGenerated(BaseEvent):
    lead_id: int
    recommendation: dict

class CustomerResponded(BaseEvent):
    lead_id: int
    response: dict

class AppointmentBooked(BaseEvent):
    lead_id: int
    appointment: dict

class FollowupScheduled(BaseEvent):
    lead_id: int
    followup: dict

class WorkflowPaused(BaseEvent):
    lead_id: int
    reason: Optional[str] = None

class WorkflowResumed(BaseEvent):
    lead_id: int

class WorkflowCompleted(BaseEvent):
    lead_id: int
    outcome: Optional[str] = None
