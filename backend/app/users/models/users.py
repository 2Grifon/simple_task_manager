from sqlmodel import Field

from app.core.base_models import UUIDModelBase, TimestampedModelBase


class User(UUIDModelBase, TimestampedModelBase, table=True):
    # id - уже определён в UUIDModelBase
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: str
