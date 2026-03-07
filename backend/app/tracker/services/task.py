import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.tracker.models import (
    ALLOWED_TRANSITIONS,
    Project,
    Task,
    TaskPriority,
    TaskStatus,
    TaskStatusHistory,
)
from app.tracker.schemas import TaskCreate
from app.users.models.users import User


class TaskService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # Validation for internal use
    async def _get_user_or_400(self, user_id: uuid.UUID) -> None:
        user = await self._session.get(User, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь {user_id} не найден",
            )

    async def _get_project_or_400(self, project_id: uuid.UUID) -> None:
        project = await self._session.get(Project, project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Проект {project_id} не найден",
            )

    # Retrieve
    async def get_task(self, task_id: uuid.UUID) -> Task:
        task = await self._session.get(Task, task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача {task_id} не найдена",
            )
        return task

    def get_tasks_query(
        self,
        status_filter: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        project_id: Optional[uuid.UUID] = None,
    ):
        filters = []
        if status_filter is not None:
            filters.append(Task.status == status_filter)
        if priority is not None:
            filters.append(Task.priority == priority)
        if project_id is not None:
            filters.append(Task.project_id == project_id)

        return select(Task).where(*filters).order_by(Task.created_at.desc())

    async def get_history(self, task_id: uuid.UUID) -> list[TaskStatusHistory]:
        await self.get_task(task_id)
        result = await self._session.exec(
            select(TaskStatusHistory)
            .where(TaskStatusHistory.task_id == task_id)
            .order_by(TaskStatusHistory.created_at.asc())
        )
        return result.all()

    # Create
    async def create_task(self, data: TaskCreate) -> Task:
        await self._get_project_or_400(data.project_id)
        await self._get_user_or_400(data.author_id)
        if data.assignee_id:
            await self._get_user_or_400(data.assignee_id)

        task = Task(
            project_id=data.project_id,
            title=data.title,
            description=data.description,
            priority=data.priority,
            status=TaskStatus.created,
            author_id=data.author_id,
            assignee_id=data.assignee_id,
        )
        self._session.add(task)

        self._session.add(
            TaskStatusHistory(
                task_id=task.id,
                changed_by_user_id=data.author_id,
                from_status=None,
                to_status=TaskStatus.created,
                comment="Task created",
            )
        )

        await self._session.commit()
        await self._session.refresh(task)
        return task

    # Update
    async def change_status(
        self,
        task_id: uuid.UUID,
        new_status: TaskStatus,
        changed_by_user_id: uuid.UUID,
        comment: Optional[str] = None,
    ) -> Task:
        await self._get_user_or_400(changed_by_user_id)

        task = await self.get_task(task_id)

        allowed = ALLOWED_TRANSITIONS[task.status]
        if new_status not in allowed:
            allowed_str = ", ".join(s.value for s in allowed) or "нет"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Переход '{task.status.value}' -> '{new_status.value}' запрещён. "
                    f"Допустимые переходы: [{allowed_str}]"
                ),
            )

        self._session.add(
            TaskStatusHistory(
                task_id=task.id,
                changed_by_user_id=changed_by_user_id,
                from_status=task.status,
                to_status=new_status,
                comment=comment,
            )
        )
        task.status = new_status
        self._session.add(task)

        await self._session.commit()
        await self._session.refresh(task)
        return task
