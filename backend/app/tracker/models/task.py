from __future__ import annotations

from enum import Enum
import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.core.base_models import TimestampedModelBase, UUIDModelBase

if TYPE_CHECKING:
    from app.tracker.models.project import Project
    from app.users.models import User


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    review = "review"
    done = "done"
    cancelled = "cancelled"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


# Допустимые переходы статусов — используется в service.py
ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.created: {TaskStatus.in_progress, TaskStatus.cancelled},
    TaskStatus.in_progress: {TaskStatus.review, TaskStatus.created},
    TaskStatus.review: {TaskStatus.done, TaskStatus.in_progress},
    TaskStatus.done: set(),
    TaskStatus.cancelled: set(),
}


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


class Task(UUIDModelBase, table=True):
    """Задача внутри проекта."""

    project_id: uuid.UUID = Field(
        foreign_key="project.id",
        nullable=False,
        index=True,
        ondelete="CASCADE",
    )
    title: str = Field(max_length=500, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)

    priority: TaskPriority = Field(
        default=TaskPriority.medium,
        # sa_column=Column(
        #     SAEnum(TaskPriority, name="task_priority", create_type=True),
        #     nullable=False,
        # ),
    )
    status: TaskStatus = Field(
        default=TaskStatus.created,
        # sa_column=Column(
        #     SAEnum(TaskStatus, name="task_status", create_type=True),
        #     nullable=False,
        #     index=True,
        # ),
    )

    author_id: uuid.UUID = Field(
        foreign_key="user.id",
        nullable=False,
        index=True,
        ondelete="CASCADE",
    )
    assignee_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="user.id",
        nullable=True,
        ondelete="CASCADE",
        index=True,
    )

    # Relations
    project: Project = Relationship(back_populates="tasks")
    author: User = Relationship(
        back_populates="authored_tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.author_id]"},
        cascade_delete=True,
    )
    assignee: Optional[User] = Relationship(
        back_populates="assigned_tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"},
    )
    status_history: list[TaskStatusHistory] = Relationship(
        back_populates="task",
        cascade_delete=True,
    )
