from sqlmodel import Field
from .schemas import UrlBase
from app.core.models import TimestampModel, UUIDModel


class Url(UrlBase, TimestampModel, UUIDModel, table=True):
    code: str = Field(..., max_length=11, unique=True, nullable=True, index=True)
    short_url: str = Field(..., max_length=50, unique=True, index=True)
    original_url: str = Field(..., max_length=500, unique=True, index=True)

