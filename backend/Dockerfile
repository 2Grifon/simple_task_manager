FROM python:3.12-slim


ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --yes --no-install-recommends gcc libc-dev git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend/

# Копируем только файлы, нужные для установки зависимостей
COPY pyproject.toml ./

# pip читает зависимости из pyproject.toml
RUN pip install --upgrade pip \
    && pip install .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
