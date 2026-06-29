# Lesson 20: AI Agent Layer

## Goal

Wrap retrieval and answer generation in an agent-style workflow.

The agent chooses a path based on the question:

- PII check
- lineage check
- catalog lookup
- general governance answer

## Why This Matters

An AI agent is more than a single prompt.

It should:

- understand the user's intent
- choose actions
- call tools
- keep an execution trace
- return an answer with citations

This lesson gives the platform an agent interface without depending on a paid LLM.

## Run The Agent

Make sure Qdrant is running and loaded:

```powershell
docker compose up -d qdrant
.\.venv\Scripts\python.exe scripts\load_qdrant.py
```

Ask the agent:

```powershell
.\.venv\Scripts\python.exe scripts\run_governance_agent.py "which tables contain customer pii"
```

Print full JSON:

```powershell
.\.venv\Scripts\python.exe scripts\run_governance_agent.py "which tables contain customer pii" --json
```

## Production Mindset

This lesson uses a deterministic planner.

That is intentional because the project should be explainable and testable.

Later, this can evolve into:

- an LLM-based router
- tool calling
- LangGraph
- OpenAI function calling
- Bedrock Agents

The agent contract stays the same:

```text
question -> intent -> actions -> tools -> cited answer
```

## Interview Questions

1. What is an AI agent?
2. What is the difference between RAG and an agent?
3. Why should an agent keep an execution trace?
4. Why start with deterministic routing?
5. What tools should a data governance agent have?

## Best Practices

- Keep agent actions observable.
- Keep the planner testable.
- Use tools with clear inputs and outputs.
- Return citations and safety notes.
- Avoid giving the agent unnecessary access.

## Commit

```text
feat: add governance agent workflow
```
