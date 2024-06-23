from pydantic import BaseModel
from datetime import datetime


class SingleDetectionPost(BaseModel):
    detected_class: str

    detection_timestamp: datetime
    confidence: float

    model_version: str


class DetectionPost(BaseModel):
    detections: list[SingleDetectionPost]


class DetectionGet(SingleDetectionPost):
    id: int

    class Config:
        orm_mode = True
