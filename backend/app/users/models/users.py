from sqlmodel import Field, Relationship

from app.core.base_models import UUIDModelBase, TimestampedModelBase


class User(UUIDModelBase, TimestampedModelBase, table=True):
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: str

    # Relations
    owned_projects: list["Project"] = Relationship(  # noqa F821
        back_populates="owner",
    )
    project_memberships: list["ProjectMember"] = Relationship(  # noqa F821
        back_populates="user",
        cascade_delete=True,
    )
    authored_tasks: list["Task"] = Relationship(  # noqa F821
        back_populates="author",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "[Task.author_id]"},
    )
    assigned_tasks: list["Task"] = Relationship(  # noqa F821
        back_populates="assignee",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"},
    )
    status_changes: list["TaskStatusHistory"] = Relationship(  # noqa F821
        back_populates="changed_by_user",
        cascade_delete=True,
    )
