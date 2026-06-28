# Lesson 10: Delta Lake

## Goal

Create the first lakehouse table using Delta Lake.

This lesson adds:

- A Delta Lake Spark job
- A curated Delta table
- A real transaction log under `_delta_log`

## Why This Matters

Plain CSV and Parquet files are useful, but enterprise data platforms need stronger guarantees.

Delta Lake adds lakehouse features on top of data files:

- ACID-style transactions
- Table history through a transaction log
- Safer overwrites
- Schema enforcement and evolution patterns
- Better reliability for repeated pipeline runs

## Input

```text
data/samples/marketing_campaigns.csv
```

## Output

```text
data/curated/delta/campaign_summary/
```

The generated output is ignored by Git. We commit the code that creates the table, not the table files.

## Run Delta Job

```powershell
docker compose run --rm spark /opt/spark/bin/spark-submit --packages io.delta:delta-spark_2.12:3.2.0 --conf "spark.jars.ivy=/tmp/.ivy2" --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" jobs/spark/build_campaign_delta_table.py
```

## Check Delta Output

```powershell
Get-ChildItem data/curated/delta/campaign_summary
```

You should see:

```text
_delta_log
part-...
```

`_delta_log` is the important difference. It stores table transaction metadata.

## Production Mindset

In production, lakehouse tables help teams avoid fragile file processing.

Instead of treating a folder as random files, a lakehouse table gives the data platform a managed table abstraction.

This helps with:

- Reliable batch jobs
- Repeatable transformations
- Safer downstream consumption
- Table-level governance
- Better metadata capture
- Future quality checks

## Local to Cloud Mapping

```text
Local Delta folder -> S3 Delta table
Spark container    -> AWS Glue / EMR / Databricks
Local curated data -> governed lakehouse layer
```

## Interview Questions

1. What problem does Delta Lake solve?
2. What is a transaction log?
3. How is a Delta table different from plain Parquet files?
4. Why is ACID important in data lakes?
5. Why should generated Delta files not be committed to Git?
6. How would this map to S3 in AWS?
7. What is a curated lakehouse table?

## Best Practices

- Keep raw data unchanged.
- Write curated data into managed lakehouse tables.
- Commit transformation code, not generated table files.
- Use predictable table paths.
- Use orchestration to run lakehouse jobs.
- Add quality checks after table creation.

## Suggested Commit

```text
feat: add delta lake table for curated campaign data
```
