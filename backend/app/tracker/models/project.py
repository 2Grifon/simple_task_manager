from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.core.base_models import UUIDModelBase

if TYPE_CHECKING:
    from app.tracker.models.task import Task
    from app.users.models.users import User


class Project(UUIDModelBase, table=True):
    name: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)

    # Relations
    owner_id: uuid.UUID = (
        Field(  # Тут пожалуй есть некоторая избыточность, т.к. есть связь m2m с моделью
            # пользователей через ProjectMember, но, это поле нужно для быстой выборки владельца по
            # проекту и наоборот, а m2m для отслеживания исполнителей.
            foreign_key="user.id",
            nullable=False,
            index=True,
            ondelete="CASCADE",
        )
    )
    owner: User = Relationship(
        back_populates="owned_projects",
        cascade_delete=True,
    )

    members: list[ProjectMember] = Relationship(
        back_populates="projects",
    )

    tasks: list[Task] = Relationship(
        back_populates="project",
    )


class ProjectMember(SQLModel, table=True):
    """
    M2M между проектами и пользователями. Не обязательно хранит связь с владельцем проекта, только с
    исполнителями. Владелец проекта может быть исполнителем, но не обязан.
    """

    project_id: uuid.UUID = Field(
        foreign_key="project.id",
        primary_key=True,
        nullable=False,
        ondelete="CASCADE",
    )
    user_id: uuid.UUID = Field(
        foreign_key="user.id",
        primary_key=True,
        nullable=False,
        index=True,
        ondelete="CASCADE",
    )

    project: Project = Relationship(back_populates="members")
    user: User = Relationship(back_populates="project_memberships")
