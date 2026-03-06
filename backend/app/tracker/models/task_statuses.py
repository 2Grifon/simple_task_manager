from enum import Enum


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    review = "review"
    done = "done"
    cancelled = "cancelled"


# Допустимые переходы статусов — используется в service.py
ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.created: {TaskStatus.in_progress, TaskStatus.cancelled},
    TaskStatus.in_progress: {TaskStatus.review, TaskStatus.created},
    TaskStatus.review: {TaskStatus.done, TaskStatus.in_progress},
    TaskStatus.done: set(),
    TaskStatus.cancelled: set(),
}
