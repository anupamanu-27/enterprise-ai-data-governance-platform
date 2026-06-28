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

Lesson 4: Docker - complete

Lesson 5: Postgres - complete

Lesson 6: MinIO - complete

Lesson 7: Data Ingestion Pipeline - complete

Lesson 8: Spark / PySpark - complete

Lesson 9: Airflow - complete

Lesson 10: Delta Lake - complete

Lesson 11: dbt Core - complete

Lesson 12: Great Expectations - complete

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

## Postgres Commands

Start local Postgres:

```powershell
docker compose up -d postgres
```

Check local Postgres:

```powershell
docker compose exec -T postgres psql -U governance_user -d governance_catalog -c "SELECT COUNT(*) FROM raw.customers;"
```

Stop local Postgres:

```powershell
docker compose down
```

## MinIO Commands

Start local MinIO and create buckets:

```powershell
docker compose up -d minio create-minio-buckets
```

Open the MinIO console:

```text
http://localhost:9001
```

Local login:

```text
Username: minioadmin
Password: minioadmin
```

## Data Ingestion Command

Run the first ingestion pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\run_ingestion.py
```

## Spark Command

Run the campaign summary Spark job:

```powershell
docker compose run --rm spark /opt/spark/bin/spark-submit jobs/spark/build_campaign_summary.py
```

## Airflow Commands

Start Airflow:

```powershell
docker compose up -d airflow
```

Open Airflow:

```text
http://localhost:8080
```

List DAGs:

```powershell
docker compose exec airflow airflow dags list
```

## Delta Lake Command

Build the curated campaign Delta table:

```powershell
docker compose run --rm spark /opt/spark/bin/spark-submit --packages io.delta:delta-spark_2.12:3.2.0 --conf "spark.jars.ivy=/tmp/.ivy2" --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" jobs/spark/build_campaign_delta_table.py
```

## dbt Commands

Check dbt connection:

```powershell
docker compose run --rm dbt debug
```

Run dbt models:

```powershell
docker compose run --rm dbt run
```

Run dbt tests:

```powershell
docker compose run --rm dbt test
```

## Great Expectations Commands

Install project dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Run data quality checks:

```powershell
$env:PYTHONPATH="src;."
.\.venv\Scripts\python.exe scripts\run_quality_checks.py
```

The latest generated quality report is written to:

```text
quality/reports/latest_quality_report.json
```
