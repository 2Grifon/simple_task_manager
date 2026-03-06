from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.core.base_models import UUIDModelBase, TimestampedModelBase

if TYPE_CHECKING:
    from app.tracker.models.project import Project, ProjectMember
    from app.tracker.models.task import Task
    from app.tracker.models.task_history import TaskStatusHistory


class User(UUIDModelBase, TimestampedModelBase, table=True):
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: str

    # Relations
    owned_projects: list[Project] = Relationship(
        back_populates="owner",
    )
    project_memberships: list[ProjectMember] = Relationship(
        back_populates="user",
        cascade_delete=True,
    )
    authored_tasks: list[Task] = Relationship(
        back_populates="author",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "[Task.author_id]"},
    )
    assigned_tasks: list[Task] = Relationship(
        back_populates="assignee",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"},
    )
    status_changes: list[TaskStatusHistory] = Relationship(
        back_populates="changed_by_user",
        cascade_delete=True,
    )
