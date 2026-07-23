# tests/test_metrics.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.main import app
from app.db.session import get_db
from app.db.models.models import Base

# Create SQLite in-memory DB with StaticPool so all connections share the same memory DB
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_leads_today():
    response = client.get("/leads/today")
    assert response.status_code == 200
    assert "count" in response.json()

def test_metrics_leads_count():
    response = client.get("/metrics/leads/count?days=7")
    assert response.status_code == 200
    data = response.json()
    assert "counts" in data
    assert len(data["counts"]) == 7

def test_events_recent():
    response = client.get("/events/recent")
    assert response.status_code == 200
    data = response.json()
    assert "events" in data

def test_agents_list():
    response = client.get("/agents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_workflows_list():
    response = client.get("/workflows/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
