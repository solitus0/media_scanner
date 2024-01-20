import datetime
from dataclasses import dataclass

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Boolean

from media_scanner.database import Base, engine


@dataclass
class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False, index=True, unique=True)
    file_path = Column(String)
    file_name = Column(String)
    file_size = Column(Float, nullable=True)
    video_codec = Column(JSON, nullable=True)
    audio_codec = Column(JSON, nullable=True)
    subtitle_codec = Column(JSON, nullable=True)
    duration = Column(Float, nullable=True)
    dimensions = Column(String, nullable=True)
    has_default_subtitle = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


Base.metadata.create_all(engine)
