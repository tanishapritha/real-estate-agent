# app/db/models/__init__.py
"""SQLAlchemy model base and imports.
All model classes should inherit from `Base` defined here.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Export models for easy import
from .lead import Lead
from .customer import Customer
from .property import Property
from .conversation import Conversation
from .message import Message
from .workflow_execution import WorkflowExecution
from .workflow_checkpoint import WorkflowCheckpoint
from .event import Event
from .agent_execution import AgentExecution
from .tool_invocation import ToolInvocation
