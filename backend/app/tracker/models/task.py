import uuid
from typing import Optional

from sqlmodel import Field, Relationship

from app.core.base_models import UUIDModelBase
from app.tracker.models.task_statuses import TaskPriority, TaskStatus


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
    project: "Project" = Relationship(back_populates="tasks")  # noqa F821
    author: "User" = Relationship(  # noqa F821
        back_populates="authored_tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.author_id]"},
        cascade_delete=True,
    )
    assignee: Optional["User"] = Relationship(  # noqa F821
        back_populates="assigned_tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"},
    )
    status_history: list["TaskStatusHistory"] = Relationship(  # noqa F821
        back_populates="task",
        cascade_delete=True,
    )
