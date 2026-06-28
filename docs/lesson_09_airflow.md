# Lesson 9: Airflow

## Goal

Add Airflow as the orchestration layer for the platform.

This lesson adds:

- Airflow service in Docker Compose
- A governance pipeline DAG
- Local asset validation tasks
- Scheduling, dependency, retry, and monitoring concepts

## Why This Matters

Data platforms are not just scripts. In companies, pipelines need to run in the correct order, on a schedule, with retries, logs, and visibility.

Airflow helps teams answer:

- What ran?
- When did it run?
- Did it fail?
- Which task failed?
- Should it retry?
- What depends on what?

## DAG

```text
governance_catalog_pipeline
```

The DAG currently checks:

1. Raw campaign source file exists and has valid columns.
2. Curated Spark output exists and has data rows.
3. A pipeline summary file can be written.

## Local Run

Start Airflow:

```powershell
docker compose up -d airflow
```

Open the UI:

```text
http://localhost:8080
```

Airflow standalone prints the generated admin password in container logs:

```powershell
docker compose logs airflow
```

List DAGs:

```powershell
docker compose exec airflow airflow dags list
```

Test a task:

```powershell
docker compose exec airflow airflow tasks test governance_catalog_pipeline validate_campaign_source 2026-06-28
```

## Production Mindset

In this local lesson, Airflow validates assets that were created by earlier lessons.

In production, these same task slots would usually trigger:

- Ingestion containers
- Spark jobs
- dbt transformations
- Data quality checks
- Catalog metadata updates
- RAG indexing jobs
- Alerts when something fails

Airflow is task-oriented. It is very strong for scheduled workflows, retries, backfills, alerting, and operational visibility.

## Airflow vs Dagster

Airflow thinks mainly in tasks:

```text
extract -> load -> transform -> check -> publish
```

Dagster thinks mainly in data assets:

```text
raw.customers -> curated.customer_summary -> quality.customer_score
```

For this project, we are using Airflow because it is widely used in enterprise data engineering and is important for interviews.

## Interview Questions

1. What problem does Airflow solve?
2. What is a DAG?
3. What is a task?
4. What is the difference between a schedule and a manual run?
5. Why are retries important?
6. What is backfilling?
7. How would Airflow trigger a Spark job in production?

## Best Practices

- Keep DAG files small and readable.
- Make tasks idempotent.
- Avoid hard-coding secrets in DAGs.
- Use retries for transient failures.
- Use clear task names.
- Do not put heavy business logic directly in DAG files.
- Keep reusable logic in normal Python modules.

## Suggested Commit

```text
feat: orchestrate data pipeline with airflow
```

