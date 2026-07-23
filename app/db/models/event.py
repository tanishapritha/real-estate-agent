# app/db/models/event.py
"""Event model.
Stores domain events emitted during workflow execution.
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from . import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("workflow_executions.id"), nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=True)
    timestamp = Column(DateTime, nullable=False)
