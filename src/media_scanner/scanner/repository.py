import logging

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from . import schemas
from media_scanner.scanner.entity import Media


def get_media(db: Session, media_id: int):
    return db.query(Media).filter(Media.id == media_id).first()


def all(db: Session):
    return db.query(Media).all()


def get_by_uuid(db: Session, uuid: str):
    return db.query(Media).filter(Media.uuid == uuid).first()


def get_by_ids(db: Session, media_ids: list[int]):
    return db.query(Media).filter(Media.uuid.in_(media_ids)).all()


def get_by_filter(db: Session, filter: schemas.MediaQuery) -> list[Media]:
    query = db.query(Media)

    if filter.video_codec:
        query = query.filter(Media.video_codec.contains(filter.video_codec))

    if filter.not_video_codec:
        query = query.filter(~Media.video_codec.contains(filter.not_video_codec))

    if filter.audio_codec:
        query = query.filter(Media.audio_codec.contains(filter.audio_codec))

    if filter.not_audio_codec:
        query = query.filter(~Media.audio_codec.contains(filter.not_audio_codec))

    if filter.subtitle_codec:
        query = query.filter(Media.subtitle_codec.contains(filter.subtitle_codec))

    if filter.not_subtitle_codec:
        query = query.filter(~Media.subtitle_codec.contains(filter.not_subtitle_codec))

    if filter.min_size:
        query = query.filter(Media.file_size >= filter.min_size)

    order_by = getattr(Media, filter.order_by)
    order_direction = getattr(order_by, filter.order_direction)

    paginated_query = (
        query.order_by(order_direction())
        .offset((filter.page - 1) * filter.batch_size)
        .limit(filter.batch_size)
    )

    return paginated_query.all()


def get_by_file_path(db: Session, file_path: str):
    return db.query(Media).filter(Media.file_path == file_path).first()


def create_media(db: Session, data: schemas.MediaCreate) -> Media:
    db_media = Media(**data.model_dump())
    db.add(db_media)
    db.commit()
    db.refresh(db_media)

    return db_media


def update_media(db: Session, media: Media, data: schemas.MediaCreate) -> Media:
    for key, value in data.model_dump().items():
        if getattr(media, key) != value:
            logging.info(f"Updating {key} from {getattr(media, key)} to {value}")
            setattr(media, key, value)

    db.commit()
    db.refresh(media)

    return media


def should_update(model: BaseModel, database_model):
    column_names = [
        column.key for column in inspect(database_model).mapper.column_attrs
    ]

    schema_attributes = set(model.__fields__.keys())
    if not schema_attributes.issubset(column_names):
        raise ValueError("Pydantic schema attributes do not match the database fields.")

    schema_values = {
        attr: getattr(model, attr) for attr in schema_attributes if attr not in ["uuid"]
    }

    model_values = {
        attr: getattr(database_model, attr)
        for attr in schema_attributes
        if attr not in ["uuid"]
    }

    return schema_values != model_values


def delete(db: Session, media: Media):
    db.delete(media)
    db.commit()
