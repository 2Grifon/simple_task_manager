from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.tracker.models import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    project_id: uuid.UUID
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.medium
    author_id: uuid.UUID
    assignee_id: Optional[uuid.UUID] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus
    comment: Optional[str] = None
    changed_by_user_id: uuid.UUID


class TaskRetrieve(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    description: Optional[str]
    priority: TaskPriority
    status: TaskStatus
    author_id: uuid.UUID
    assignee_id: Optional[uuid.UUID]
    created_at: datetime


class TaskStatusHistoryRetrieve(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    task_id: uuid.UUID
    changed_by_user_id: uuid.UUID
    from_status: Optional[TaskStatus]
    to_status: TaskStatus
    comment: Optional[str]
    created_at: datetime


class PaginatedTasksList(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[TaskRetrieve]
