# Lesson 19: LLM Answer Layer

## Goal

Generate governance answers from retrieved RAG context with citations.

This lesson uses a local citation synthesizer instead of calling a paid LLM.

## Why This Matters

Retrieval gives us relevant context.

The answer layer turns that context into a user-facing response.

A production answer layer should:

- use only retrieved context
- cite sources
- keep safety notes
- avoid exposing raw sensitive values
- make the model provider replaceable

## Run The Answer Layer

Make sure Qdrant is running and loaded:

```powershell
docker compose up -d qdrant
.\.venv\Scripts\python.exe scripts\load_qdrant.py
```

Ask a governance question:

```powershell
.\.venv\Scripts\python.exe scripts\answer_governance_question.py "which tables contain customer pii"
```

Print the full JSON answer:

```powershell
.\.venv\Scripts\python.exe scripts\answer_governance_question.py "which tables contain customer pii" --json
```

## Production Mindset

This lesson separates retrieval from answer generation.

That is important because teams may later swap the answer provider:

- local deterministic answer generator
- Ollama
- OpenAI
- Amazon Bedrock
- Azure OpenAI

The interface stays the same:

```text
question -> retrieval context -> answer with citations
```

## Interview Questions

1. Why should RAG answers include citations?
2. Why should the LLM be told to use only retrieved context?
3. What is hallucination?
4. How does PII classification affect LLM safety?
5. Why keep model providers replaceable?

## Best Practices

- Never answer governance questions without sources.
- Keep retrieval and generation as separate layers.
- Preserve safety warnings in the final answer.
- Log citations for auditability.
- Avoid sending raw sensitive values to external LLMs.

## Commit

```text
feat: answer governance questions with cited rag context
```
