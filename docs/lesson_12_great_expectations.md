# Lesson 12: Great Expectations

## Goal

Add a data quality layer with Great Expectations.

This lesson validates the trusted analytics marts created by dbt:

- `analytics_marts.mart_customer_revenue`
- `analytics_marts.mart_governance_asset_health`

## Why This Matters

Enterprise data platforms cannot only move data.

They must prove that data is trustworthy before analysts, AI systems, and business users depend on it.

Great Expectations helps teams define quality rules such as:

- required columns must not be null
- IDs must be unique
- row counts must stay within expected limits
- numeric values must stay in valid ranges
- categorical values must match allowed business values

## Run Quality Checks

Make sure Postgres is running and dbt marts are built:

```powershell
docker compose up -d postgres
docker compose run --rm dbt run
```

Run the Great Expectations quality checks:

```powershell
.\.venv\Scripts\python.exe scripts\run_quality_checks.py
```

The command writes a JSON report to:

```text
quality/reports/latest_quality_report.json
```

The report is ignored by Git because it is generated output.

## Production Mindset

In production, quality checks usually run after ingestion and transformation jobs.

For this project, the quality flow is:

```text
raw Postgres tables -> dbt marts -> Great Expectations checks -> quality report -> trust score/catalog later
```

Later, this report can feed:

- catalog metadata
- trust score calculation
- Airflow alerts
- AI governance assistant answers

## Interview Questions

1. What problem does Great Expectations solve?
2. What is the difference between dbt tests and Great Expectations checks?
3. Why should quality checks run after transformation jobs?
4. How would you handle a failed data quality check in production?
5. How can quality results improve a data catalog?

## Best Practices

- Keep expectations close to the dataset they protect.
- Start with high-value checks instead of hundreds of noisy rules.
- Save quality results in a machine-readable format.
- Use failed checks to block downstream pipelines when the risk is high.
- Connect quality results to ownership, lineage, and trust scoring.

## Commit

```text
feat: add great expectations quality checks
```
