# Lesson 18: RAG Retrieval Layer

## Goal

Turn Qdrant search results into structured RAG context.

This lesson does not call an LLM yet. It prepares the context that an LLM will use later.

## Why This Matters

Raw vector search results are not enough for enterprise RAG.

A production RAG system should return:

- source text
- citation IDs
- source asset IDs
- similarity scores
- safety notes
- prompt-ready context

This lets the future AI assistant answer with citations instead of guessing.

## Run Retrieval

Make sure Qdrant is running and loaded:

```powershell
docker compose up -d qdrant
.\.venv\Scripts\python.exe scripts\load_qdrant.py
```

Retrieve RAG context:

```powershell
.\.venv\Scripts\python.exe scripts\retrieve_rag_context.py "which tables contain customer pii"
```

Print the full JSON object:

```powershell
.\.venv\Scripts\python.exe scripts\retrieve_rag_context.py "which tables contain customer pii" --json
```

## Production Mindset

In a real RAG architecture, retrieval is a separate layer.

It is responsible for:

- searching the vector database
- selecting useful chunks
- formatting citations
- controlling sensitive context
- building the final LLM prompt

For this project, the flow is:

```text
catalog -> chunks -> embeddings -> Qdrant -> RAG retrieval context -> LLM later
```

## Interview Questions

1. What is RAG?
2. Why should RAG answers include citations?
3. What is the role of the retriever?
4. Why should PII be checked before sending context to an LLM?
5. What happens if retrieval returns irrelevant chunks?

## Best Practices

- Keep retrieval separate from generation.
- Always include source IDs and citations.
- Add safety metadata before the LLM call.
- Keep prompts explicit about using only retrieved context.
- Log retrieval results for debugging and evaluation.

## Commit

```text
feat: build cited rag retrieval context
```
