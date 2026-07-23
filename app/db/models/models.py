# app/db/models/models.py
"""SQLAlchemy models for RealEstate AI Sales OS.
Defines core entities used throughout the workflow.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ---- Core Entities ----

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # relationship to Conversation
    conversations = relationship("Conversation", back_populates="lead", cascade="all, delete-orphan")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # relationship to WorkflowExecution
    workflows = relationship("WorkflowExecution", back_populates="customer", cascade="all, delete-orphan")

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    extra_metadata = Column(JSON, nullable=True)  # extra free‑form data

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    lead = relationship("Lead", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String, nullable=False)  # "lead" or "agent"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    conversation = relationship("Conversation", back_populates="messages")

# ---- Workflow Execution ----

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status = Column(String, nullable=False, default="running")
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    current_node = Column(String, nullable=True)
    customer = relationship("Customer", back_populates="workflows")
    checkpoints = relationship("WorkflowCheckpoint", back_populates="execution", cascade="all, delete-orphan")

class WorkflowCheckpoint(Base):
    __tablename__ = "workflow_checkpoints"
    id = Column(Integer, primary_key=True, autoincrement=True)
    execution_id = Column(Integer, ForeignKey("workflow_executions.id"), nullable=False)
    node = Column(String, nullable=False)
    state_snapshot = Column(JSON, nullable=False)  # serialized state for resumption
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    execution = relationship("WorkflowExecution", back_populates="checkpoints")

# ---- Event & Agent Execution ----

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class AgentExecution(Base):
    __tablename__ = "agent_executions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_name = Column(String, nullable=False)
    execution_id = Column(Integer, ForeignKey("workflow_executions.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="running")
    workflow_execution = relationship("WorkflowExecution")

class ToolInvocation(Base):
    __tablename__ = "tool_invocations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_execution_id = Column(Integer, ForeignKey("agent_executions.id"), nullable=False)
    tool_name = Column(String, nullable=False)
    request = Column(JSON, nullable=False)
    response = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    agent_execution = relationship("AgentExecution")
