import pytest
from app.models.database import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all database tables for tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
