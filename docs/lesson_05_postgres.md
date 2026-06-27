# Lesson 5: Postgres

## Goal

Run a local Postgres database for the platform and load realistic enterprise sample data.

This lesson adds:

- `docker-compose.yml`
- Postgres service
- Database schemas
- Seed data for customers, products, sales orders, support tickets, data assets, and glossary terms

## Why This Matters

Postgres gives us a real relational database for local platform development.

In this project, Postgres starts as:

- Landing database for operational data
- Metadata store for governance concepts
- Practice database for SQL, ingestion, and quality checks

Later, some workloads may move to Snowflake, Redshift, Athena, or a lakehouse, but Postgres is excellent for local learning and repeatable demos.

## Schemas

```text
raw
curated
governance
```

`raw` stores source-like data.

`curated` is reserved for transformed analytics-ready data.

`governance` stores catalog-style metadata such as data assets and glossary terms.

## Tables

```text
raw.customers
raw.products
raw.sales_orders
raw.support_tickets
governance.data_assets
governance.business_glossary
```

## Start Postgres

```powershell
docker compose up -d postgres
```

## Check Containers

```powershell
docker compose ps
```

## Query the Database

```powershell
docker compose exec -T postgres psql -U governance_user -d governance_catalog -c "SELECT COUNT(*) FROM raw.customers;"
```

## Stop Postgres

```powershell
docker compose down
```

## Reset Postgres Data

Use this only when you intentionally want to delete the local database volume:

```powershell
docker compose down -v
```

## Production Mindset

Companies use relational databases for operational systems, metadata stores, application backends, audit logs, and governance workflows.

For production, teams care about:

- Backups
- Access control
- Network security
- Connection pooling
- Monitoring
- Schema migrations
- Disaster recovery
- Data retention

This local Postgres setup is not production-grade yet. It is a development database that teaches the structure and behavior we need before moving to managed cloud services.

## Interview Questions

1. What is Postgres used for in data platforms?
2. What is a schema in Postgres?
3. What is the difference between raw and curated data?
4. Why should local databases be created with repeatable scripts?
5. What is a primary key?
6. What is a foreign key?
7. Why do companies separate operational data from governance metadata?

## Best Practices

- Keep schema creation scripts in Git.
- Keep seed data small and understandable.
- Use environment variables for database credentials.
- Use separate schemas for raw, curated, and governance data.
- Do not commit database volumes or generated database files.

## Suggested Commit

```text
feat: add postgres database and sample enterprise data
```

