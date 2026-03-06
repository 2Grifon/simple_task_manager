from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.core.base_models import TimestampedModelBase, UUIDModelBase
from app.tracker.models.task_statuses import TaskStatus

if TYPE_CHECKING:
    from app.tracker.models.task import Task
    from app.users.models import User


class TaskStatusHistory(TimestampedModelBase, UUIDModelBase, table=True):
    """История изменений статуса задачи."""

    task_id: uuid.UUID = Field(
        foreign_key="task.id",
        nullable=False,
        index=True,
        ondelete="CASCADE",
    )
    changed_by_user_id: uuid.UUID = Field(
        foreign_key="user.id",
        nullable=False,
        index=True,
        ondelete="CASCADE",
    )

    # from_status = None означает первую запись при создании задачи
    from_status: Optional[TaskStatus] = Field(default=None, nullable=True)
    to_status: TaskStatus = Field(nullable=False)

    comment: Optional[str] = Field(default=None, nullable=True)

    # Relations
    task: Task = Relationship(back_populates="status_history")
    changed_by_user: User = Relationship(back_populates="status_changes")
