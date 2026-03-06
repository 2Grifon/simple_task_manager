from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, DateTime


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class UUIDModelBase(SQLModel):
    """Базовый класс для моделей с UUID в качестве первичного ключа."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)


class TimestampedModelBase(SQLModel):
    """Базовый класс для моделей с полями created_at и updated_at."""

    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
