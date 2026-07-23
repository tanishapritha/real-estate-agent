# app/db/models/property.py
"""Property model.
Represents a real estate property.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from . import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    sqft = Column(Integer, nullable=True)
    listed_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
