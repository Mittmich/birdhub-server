from .utils import get_session
import os
from app.data.crud import get_all_recordings


def test_add_recording(client, tmp_upload_folder):
    # post recording
    with open(r"tests\testfiles\test_video.mp4", "rb") as f:
        response = client.post(
            "/recordings/",
            files={
                "file": ("test.mp4", f, "video/mp4"),
            },
            data={
                "recording_timestamp": "2021-01-01T00:00:00",
                "recording_end_timestamp": "2021-01-01T00:00:10",
            },
        )
    assert response.status_code == 200
    # check if recording was added to the database
    db = get_session()
    recordings = get_all_recordings(db)
    db.close()
    assert len(recordings) == 1
    # check if file was saved to the upload folder
    assert len(os.listdir("tmp_uploads")) == 1
    assert os.listdir("tmp_uploads")[0].endswith(".mp4")
    # check if file content if the same
    with open(r"tests\testfiles\test_video.mp4", "rb") as f:
        original_content = f.read()
    with open(f"tmp_uploads/{os.listdir('tmp_uploads')[0]}", "rb") as f:
        new_content = f.read()
    assert original_content == new_content
