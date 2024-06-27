import os
import pytest
import shutil
from functools import partial
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


@pytest.fixture
def tmp_upload_folder():
    """Creates and removes a temporary upload folder before and after each test."""
    # create temp upload folder
    os.makedirs("tmp_uploads", exist_ok=True)
    yield
    # remove temp upload folder
    shutil.rmtree("tmp_uploads")


def override_get_db():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = partial(
        get_settings_test, upload_folder="tmp_uploads"
    )
    return TestClient(app)
