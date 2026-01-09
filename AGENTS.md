# AGENTS.md

## Purpose
This repo is the default control hub for Codex CLI. Use these rules unless a target repo has its own AGENTS.md.

## Primary Repos
- /Users/martin/Documents/adrez/dbt-cloud
- /Users/martin/Documents/adrez/data-factory
- /Users/martin/Documents/adrez/data-platform
- /Users/martin/Documents/adrez/extractor-spreadsheets

Default scope is /Users/martin/Documents/adrez. Look outside only if needed to solve the task or when asked.
Do not inspect /Users/martin/Documents/adrez/old unless explicitly asked.

## Style
- Short direct responses. Minimal filler.
- No emojis.

## Git Defaults
- Always run `git status -sb` before edits.
- Pull with `--ff-only` by default for safety.
- Do not push unless explicitly asked.
- Do not amend commits unless explicitly asked.

## Testing
- Run relevant tests or validation when changes are made.
- If tests are expensive, ask first.

## Safety
- Do not run destructive commands unless explicitly asked.
- Ask before running commands that need network access or credentials.

## Docs
- Update docs when behavior changes.
- Keep docs business friendly, not implementation heavy.
