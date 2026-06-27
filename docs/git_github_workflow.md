# Git & GitHub Workflow

## Goal

Use Git and GitHub like a professional engineering project, not just a file backup tool.

Every lesson should end with a meaningful commit so the project history tells a clear story of how the platform was built.

## Repository Rules

1. Commit only source code, configuration templates, and documentation.
2. Never commit secrets, passwords, tokens, `.env`, or virtual environments.
3. Keep commits small and meaningful.
4. Write commit messages that explain the purpose of the change.
5. Keep `main` stable.

## Branch Strategy

For this learning project, we will keep the workflow simple:

```text
main
```

Use `main` as the primary branch while learning. Later, when the project grows, we can add feature branches:

```text
feature/postgres-setup
feature/minio-storage
feature/data-quality
feature/rag-assistant
```

## Commit Message Style

Use this format:

```text
type: short description
```

Common types:

```text
chore: setup or maintenance work
docs: documentation changes
feat: new feature
fix: bug fix
test: tests
ci: CI/CD changes
refactor: code restructuring without behavior change
```

Examples:

```text
chore: initialize project environment and documentation
docs: add git and github workflow
feat: add postgres database service
feat: build initial ingestion pipeline
test: add validation tests for metadata parser
ci: add github actions validation workflow
```

## What Should Be Committed

Commit these:

- `README.md`
- `.gitignore`
- `.env.example`
- Source code
- Docker files
- SQL files
- dbt models
- DAGs or Dagster assets
- Tests
- Documentation

Do not commit these:

- `.env`
- `.venv/`
- Secrets
- Large raw datasets
- Generated logs
- Local cache files
- API keys

## Lesson-End Checklist

At the end of every lesson:

1. Check changed files.

```powershell
git status --short
```

2. Review what changed.

```powershell
git diff
```

3. Stage files.

```powershell
git add .
```

4. Commit with a meaningful message.

```powershell
git commit -m "type: message"
```

5. Push to GitHub.

```powershell
git push
```

## GitHub Repository Setup

Create a GitHub repository with:

```text
Repository name: enterprise-ai-data-governance-platform
Visibility: Public or Private
Initialize with README: No
Add .gitignore: No
Choose a license: Optional for now
```

Do not initialize with README because this local project already has one.

After creating the empty GitHub repository, connect it:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/enterprise-ai-data-governance-platform.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Production Mindset

Companies rely on Git because it gives teams:

- Change history
- Rollback ability
- Code review workflows
- Collaboration
- CI/CD triggers
- Release tracking

In production, Git is not optional. It is the source of truth for code, infrastructure, documentation, and deployment workflows.

## Interview Questions

1. What is the difference between Git and GitHub?
2. Why should secrets not be committed?
3. What is the purpose of `.gitignore`?
4. What is a branch?
5. What is the difference between `git add`, `git commit`, and `git push`?
6. Why do teams use pull requests?
7. What makes a good commit message?

## Common Mistakes

- Committing `.env` files.
- Committing virtual environments.
- Making huge commits with unrelated changes.
- Using unclear commit messages like `update` or `final`.
- Creating a GitHub README when the local project already has one, causing merge conflicts.

