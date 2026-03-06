from typing import Annotated, Any
from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    # CORS settings
    CORS_ORIGIN_WHITELIST: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.CORS_ORIGIN_WHITELIST.split(",")]

    # Postgres settings
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "postgres"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:

        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    # Application settings
    CORS_ORIGIN_WHITELIST: str

    MEDIA_URL: str = "/media/"

    # RabbitMQ
    RABBITMQ_PROTOCOL: str = "amqp"
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"

    # Celery
    CELERY_ACCEPT_CONTENT: list[str] = ["json"]
    CELERY_ENABLE_UTC: bool = False
    CELERY_TIMEZONE: str = "Europe/Moscow"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_MAX_TASKS_PER_CHILD: int = 1
    CELERY_RESULT_BACKEND: str = "rpc://"

    @property
    def CELERY_BROKER_URL(self) -> str:
        return (
            f"{self.RABBITMQ_PROTOCOL}://{self.RABBITMQ_USER}:"
            f"{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"
        )


settings = Settings()
