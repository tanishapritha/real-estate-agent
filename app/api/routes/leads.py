# app/api/routes/leads.py
"""FastAPI routes for lead management.
Creates a lead in the DB and publishes a `LeadCreated` event.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.models import Lead

from app.events.bus import publish
from app.events.schemas import LeadCreated

router = APIRouter(prefix="/leads", tags=["leads"])

class LeadCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    email: str = Field(..., example="john@example.com")
    phone: str | None = Field(None, example="+1-555-1234")

@router.post("/", response_model=dict)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    # Prevent duplicate leads by email
    existing = db.query(Lead).filter(Lead.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Lead with this email already exists")

    lead = Lead(name=payload.name, email=payload.email, phone=payload.phone)
    db.add(lead)
    db.commit()
    db.refresh(lead)

    # Publish a LeadCreated event to the Redis stream
    event = LeadCreated(lead_id=lead.id)
    publish(event, stream="lead_created")

    return {"lead_id": lead.id, "status": "created"}
