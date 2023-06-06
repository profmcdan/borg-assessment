from datetime import datetime
from sqlmodel import SQLModel
from app.core.models import TimestampModel, UUIDModel


class UrlBase(SQLModel):
    original_url: str
    short_url: str
    published: bool = False
    owner_id: str
    expiry_date: datetime = None
    code: str = None


class UrlRead(UrlBase, UUIDModel, TimestampModel):
    pass

    # class Config:
    #     schema_extra = {"example": ex_url_read}


class UrlCreate(SQLModel):
    original_url: str


class UrlPatch(SQLModel):
    original_url: str
    expiry_date: datetime = None
