from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
import uuid
import datetime
from ..data.crud import add_recording
from ..data.schemas import RecordingPost
from ..data.database import get_db
from ..data.settings import Settings, get_settings

router = APIRouter()


@router.post("/recordings/", tags=["recordings"])
async def post_recording(
    db=Depends(get_db),
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
    recording_timestamp: datetime.datetime = Form(...),
    recording_end_timestamp: datetime.datetime = Form(...),
):
    # check whether file is an mp4 basd on file extension
    if not file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only mp4 files are allowed!")
    # Save the file to the upload folder
    filename = f"{uuid.uuid4().hex}.mp4"
    file_path = f"{settings.upload_folder}/{filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # Add the recording to the database
    add_recording(
        db,
        RecordingPost(
            recording_timestamp=recording_timestamp,
            recording_end_timestamp=recording_end_timestamp,
        ),
        file_path,
    )
    return {"message": "Recording added successfully!"}
