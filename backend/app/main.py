from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

# Import all models to register them with SQLAlchemy
from app.users.models import User  # noqa: F401
from app.tracker.models import Task, Project, ProjectMember  # noqa: F401

from app.core.config import settings
from app.tracker.routes import router as task_router

app = FastAPI(
    title="Simple Task Manager API",
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

main_router = APIRouter(prefix="/api", tags=["API"])

main_router.include_router(task_router)

app.include_router(main_router)

add_pagination(app)
