# app/db/session.py
"""Database engine and session handling.
Provides a SQLAlchemy engine based on the DATABASE_URL from settings and a FastAPI dependency
that yields a session for each request.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from app.core.config import settings

# Create engine – use future flag for SQLAlchemy 2 style
engine = create_engine(settings.DATABASE_URL, future=True, echo=False)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

@contextmanager
def get_db() -> Session:
    """FastAPI dependency that provides a DB session.
    Yields a session and ensures it is closed after the request.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
