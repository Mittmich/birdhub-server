from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # relationship with the Detection model
    detections = relationship("Detection", back_populates="owner")
    # relationship with the EffectorAction model
    effector_actions = relationship("EffectorAction", back_populates="owner")

class Detection(Base):
    """Model forbird detections."""
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    class = Column(String, index=True)
    detection_timestmap = Column(DateTime, index=True)
    confidence = Column(Float, index=True)
    model_version = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # add many to one relationship with recorindg model
    recording_id = Column(Integer, ForeignKey("recordings.id"))

class EffectorAction(Base):
    """Model for effector actions."""
    __tablename__ = "effector_actions"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    action_timestamp = Column(DateTime, index=True)
    detection_timestmap = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

class Recording(Base):
    """Model for recordings."""
    __tablename__ = "recordings"

    id = Column(Integer, primary_key=True, index=True)
    recording_timestamp = Column(DateTime, index=True)
    recording_duration = Column(Integer, index=True)
    # add path to recording file
    recording_file_path = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))