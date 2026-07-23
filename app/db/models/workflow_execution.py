# app/db/models/workflow_execution.py
"""WorkflowExecution model.
Tracks an execution of a workflow.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from . import Base

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="running")
    is_successful = Column(Boolean, default=False)
