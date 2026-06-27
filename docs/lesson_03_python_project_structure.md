# Lesson 3: Python Project Structure

## Goal

Create the first real Python package for the platform.

This lesson adds:

- A `src/` package layout
- A settings loader
- A logging setup
- A command-line health check
- Standard-library unit tests

## Why This Matters

Enterprise projects need a clean structure before they grow. Without structure, pipeline code, API code, catalog code, and AI code quickly become mixed together.

The `src/` layout keeps application code separate from tests, data, docs, and deployment files.

## Files Added

```text
pyproject.toml
src/governance_platform/__init__.py
src/governance_platform/__main__.py
src/governance_platform/cli.py
src/governance_platform/config.py
src/governance_platform/logging_config.py
tests/test_config.py
```

## Core Concepts

`pyproject.toml` stores Python project metadata.

`src/governance_platform/` is the main application package.

`config.py` reads environment variables and gives the rest of the app one typed settings object.

`logging_config.py` centralizes logging so every future service writes logs consistently.

`tests/` proves behavior and protects the project when we refactor later.

## Production Mindset

Companies separate configuration from code because local, staging, and production environments use different database hosts, ports, API keys, model names, and storage endpoints.

They centralize logging because logs are needed for debugging, monitoring, incident response, and audit trails.

They add tests early because platform code becomes risky when ingestion, quality, APIs, and AI features all depend on shared utilities.

## Commands

Run the CLI:

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m governance_platform
```

Run tests:

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

## Interview Questions

1. Why use a `src/` folder in a Python project?
2. Why should configuration come from environment variables?
3. What is the difference between source code and generated files?
4. Why is centralized logging useful in production?
5. Why add tests before the project becomes complex?

## Best Practices

- Keep source code under `src/`.
- Keep tests under `tests/`.
- Keep secrets out of code and Git.
- Use one settings object instead of reading environment variables everywhere.
- Configure logging once at application startup.

## Suggested Commit

```text
feat: add python project structure and base utilities
```

