from pydantic import BaseModel
from datetime import datetime

class SingleDetection(BaseModel):
    detected_class: str
    detection_timestamp: datetime
    confidence: float
    model_version: str

class DetectionPost(BaseModel):
    detections: list[SingleDetection]