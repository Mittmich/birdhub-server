from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float

from .database import Base


class Detection(Base):
    """Model forbird detections."""

    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    detected_class = Column(String, index=True)
    detection_timestamp = Column(DateTime, index=True)
    confidence = Column(Float)
    # add many to one relationship with recorindg model
    recording_id = Column(Integer, ForeignKey("recordings.id"))


class EffectorAction(Base):
    """Model for effector actions."""

    __tablename__ = "effector_actions"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    action_metadata = Column(String)
    detection_timestamp = Column(DateTime, index=True)
    action_timestamp = Column(DateTime, index=True)
    # add many to one relationship with recording model
    recording_id = Column(Integer, ForeignKey("recordings.id"))
    # add relationship with detection model
    detection_id = Column(Integer, ForeignKey("detections.id"))


class Recording(Base):
    """Model for recordings."""

    __tablename__ = "recordings"

    id = Column(Integer, primary_key=True, index=True)
    recording_timestamp = Column(DateTime, index=True)
    recording_end_timestamp = Column(DateTime, index=True)
    # add path to recording file
    recording_file_path = Column(String, index=True)


class SunsetSunrise(Base):
    """Model for sunset and sunrise times."""

    __tablename__ = "sunset_sunrise"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer, index=True)
    day = Column(Integer, index=True)
    sunrise = Column(DateTime)
    sunset = Column(DateTime)
    city = Column(String, index=True)