from datetime import datetime
from app.data.crud import get_all_detections
from .utils import get_session


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
                    "detection_timestamp": datetime(2021, 5, 1, 10, 12).strftime("%Y-%m-%dT%H:%M:%S"),
                    "confidence": 0.9,
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Detections added successfully!"}
    # check whether the detection was added to the database
    db = get_session()
    detections = get_all_detections(db)
    assert len(detections) == 1
    assert detections[0].detected_class == "pigeon"
    assert detections[0].confidence == 0.9
    assert detections[0].detection_timestamp == datetime(2021, 5, 1, 10, 12)

def test_read_all_detections(client):
    # add 3 detections to database
    response = client.post(
        "/detections/",
        json={
            "detections": [
                {
                    "detected_class": "pigeon",
                    "detection_timestamp": "2021-01-01T00:00:00",
                    "confidence": 0.9,
                    "model_version": "v1",
                },
                {
                    "detected_class": "sparrow",
                    "detection_timestamp": "2021-02-01T01:00:00",
                    "confidence": 0.8,
                    "model_version": "v1",
                },
                {
                    "detected_class": "crow",
                    "detection_timestamp": "2021-03-01T02:00:00",
                    "confidence": 0.7,
                    "model_version": "v1",
                },
            ]
        },
    )
    # test read all detections
    response = client.get("/detections/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_read_detections_time_range(client):
    # add 3 detections to database
    response = client.post(
        "/detections/",
        json={
            "detections": [
                {
                    "detected_class": "pigeon",
                    "detection_timestamp": "2021-01-01T00:00:00",
                    "confidence": 0.9,
                    "model_version": "v1",
                },
                {
                    "detected_class": "sparrow",
                    "detection_timestamp": "2021-02-01T01:00:00",
                    "confidence": 0.8,
                    "model_version": "v1",
                },
                {
                    "detected_class": "crow",
                    "detection_timestamp": "2021-03-01T02:00:00",
                    "confidence": 0.7,
                    "model_version": "v1",
                },
            ]
        },
    )
    # test read all detections
    response = client.get(
        "/detections/?start=2021-02-01T00:00:00&end=2021-03-01T03:00:00"
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
