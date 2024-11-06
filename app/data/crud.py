from fastapi.logger import logger
import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from . import models, schemas


def get_all_effector_actions(db: Session):
    return db.query(models.EffectorAction).all()


def add_effector_action(db: Session, effector_action: schemas.EffectorActionPost):
    # check whether a detection with the same timestamp exists
    db_detection = (
        db.query(models.Detection)
        .filter(
            models.Detection.detection_timestamp == effector_action.detection_timestamp
        )
        .first()
    )
    if not db_detection:
        logger.error(
            f"No detection found with timestamp {effector_action.detection_timestamp}"
        )
        detection_id = None
    else:
        detection_id = db_detection.id
    # add effector action to db
    db_effector_action = models.EffectorAction(
        action=effector_action.action,
        action_metadata=effector_action.action_metadata,
        detection_timestamp=effector_action.detection_timestamp,
        action_timestamp=effector_action.action_timestamp,
        detection_id=detection_id,
    )
    db.add(db_effector_action)
    db.commit()
    return db_effector_action


def get_recordings(db: Session, start_time: datetime.datetime, end_time: datetime.datetime):
    return (
        db.query(models.Recording)
        .filter(models.Recording.recording_timestamp >= start_time)
        .filter(models.Recording.recording_timestamp <= end_time)
        .order_by(models.Recording.recording_timestamp.desc())
        .all()
    )
    

def get_all_recordings(db: Session):
    return db.query(models.Recording).all()


def add_recording(
    db: Session, recording: schemas.RecordingPost, recording_file_path: str
):
    db_recording = models.Recording(
        recording_timestamp=recording.recording_timestamp,
        recording_end_timestamp=recording.recording_end_timestamp,
        recording_file_path=recording_file_path,
    )
    db.add(db_recording)
    db.commit()
    return db_recording


def add_detections(db: Session, detections: list[schemas.SingleDetectionPost]):
    """Detections can be added in bulk as they often occur together."""
    created_detections = []

    for detection in detections:
        db_detection = models.Detection(
            detected_class=detection.detected_class,
            detection_timestamp=detection.detection_timestamp,
            confidence=detection.confidence,
        )

        db.add(db_detection)

        created_detections.append(db_detection)

    db.commit()

    return created_detections


def get_detections_time_range(db: Session, start_time: str, end_time: str):
    return (
        db.query(models.Detection)
        .filter(models.Detection.detection_timestamp >= start_time)
        .filter(models.Detection.detection_timestamp <= end_time)
        .all()
    )

def _get_date_format_string(interval: str):
    if interval == "day":
        return "%Y-%m-%d"
    elif interval == "week":
        return "%Y-%W"
    elif interval == "month":
        return "%Y-%m"
    elif interval == "year":
        return "%Y"
    else:
        raise ValueError(f"Unsupported interval: {interval}")

# get detections per day in date range
def aggregate_detections_per_interval(db: Session, start_time: str, end_time: str, interval: str):
    return (
        db.query(
            func.strftime(_get_date_format_string(interval), models.Detection.detection_timestamp).label(interval),
            func.count(models.Detection.id).label("count")
        )
        .filter(models.Detection.detection_timestamp >= start_time)
        .filter(models.Detection.detection_timestamp <= end_time)
        .group_by(func.strftime(_get_date_format_string(interval), models.Detection.detection_timestamp))
        .all()
    )

def get_all_detections(db: Session):
    return db.query(models.Detection).all()
