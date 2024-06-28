from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EffectorActionPost(BaseModel):
    action: str
    action_metadata: Optional[str] = None
    detection_timestamp: datetime
    action_timestamp: datetime


class SingleDetectionPost(BaseModel):
    detected_class: str
    detection_timestamp: datetime
    confidence: float
    model_version: str


class DetectionPost(BaseModel):
    detections: list[SingleDetectionPost]


class RecordingPost(BaseModel):
    recording_timestamp: datetime
    recording_end_timestamp: datetime


class DetectionGet(SingleDetectionPost):
    id: int

    class Config:
        orm_mode = True
