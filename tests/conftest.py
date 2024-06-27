import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data.database import get_db
from .utils import set_up_db, clean_up_db, get_session
from app.data.settings import get_settings_test, get_settings


@pytest.fixture(autouse=True)
def db_setup():
    """Runs setup and teardown for the database before and after each test."""
    set_up_db()
    yield
    clean_up_db()


def override_get_db():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = get_settings_test
    return TestClient(app)
