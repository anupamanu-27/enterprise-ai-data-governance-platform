# Lesson 16: Embeddings

## Goal

Turn catalog metadata into searchable text chunks and local embedding vectors.

This is the first RAG foundation lesson.

The platform now converts metadata such as:

- asset name
- description
- owner
- business domain
- trust score
- PII classification
- lineage
- column profiles

into text records that can later be loaded into Qdrant.

## Why This Matters

LLMs do not automatically know your company's data catalog.

RAG solves this by:

1. turning trusted catalog metadata into searchable chunks
2. embedding those chunks as vectors
3. finding relevant chunks for a user question
4. sending only the relevant context to the LLM

## Run The Embedding Builder

Build the catalog first:

```powershell
.\.venv\Scripts\python.exe scripts\build_metadata_catalog.py
```

Build embeddings:

```powershell
.\.venv\Scripts\python.exe scripts\build_embeddings.py
```

The generated embedding file is written to:

```text
data/embeddings/catalog_embeddings.json
```

The file is ignored by Git because it is generated output.

## Production Mindset

This lesson uses a deterministic local hashing embedding.

That keeps the project:

- local-first
- free to run
- testable
- independent of paid APIs

In production, the embedding function can be replaced with:

- OpenAI embeddings
- Amazon Bedrock Titan embeddings
- Ollama local embeddings
- Hugging Face sentence transformers

The pipeline shape stays the same.

## Interview Questions

1. What is an embedding?
2. Why do RAG systems need chunks?
3. Why should metadata be filtered before sending it to an LLM?
4. What is the difference between keyword search and vector search?
5. How can PII classification improve RAG safety?

## Best Practices

- Chunk metadata by useful retrieval units.
- Keep generated embeddings out of Git.
- Store enough metadata with every vector for citations.
- Avoid embedding raw sensitive data unless there is a clear governance policy.
- Make the embedding provider replaceable.

## Commit

```text
feat: generate catalog embeddings for rag search
```
