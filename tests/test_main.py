import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.data.database import Base, get_db
from app.data.settings import get_settings_test, get_settings
from app.data.crud import get_all_detections
from app.main import app


# Override the get_db function to use a SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = get_settings_test
    return TestClient(app)


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Birdhub (test)!"}


def test_add_detection(client):
    response = client.post(
        "/detections/",
        json={
            "detections": [
                {
                    "detected_class": "pigeon",
                    "detection_timestamp": "2021-01-01T00:00:00",
                    "confidence": 0.9,
                    "model_version": "v1",
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Detections added successfully!"}
    # check whether the detection was added to the database
    db = TestingSessionLocal()
    detections = get_all_detections(db)
    assert len(detections) == 1
    assert detections[0].detected_class == "pigeon"
    assert detections[0].confidence == 0.9
    db.close()
