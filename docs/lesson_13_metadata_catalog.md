# Lesson 13: Metadata Catalog

## Goal

Build the first metadata catalog for the governance platform.

The catalog combines:

- discovered Postgres tables
- column-level technical metadata
- business ownership metadata
- glossary terms
- Great Expectations quality results
- trust score bands

## Why This Matters

A data catalog helps people answer:

- What data exists?
- Who owns it?
- What does it mean?
- Does it contain PII?
- Can I trust it?
- Which columns are available?

This is the foundation for enterprise governance and future RAG search.

## Run The Catalog Builder

Make sure dbt marts and quality reports exist:

```powershell
docker compose run --rm dbt run
.\.venv\Scripts\python.exe scripts\run_quality_checks.py
```

Build the metadata catalog:

```powershell
.\.venv\Scripts\python.exe scripts\build_metadata_catalog.py
```

The generated catalog is written to:

```text
data/catalog/metadata_catalog.json
```

The file is ignored by Git because it is generated output.

## Production Mindset

In real companies, catalogs combine technical metadata with business metadata.

Technical metadata usually comes from systems like:

- databases
- data warehouses
- dbt manifests
- object storage
- orchestration tools

Business metadata usually comes from:

- data owners
- business glossaries
- privacy teams
- data governance offices

For this project, the flow is:

```text
Postgres information_schema
  + governance.data_assets
  + governance.business_glossary
  + Great Expectations report
  -> metadata catalog JSON
```

## Interview Questions

1. What is a data catalog?
2. What is the difference between technical metadata and business metadata?
3. Why should quality results be visible in a catalog?
4. How do ownership and glossary terms improve data discovery?
5. How could this catalog power a RAG assistant later?

## Best Practices

- Do not rely only on table names for meaning.
- Always include owners and business domains.
- Show quality and trust status close to the asset.
- Store generated catalog output in a machine-readable format.
- Keep catalog generation repeatable and automatable.

## Commit

```text
feat: build metadata catalog from governance assets
```
