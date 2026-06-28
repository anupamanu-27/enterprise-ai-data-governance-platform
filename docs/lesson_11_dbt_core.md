# Lesson 11: dbt Core

## Goal

Add dbt Core for analytics engineering transformations, model tests, and documentation.

This lesson adds:

- dbt project
- Postgres profile
- Raw source definitions
- Staging models
- Mart models
- dbt tests

## Why This Matters

dbt is widely used by analytics engineering and data platform teams.

It helps teams:

- Write SQL transformations as version-controlled models
- Define source tables
- Build staging and mart layers
- Add tests like `not_null` and `unique`
- Generate documentation and lineage

## Models

Staging models:

```text
stg_customers
stg_products
stg_sales_orders
stg_support_tickets
stg_marketing_campaigns
```

Mart models:

```text
mart_customer_revenue
mart_governance_asset_health
```

## Run dbt

Make sure Postgres is running:

```powershell
docker compose up -d postgres
```

Check connection:

```powershell
docker compose run --rm dbt debug
```

Build models:

```powershell
docker compose run --rm dbt run
```

Run tests:

```powershell
docker compose run --rm dbt test
```

Generate docs:

```powershell
docker compose run --rm dbt docs generate
```

## Production Mindset

In companies, dbt often owns the transformation layer between raw data and business-ready marts.

For this project:

```text
raw Postgres tables -> dbt staging models -> dbt mart models -> quality/catalog/RAG later
```

dbt makes the project stronger because it adds:

- SQL transformation discipline
- Lineage
- Tests
- Documentation
- A clear analytics layer

## Interview Questions

1. What problem does dbt solve?
2. What is the difference between staging and mart models?
3. What is a dbt source?
4. What does `ref()` do?
5. What does `source()` do?
6. Why add `not_null` and `unique` tests?
7. How does dbt help with lineage?

## Best Practices

- Keep raw sources separate from staging models.
- Use staging models for light cleanup and renaming.
- Use marts for business-ready analytics.
- Add tests to important keys.
- Document models and columns.
- Keep SQL readable.

## Suggested Commit

```text
feat: add dbt transformations and lineage documentation
```

