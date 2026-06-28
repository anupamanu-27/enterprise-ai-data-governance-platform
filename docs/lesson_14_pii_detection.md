# Lesson 14: PII Detection and Classification

## Goal

Add column-level PII detection to the metadata catalog.

PII means Personally Identifiable Information. It is data that can identify a real person directly or indirectly.

This lesson classifies columns such as:

- `email`
- `phone`
- `full_name`
- `customer_id`

It also marks non-PII business-sensitive columns such as:

- `net_amount`
- `total_revenue`
- `trust_score`

## Why This Matters

Enterprise governance platforms must help teams understand sensitive data risk.

Before data is used for analytics, AI, or RAG, teams need to know:

- which tables contain PII
- which columns are sensitive
- which assets need masking or access control
- which data should not be sent directly to an LLM

## Run The PII-Enabled Catalog

Build the metadata catalog:

```powershell
.\.venv\Scripts\python.exe scripts\build_metadata_catalog.py
```

The generated catalog includes:

```text
pii_summary
columns[].is_pii
columns[].pii_type
columns[].sensitivity
columns[].classification_reason
```

## Production Mindset

This lesson uses deterministic rules.

That is intentional. In production, rule-based PII detection is usually the first layer because it is:

- explainable
- testable
- fast
- easy to audit

Later, teams can add ML or LLM-based detection for messy data and free text.

## Interview Questions

1. What is PII?
2. What is the difference between direct and indirect PII?
3. Why is `customer_id` often treated as sensitive?
4. Why should a catalog show column-level sensitivity?
5. Why should PII be controlled before sending data to an LLM?

## Best Practices

- Classify sensitive data at the column level.
- Keep classification rules explainable.
- Separate PII from business-sensitive data.
- Store the reason for every classification.
- Use PII flags later for masking, access control, and AI safety.

## Commit

```text
feat: add pii classification to metadata catalog
```
