# app/db/models/lead.py
"""Lead model.
Represents an incoming lead.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from . import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships (optional placeholders)
    customer_id = Column(Integer, nullable=True)
    # Add more fields as needed later
