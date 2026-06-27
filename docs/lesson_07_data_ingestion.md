# Lesson 7: Data Ingestion Pipeline

## Goal

Create the first repeatable ingestion pipeline.

This lesson loads a marketing campaign CSV into:

- Postgres table: `raw.marketing_campaigns`
- MinIO object: `raw/source/marketing_campaigns.csv`

## Why This Matters

Enterprise ingestion pipelines usually do two things:

1. Preserve the raw source file.
2. Load structured data into a queryable system.

Preserving the raw file gives teams auditability and replay ability. Loading the data into Postgres gives analysts and downstream pipelines a structured table to use.

## Files Added

```text
data/samples/marketing_campaigns.csv
src/governance_platform/ingestion.py
scripts/run_ingestion.py
tests/test_ingestion.py
docs/lesson_07_data_ingestion.md
```

## Run the Pipeline

Make sure Postgres and MinIO are running:

```powershell
docker compose up -d postgres minio create-minio-buckets
```

Run ingestion:

```powershell
.\.venv\Scripts\python.exe scripts\run_ingestion.py
```

## Verify Postgres

```powershell
docker compose exec -T postgres psql -U governance_user -d governance_catalog -c "SELECT COUNT(*) FROM raw.marketing_campaigns;"
```

## Verify MinIO

```powershell
docker compose run --rm -T minio-client "mc alias set local http://minio:9000 \"$MINIO_ACCESS_KEY\" \"$MINIO_SECRET_KEY\"; mc ls local/raw/source/"
```

## Production Mindset

This is a local version of a common production ingestion pattern:

```text
source system -> raw object storage -> structured landing table -> quality checks -> curated data
```

In production, this could be implemented with:

- Airbyte
- dlt
- Kafka
- AWS Glue
- Lambda
- Step Functions
- Dagster
- Airflow

The important concepts are the same:

- Make ingestion repeatable.
- Keep raw data.
- Validate inputs.
- Load to a predictable schema.
- Make the process idempotent.
- Log what happened.

## Interview Questions

1. Why preserve raw source files?
2. What is idempotent ingestion?
3. Why load raw data before transforming it?
4. What can go wrong in a CSV ingestion pipeline?
5. Why should ingestion scripts validate required columns?
6. How would this local pipeline map to AWS?
7. What is the difference between batch ingestion and streaming ingestion?

## Best Practices

- Keep sample data small and understandable.
- Validate required columns before loading.
- Make database writes idempotent.
- Store raw files in object storage.
- Keep ingestion code testable.
- Separate ingestion from transformation.

## Suggested Commit

```text
feat: build initial data ingestion pipeline
```

