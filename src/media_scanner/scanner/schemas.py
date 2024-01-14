from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, validator
from typing import Dict, List, Optional, Union


class DimensionsMixin:
    @validator("dimensions")
    def validate_dimensions(cls, v):
        if not v:
            return v

        if v.count("x") != 1:
            raise ValidationError('Dimensions must have exactly one "x"')

        try:
            width, height = map(int, v.split("x"))
        except ValidationError:
            raise ValidationError('Dimensions must contain numbers separated by "x"')

        if width <= 0 or height <= 0:
            raise ValidationError("Width and height must be positive integers")

        return v


class QueueScan(BaseModel):
    source_path: str

    class Config:
        from_attributes = True


class MediaBase(BaseModel, DimensionsMixin):
    file_path: str
    file_name: str
    dimensions: Optional[str] = None
    file_size: Optional[float] = None
    video_codec: Optional[list] = None
    audio_codec: Optional[list] = None
    subtitle_codec: Optional[list] = None
    duration: Optional[float] = None


class MediaCreate(MediaBase):
    uuid: str


class Media(MediaBase):
    id: int
    uuid: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    permissions: Optional[dict] = None

    class Config:
        from_attributes = True


class OrderDirectionEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class OrderByEnum(str, Enum):
    file_size = "file_size"
    file_path = "file_path"
    created_at = "created_at"
    updated_at = "updated_at"
    file_name = "file_name"


class FieldEnum(str, Enum):
    subtitle_codec = "subtitle_codec"
    audio_codec = "audio_codec"
    video_codec = "video_codec"
    file_name = "file_name"
    file_path = "file_path"
    dimensions = "dimensions"


class OperatorEnum(str, Enum):
    contains = "contains"


class MediaQuery(BaseModel):
    page: int = 1
    batch_size: int = 50
    order_by: OrderByEnum = Field(
        default=OrderByEnum.created_at,
        description=f"Options: {', '.join([item.value for item in OrderByEnum])}",
    )
    order_direction: OrderDirectionEnum = Field(
        default="desc", description="Options: asc, desc"
    )
    audio_codec: Optional[str] = None
    video_codec: Optional[str] = None
    subtitle_codec: Optional[str] = None
    min_size: Optional[int] = None


class ScanCommand(BaseModel):
    scan_path: str


class Disposition(BaseModel):
    default: Optional[int] = None
    dub: Optional[int] = None
    original: Optional[int] = None
    comment: Optional[int] = None
    lyrics: Optional[int] = None
    karaoke: Optional[int] = None
    forced: Optional[int] = None
    hearing_impaired: Optional[int] = None
    visual_impaired: Optional[int] = None
    clean_effects: Optional[int] = None
    attached_pic: Optional[int] = None
    timed_thumbnails: Optional[int] = None
    captions: Optional[int] = None
    descriptions: Optional[int] = None
    metadata: Optional[int] = None
    dependent: Optional[int] = None
    still_image: Optional[int] = None


class BaseStream(BaseModel):
    index: int
    codec_name: str
    codec_long_name: Optional[str] = None
    codec_tag_string: Optional[str] = None
    codec_tag: Optional[str] = None
    r_frame_rate: Optional[str] = None
    avg_frame_rate: Optional[str] = None
    time_base: Optional[str] = None
    start_pts: Optional[int] = None
    start_time: Optional[str] = None
    disposition: Optional[Disposition] = None
    tags: Optional[Dict[str, str]] = None


class VideoStream(BaseStream):
    codec_type: Optional[str] = Field("video", Literal=True)
    profile: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    coded_width: Optional[int] = None
    coded_height: Optional[int] = None
    closed_captions: Optional[int] = None
    film_grain: Optional[int] = None
    has_b_frames: Optional[int] = None
    sample_aspect_ratio: Optional[str] = None
    display_aspect_ratio: Optional[str] = None
    pix_fmt: Optional[str] = None
    level: Optional[int] = None
    color_range: Optional[str] = None
    color_space: Optional[str] = None
    color_transfer: Optional[str] = None
    color_primaries: Optional[str] = None
    chroma_location: Optional[str] = None
    field_order: Optional[str] = None
    refs: Optional[int] = None
    is_avc: Optional[str] = None
    nal_length_size: Optional[str] = None
    bits_per_raw_sample: Optional[str] = None
    extradata_size: Optional[int] = None


class AudioStream(BaseStream):
    codec_type: Optional[str] = Field("audio", Literal=True)
    profile: Optional[str] = None
    sample_fmt: Optional[str] = None
    sample_rate: Optional[str] = None
    channels: Optional[int] = None
    channel_layout: Optional[str] = None
    bits_per_sample: Optional[int] = None
    initial_padding: Optional[int] = None
    extradata_size: Optional[int] = None


class SubtitleStream(BaseStream):
    codec_type: Optional[str] = Field("subtitle", Literal=True)
    duration_ts: Optional[int] = None
    duration: Optional[str] = None
    extradata_size: Optional[int] = None


class AttachmentStream(BaseStream):
    codec_type: Optional[str] = Field("attachment", Literal=True)
    duration_ts: Optional[int] = None
    duration: Optional[str] = None
    extradata_size: Optional[int] = None


class Format(BaseModel):
    filename: Optional[str] = None
    nb_streams: Optional[int] = None
    nb_programs: Optional[int] = None
    format_name: Optional[str] = None
    format_long_name: Optional[str] = None
    start_time: Optional[str] = None
    duration: Optional[str] = None
    size: Optional[str]
    bit_rate: Optional[str] = None
    probe_score: Optional[int] = None
    tags: Optional[Dict[str, str]] = None


class MediaMetadata(BaseModel):
    streams: Optional[
        List[Union[VideoStream, AudioStream, SubtitleStream, AttachmentStream]]
    ] = None
    format: Optional[Format] = None

    def get_streams(self, type: str) -> List[BaseStream]:
        return [stream for stream in self.streams if stream.codec_type == type]

    def get_tag(self, tag: str) -> Optional[str]:
        return self.format.tags.get(tag)


class Result(BaseModel):
    file_path: str
    file_name: str
    dimensions: Optional[str] = None
    file_size: Optional[float] = None
    video_codec: Optional[list] = None
    audio_codec: Optional[list] = None
    subtitle_codec: Optional[list] = None
    duration: Optional[float] = None
    uuid: str
