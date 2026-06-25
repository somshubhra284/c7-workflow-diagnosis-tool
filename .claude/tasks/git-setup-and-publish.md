# Task: Git setup, publish to GitHub, and commit-task-file policy

## Goal
Publish the project to GitHub safely (no secret leak) and establish the rule
that EVERY commit has a corresponding task description under `.claude/tasks/`.

## Task list
1. [x] `.gitignore` — exclude `.env` (secret), `__pycache__/`, `.pytest_cache/`,
       `*.pyc`, venvs.
2. [x] `.env.example` — safe template (GROQ_API_KEY placeholder + optional EVAL_MODEL).
3. [x] Initial commit + push to origin/main. Verified `.env` NOT tracked.
4. [x] Fix commit author identity to GitHub creds:
       somshubhra284 <somshubhra.maity@gmail.com>. Amended + force-pushed
       (--force-with-lease). Also set globally.
5. [x] CLAUDE.md — added standing rule under "### Committing": every commit must
       have a task description file under `.claude/tasks/`.
6. [x] Commit + push this task file and the CLAUDE.md rule.

## Changes log
- `.gitignore`, `.env.example` created. `.env` confirmed untracked (no key leak).
- Commits: 69937bb (initial) -> 87bc99b (email fix) -> d50bdb4 (name fix to
  somshubhra284). Final on origin/main: d50bdb4.
- gh used as git credential helper (gh auth setup-git) to enable push from sandbox.
- This file backfills the task description for the git-setup/publish work, which
  previously had none — the trigger for the new policy below.
- (pending) CLAUDE.md rule + commit of this file.
