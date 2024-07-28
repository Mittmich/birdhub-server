import uuid
from typing import Optional
import datetime
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, Query
from ..data.crud import add_recording, get_recordings
from ..data.schemas import RecordingPost
from ..data.database import get_db
from ..data.settings import Settings, get_settings

router = APIRouter()


@router.get("/recordings/", tags=["recordings"])
async def get_recordings_route(
    db=Depends(get_db),
    start_time: Optional[datetime.datetime] = None,
    end_time: Optional[datetime.datetime]= None
    ):
    # initialize end_time to current time if not provided
    if end_time is None:
        # add end time as now plus one day for timezone differences
        end_time = datetime.datetime.now() + datetime.timedelta(days=1)
    if start_time is None:
        start_time = datetime.datetime(1970, 1, 1)
    return get_recordings(db, start_time, end_time)

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
