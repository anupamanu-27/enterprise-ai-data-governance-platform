# Lesson 8: Spark / PySpark

## Goal

Use Spark to process raw campaign data and create a curated analytics dataset.

This lesson adds:

- Spark service in Docker Compose
- PySpark job
- Curated campaign summary output

The local Spark runtime uses the `apache/spark:latest` Docker image.

## Why This Matters

Python scripts are fine for small files. Spark is used when data becomes too large for one machine or when companies need distributed processing.

In enterprise data platforms, Spark is commonly used for:

- Large batch processing
- Data lake transformations
- File-to-file processing
- Aggregations across large datasets
- Feature engineering
- Lakehouse table creation

## Input

```text
data/samples/marketing_campaigns.csv
```

## Output

```text
data/curated/campaign_summary/
```

The output is ignored by Git because it is generated data. The code that creates it is committed.

## Run Spark Job

```powershell
docker compose run --rm spark /opt/spark/bin/spark-submit jobs/spark/build_campaign_summary.py
```

## Check Output

```powershell
Get-ChildItem data/curated/campaign_summary
```

## What the Job Does

The job reads campaign data and creates a summary by:

- `region`
- `channel`

It calculates:

- Campaign count
- Total budget
- Average budget

## Production Mindset

This is the start of the curated layer.

In production, this pattern becomes:

```text
raw data -> Spark transformation -> curated dataset -> quality checks -> catalog metadata
```

Later, this can map to:

- AWS EMR
- AWS Glue
- Databricks
- Kubernetes Spark jobs
- Airflow or Dagster orchestration

## Interview Questions

1. What problem does Spark solve?
2. When would you use Spark instead of normal Python?
3. What is a Spark DataFrame?
4. What is the difference between raw and curated data?
5. Why should generated output not be committed to Git?
6. What does `groupBy` do in Spark?
7. Why do companies use distributed processing?

## Best Practices

- Keep raw data unchanged.
- Write transformed data to a separate curated location.
- Make output paths predictable.
- Keep processing jobs repeatable.
- Commit code, not generated data.
- Use orchestration later to schedule jobs.

## Suggested Commit

```text
feat: add spark processing job for curated datasets
```
