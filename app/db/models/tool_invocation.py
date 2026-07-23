# app/db/models/tool_invocation.py
"""ToolInvocation model.
Records a single tool call made by an agent.
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from . import Base

class ToolInvocation(Base):
    __tablename__ = "tool_invocations"

    id = Column(Integer, primary_key=True, index=True)
    agent_execution_id = Column(Integer, ForeignKey("agent_executions.id"), nullable=False)
    tool_name = Column(String, nullable=False)
    args = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    timestamp = Column(DateTime, nullable=False)
