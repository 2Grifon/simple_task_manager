from celery import Celery

from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "simple_task_manager",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
    worker_max_tasks_per_child=settings.CELERY_MAX_TASKS_PER_CHILD,
    enable_utc=settings.CELERY_ENABLE_UTC,
    timezone=settings.CELERY_TIMEZONE,
)

celery_app.autodiscover_tasks(["app.tasks"])

celery_app.conf.beat_schedule = {
    "parse-index-price": {
        "task": "app.tasks.parse_index_price.parse_index_price",
        "schedule": crontab(minute="*"),
    },
    "clear-old-prices": {
        "task": "app.tasks.clear_old_prices.clear_old_prices",
        "schedule": crontab(hour=0, minute=0),
    },
}
