import pytest
from fastapi.testclient import TestClient
from main import app
from app.models.database import Base, engine

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to HeadSpace AI API"}

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
