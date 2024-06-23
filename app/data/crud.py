from sqlalchemy.orm import Session


from . import models, schemas


def add_detections(db: Session, detections: list[schemas.SingleDetectionPost]):
    created_detections = []

    for detection in detections:
        db_detection = models.Detection(
            detected_class=detection.detected_class,
            detection_timestamp=detection.detection_timestamp,
            confidence=detection.confidence,
            model_version=detection.model_version,
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


def get_all_detections(db: Session):
    return db.query(models.Detection).all()
