FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src

CMD ["python", "-m", "governance_platform"]

