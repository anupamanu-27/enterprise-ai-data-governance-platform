# Lesson 4: Docker

## Goal

Containerize the Python project so the platform health check can run the same way on any machine with Docker.

This lesson adds:

- `Dockerfile`
- `.dockerignore`
- Docker build command
- Docker run command
- Production container concepts

## Why This Matters

In real companies, data platforms do not run only on one developer laptop. They run in CI/CD, staging, production servers, Kubernetes, ECS, Airflow workers, Dagster jobs, and scheduled containers.

Docker gives us a repeatable runtime:

- Same Python version
- Same project files
- Same startup command
- Same environment variable behavior

## Files Added

```text
Dockerfile
.dockerignore
docs/lesson_04_docker.md
```

## Dockerfile Explanation

```dockerfile
FROM python:3.12-slim
```

Uses a lightweight official Python 3.12 image.

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory inside the container.

```dockerfile
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

Configures Python for container execution.

- `PYTHONPATH=/app/src` lets Python import our package.
- `PYTHONDONTWRITEBYTECODE=1` avoids creating `__pycache__` files.
- `PYTHONUNBUFFERED=1` makes logs show immediately.

```dockerfile
COPY pyproject.toml README.md ./
COPY src ./src
```

Copies only the files needed to run the current health check.

```dockerfile
CMD ["python", "-m", "governance_platform"]
```

Runs the platform CLI when the container starts.

## Build Command

```powershell
docker build -t enterprise-ai-governance-platform:lesson-04 .
```

## Run Command

```powershell
docker run --rm enterprise-ai-governance-platform:lesson-04
```

## Environment Variable Example

```powershell
docker run --rm -e APP_ENV=container enterprise-ai-governance-platform:lesson-04
```

## Production Mindset

Companies use containers because they make applications easier to:

- Build consistently
- Test in CI/CD
- Deploy to cloud platforms
- Run in Kubernetes
- Scale horizontally
- Debug across environments

For this project, Docker will eventually run:

- FastAPI service
- Streamlit or React UI
- Ingestion jobs
- Metadata jobs
- RAG indexing jobs
- Local infrastructure through Docker Compose

## Interview Questions

1. What problem does Docker solve?
2. What is the difference between an image and a container?
3. What is a `Dockerfile`?
4. Why use `.dockerignore`?
5. Why should containers write logs to stdout?
6. Why should secrets be passed through environment variables instead of copied into images?
7. What is the difference between `docker build` and `docker run`?

## Best Practices

- Keep images small.
- Do not copy `.env` files into images.
- Do not copy virtual environments into images.
- Use environment variables for configuration.
- Keep one main process per container.
- Write logs to stdout and stderr.

## Suggested Commit

```text
feat: containerize base python service
```

