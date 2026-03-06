import uuid
from typing import Optional

from sqlmodel import Field, Relationship

from app.core.base_models import TimestampedModelBase, UUIDModelBase
from app.tracker.models.task_statuses import TaskStatus


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
    from_status: Optional[TaskStatus] = Field(
        default=None,
        # sa_column=Column(
        #     SAEnum(TaskStatus, name="task_status", create_type=False),
        #     nullable=True,
        # ),
    )
    to_status: TaskStatus = Field(
        # sa_column=Column(
        #     SAEnum(TaskStatus, name="task_status", create_type=False),
        #     nullable=False,
        # ),
    )

    comment: Optional[str] = Field(default=None, nullable=True)

    # Relations
    task: "Task" = Relationship(back_populates="status_history")  # noqa F821
    changed_by_user: "User" = Relationship(  # noqa F821
        back_populates="status_changes"
    )  # pyright: ignore[reportUndefinedVariable] # noqa F821
