# Lesson 6: MinIO (S3-Compatible Object Storage)

## Goal

Add local S3-compatible object storage to the platform using MinIO.

This lesson adds:

- MinIO service
- MinIO console
- Automatic bucket creation
- Local buckets for raw, curated, and document data

## Why This Matters

Modern data platforms separate compute from storage. Files, documents, exports, and lakehouse tables are often stored in object storage.

In AWS, that storage is usually S3. Locally, MinIO gives us an S3-compatible system without cloud cost.

## Buckets

```text
raw
curated
documents
```

`raw` stores source files as received.

`curated` stores cleaned or transformed datasets.

`documents` stores policy PDFs, glossary documents, and other unstructured files used later for RAG.

## Start MinIO

```powershell
docker compose up -d minio create-minio-buckets
```

## Check Services

```powershell
docker compose ps
```

## MinIO Console

Open:

```text
http://localhost:9001
```

Login:

```text
Username: minioadmin
Password: minioadmin
```

These are local development credentials only.

## List Buckets

```powershell
docker compose run --rm create-minio-buckets
```

## Production Mindset

Companies use object storage for:

- Raw ingestion files
- Curated analytics datasets
- Data lakehouse tables
- Document storage
- ML training data
- Data exports
- Pipeline checkpoints

In production, teams care about:

- Encryption
- Bucket policies
- IAM access
- Lifecycle rules
- Versioning
- Cost controls
- Data retention
- Audit logs

MinIO teaches the S3 pattern locally. Later, this maps cleanly to AWS S3.

## Local to AWS Mapping

```text
MinIO raw bucket       -> S3 raw bucket
MinIO curated bucket   -> S3 curated bucket
MinIO documents bucket -> S3 documents bucket
```

## Interview Questions

1. What is object storage?
2. Why do data platforms use S3 or S3-compatible storage?
3. What is the difference between object storage and a relational database?
4. Why separate raw and curated buckets?
5. What kind of data should go into a documents bucket for RAG?
6. What is bucket versioning?
7. Why should production buckets use IAM and encryption?

## Best Practices

- Separate raw, curated, and document data.
- Do not store secrets in buckets.
- Keep bucket creation repeatable.
- Use environment variables for local credentials.
- Treat local credentials as development-only.

## Suggested Commit

```text
feat: add minio object storage for local data lake
```

