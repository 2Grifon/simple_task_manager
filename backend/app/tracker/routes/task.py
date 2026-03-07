import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.db import SessionDep
from app.tracker.models import TaskPriority, TaskStatus
from app.tracker.schemas import (
    TaskCreate,
    TaskRetrieve,
    TaskStatusHistoryRetrieve,
    TaskStatusUpdate,
)
from app.tracker.services import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_service(session: SessionDep) -> TaskService:
    return TaskService(session)


ServiceDep = Annotated[TaskService, Depends(get_service)]


@router.post("/", response_model=TaskRetrieve, status_code=status.HTTP_201_CREATED)
async def create_task(body: TaskCreate, service: ServiceDep) -> TaskRetrieve:
    task = await service.create_task(body)
    return TaskRetrieve.model_validate(task)


@router.get("/", response_model=LimitOffsetPage[TaskRetrieve])
async def list_tasks(
    session: SessionDep,
    service: ServiceDep,
    status_filter: Optional[TaskStatus] = Query(default=None, alias="status"),
    priority: Optional[TaskPriority] = Query(default=None),
    project_id: Optional[uuid.UUID] = Query(default=None),
) -> LimitOffsetPage[TaskRetrieve]:
    query = service.get_tasks_query(
        status_filter=status_filter,
        priority=priority,
        project_id=project_id,
    )
    return await paginate(session, query)


@router.get("/{task_id}", response_model=TaskRetrieve)
async def get_task(task_id: uuid.UUID, service: ServiceDep) -> TaskRetrieve:
    task = await service.get_task(task_id)
    return TaskRetrieve.model_validate(task)


@router.patch("/{task_id}/status", response_model=TaskRetrieve)
async def update_task_status(
    task_id: uuid.UUID,
    body: TaskStatusUpdate,
    service: ServiceDep,
) -> TaskRetrieve:
    task = await service.change_status(
        task_id=task_id,
        new_status=body.status,
        changed_by_user_id=body.changed_by_user_id,
        comment=body.comment,
    )
    return TaskRetrieve.model_validate(task)


@router.get("/{task_id}/history", response_model=list[TaskStatusHistoryRetrieve])
async def get_task_history(
    task_id: uuid.UUID,
    service: ServiceDep,
) -> list[TaskStatusHistoryRetrieve]:
    history = await service.get_history(task_id)
    return history
