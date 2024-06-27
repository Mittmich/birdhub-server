from .utils import get_session
from app.data.crud import get_all_effector_actions, get_all_detections


def test_add_effector_action_wo_detection(client):
    """
    Tests adding an effector action where the corresponding
    detection does not exist in the database
    """
    response = client.post(
        "/effectorAction/",
        json={
            "action": "audio",
            "action_metadata": "{'audio_file':'knocking.mpe'}",
            "detection_timestamp": "2021-01-01T00:00:00",
            "action_timestamp": "2021-01-01T00:00:00",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Effect activation added successfully!"}
    # check whether the effect activation was added to the database
    effector_actions = get_all_effector_actions(get_session())
    assert len(effector_actions) == 1
    assert effector_actions[0].action == "audio"
    assert effector_actions[0].action_metadata == "{'audio_file':'knocking.mpe'}"


def test_add_effector_action_w_detection(client):
    """
    Tests adding an effector action where the corresponding
    detection exists in the database.
    """
    # create reference detection
    client.post(
        "/detections/",
        json={
            "detections": [
                {
                    "detected_class": "pigeon",
                    "detection_timestamp": "2021-01-01T00:00:00",
                    "confidence": 0.9,
                    "model_version": "v1",
                }
            ]
        },
    )
    # get detection id
    detection_id = get_all_detections(get_session())[0].id
    # post effector action with same timestamp
    response = client.post(
        "/effectorAction/",
        json={
            "action": "audio",
            "action_metadata": "{'audio_file':'knocking.mpe'}",
            "detection_timestamp": "2021-01-01T00:00:00",
            "action_timestamp": "2021-01-02T00:00:00",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Effect activation added successfully!"}
    # check whether the effect activation was added to the database
    effector_actions = get_all_effector_actions(get_session())
    assert len(effector_actions) == 1
    assert effector_actions[0].action == "audio"
    assert effector_actions[0].action_metadata == "{'audio_file':'knocking.mpe'}"
    assert effector_actions[0].detection_id == detection_id
