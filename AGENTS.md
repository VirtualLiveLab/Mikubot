# AGENTS.md

This file provides guidance to AI Agents when working with code in this repository.

## Project Overview

Discord Bot for VirtualLiveLab, built with Python + discord.py. Uses `uv` for package management and `mise` for task running.

## Commands

```bash
mise run lint        # ruff check
mise run format      # ruff format
mise run tidy        # lint:fix + format (run before committing)
uv run main.py       # start the bot locally
```

YOU MUST CHECK `mise run lint` and `mise run format` before completing task.

## Branch and Release Strategy

- Default branch is `staging` (not `master`)
- Merge feature branches into `staging`
- Pushing to `staging` auto-generates a release PR (`master ← staging`) via `git-pr-release --squashed`
- `master` is the production branch; do not push directly

## Coding Rules

- Do not use `X | Y` union syntax — use `Optional[X]` or `Union[X, Y]` instead (UP040 is disabled for discord.py compatibility)
- Type annotations are required on all functions (`mypy disallow_untyped_defs = true`)
- No test suite is currently set up; do not suggest adding tests unless explicitly asked
