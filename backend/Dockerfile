FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY alembic.ini ./
COPY app ./app

RUN pip install --no-cache-dir .

EXPOSE 8000
