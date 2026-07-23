# app/db/models/agent_execution.py
"""AgentExecution model.
Tracks execution of an individual agent within a workflow.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from . import Base

class AgentExecution(Base):
    __tablename__ = "agent_executions"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("workflow_executions.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="running")
    result = Column(JSON, nullable=True)
    is_successful = Column(Boolean, default=False)
