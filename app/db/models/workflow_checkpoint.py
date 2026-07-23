# app/db/models/workflow_checkpoint.py
"""WorkflowCheckpoint model.
Stores checkpoints (states) within a workflow execution.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from . import Base

class WorkflowCheckpoint(Base):
    __tablename__ = "workflow_checkpoints"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("workflow_executions.id"), nullable=False)
    node_name = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    state_data = Column(JSON, nullable=True)  # Serialized workflow state
