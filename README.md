# Enterprise AI Data Governance & Catalog Platform

An enterprise-grade AI data governance and catalog platform that combines metadata management, data quality, PII detection, lineage, vector search, and RAG to help teams discover trusted data assets and answer governance questions with citations.

## Project Goals

- Build a local-first data platform.
- Practice production-style data engineering.
- Create a strong GitHub portfolio project.
- Prepare for data engineering, analytics engineering, and AI platform interviews.
- Design a system that can later map to AWS and Snowflake.

## Core Capabilities

- Data ingestion
- Local object storage
- Data transformation
- Data quality checks
- Metadata cataloging
- PII classification
- Trust scoring
- Semantic search
- RAG assistant
- API and UI layers
- Local Docker deployment
- Cloud migration design

## Planned Stack

- Python
- Docker
- Postgres
- MinIO
- Spark or PySpark
- Dagster
- Delta Lake or Apache Iceberg
- dbt Core
- Great Expectations
- Qdrant
- LlamaIndex
- Ollama
- FastAPI
- Streamlit or React

## Folder Structure

```text
enterprise-ai-data-governance-platform/
  apps/
  data/
  docker/
  docs/
  orchestration/
  quality/
  scripts/
  services/
  tests/
  transformations/
```

## Learning Rules

1. Never copy code without understanding it.
2. Every lesson ends with a GitHub commit.
3. Every component is explained with a production mindset.
4. Every lesson includes interview questions and real-world scenarios.
5. Every feature connects to the final enterprise platform.

## Current Status

Lesson 1: Environment Setup - complete

Lesson 2: Git & GitHub - complete

Lesson 3: Python Project Structure - complete

Lesson 4: Docker - in progress

## Development Workflow

This project follows a lesson-by-lesson Git workflow. Each lesson ends with:

- A clear summary of what changed
- A production mindset explanation
- Interview questions
- A meaningful Git commit

See [Git & GitHub Workflow](docs/git_github_workflow.md) for the project commit and repository rules.

## Local Python Commands

Run the platform health check:

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m governance_platform
```

Run tests:

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

## Docker Commands

Build the local image:

```powershell
docker build -t enterprise-ai-governance-platform:lesson-04 .
```

Run the container:

```powershell
docker run --rm enterprise-ai-governance-platform:lesson-04
```
