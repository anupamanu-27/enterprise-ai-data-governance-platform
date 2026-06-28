# Lesson 15: Lineage

## Goal

Add lineage to the metadata catalog.

Lineage explains where data came from, how it moved, and which downstream assets depend on it.

This lesson adds lineage for:

- raw tables
- dbt staging models
- dbt marts
- governance metadata

## Why This Matters

In an enterprise platform, lineage helps teams answer:

- If this table breaks, what dashboards or marts are affected?
- Where did this field come from?
- Which raw sources feed this trusted dataset?
- Can I trace sensitive data into downstream models?
- Which datasets should be checked before changing a pipeline?

## Example

The customer revenue mart has this lineage:

```text
raw.customers
  -> analytics_staging.stg_customers
  -> analytics_marts.mart_customer_revenue

raw.sales_orders
  -> analytics_staging.stg_sales_orders
  -> analytics_marts.mart_customer_revenue
```

## Run The Catalog Builder

Build the metadata catalog:

```powershell
.\.venv\Scripts\python.exe scripts\build_metadata_catalog.py
```

The generated catalog includes:

```text
lineage_graph
assets[].lineage.upstream_assets
assets[].lineage.downstream_assets
assets[].lineage.all_upstream_assets
assets[].lineage.upstream_edges
assets[].lineage.downstream_edges
```

## Production Mindset

This lesson uses a maintained lineage map.

That is a good first step because it is explicit and easy to test.

In production, lineage can also come from:

- dbt `manifest.json`
- Airflow DAG metadata
- warehouse query logs
- Spark job metadata
- OpenLineage or Marquez

For this project, lineage is now catalog-ready and can later be used by the RAG assistant.

## Interview Questions

1. What is data lineage?
2. What is the difference between upstream and downstream lineage?
3. Why is lineage important for impact analysis?
4. How does lineage help with PII governance?
5. How can dbt generate lineage automatically?

## Best Practices

- Track both upstream and downstream dependencies.
- Keep lineage close to catalog metadata.
- Use lineage for impact analysis before schema changes.
- Combine lineage with PII and quality metadata.
- Prefer automated lineage when the platform becomes larger.

## Commit

```text
feat: add lineage metadata to catalog assets
```
