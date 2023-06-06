import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field

from app.core.models import TimestampModel, UUIDModel


class UserBase(SQLModel):
    email: str
    password: str
    firstname: str
    lastname: str
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, TimestampModel, UUIDModel, table=True):
    pass


class UserCreate(UserBase):
    pass


class TokenBase(SQLModel):
    user_id: str
    token: str
    is_valid: bool = True


class Token(TimestampModel, TokenBase, UUIDModel, table=True):
    pass
