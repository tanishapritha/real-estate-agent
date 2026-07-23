# app/db/models/message.py
"""Message model.
Stores individual messages within a conversation.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String, nullable=False)  # e.g., 'lead' or 'agent'
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_read = Column(Boolean, default=False)

    conversation = relationship("Conversation", back_populates="messages")
