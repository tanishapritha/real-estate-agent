# app/db/models/customer.py
"""Customer model.
Represents a CRM customer linked to a lead.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from . import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
