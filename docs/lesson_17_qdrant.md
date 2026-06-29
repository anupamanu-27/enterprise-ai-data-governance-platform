# Lesson 17: Qdrant Vector Database

## Goal

Load catalog embeddings into Qdrant and run semantic search.

Qdrant is a vector database. It stores vectors and returns the most similar records for a query vector.

## Why This Matters

Embeddings alone are just files.

To build RAG, we need a vector database that can:

- store embedding vectors
- store payload metadata
- search by semantic similarity
- return source text for citations

## Run Qdrant

Start Qdrant:

```powershell
docker compose up -d qdrant
```

Open the Qdrant dashboard:

```text
http://localhost:6333/dashboard
```

## Load Embeddings

Build the catalog and embeddings first:

```powershell
.\.venv\Scripts\python.exe scripts\build_metadata_catalog.py
.\.venv\Scripts\python.exe scripts\build_embeddings.py
```

Load Qdrant:

```powershell
.\.venv\Scripts\python.exe scripts\load_qdrant.py
```

Search Qdrant:

```powershell
.\.venv\Scripts\python.exe scripts\search_qdrant.py "which tables contain customer pii"
```

## Production Mindset

In production, Qdrant would usually run as:

- Qdrant Cloud
- a container service on ECS or Kubernetes
- a managed vector store alternative such as OpenSearch Serverless

The important pattern is:

```text
catalog metadata -> chunks -> embeddings -> vector database -> semantic search -> RAG
```

## Interview Questions

1. What is a vector database?
2. Why do RAG systems need vector search?
3. What is stored in a vector payload?
4. Why should search results include source text?
5. How can metadata filters improve retrieval?

## Best Practices

- Store source text with each vector for citations.
- Store metadata such as asset ID, chunk type, owner, and PII flags.
- Keep collection names stable.
- Rebuild the collection when the embedding model changes.
- Secure Qdrant before exposing it outside local development.

## Commit

```text
feat: load catalog embeddings into qdrant
```
