# RoboAdvisor Modernization Plan

This document proposes a pragmatic path to move a legacy 2018 codebase to a maintainable and deployable 2026-ready project.

## Phase 1 — Stabilize the technical baseline (short term)

1. **Freeze and verify environment**
   - Install using `requirements.txt`.
   - Validate Python version in CI.

2. **Environment-based secure config**
   - Keep secrets out of the repository.
   - Split settings by environment (`settings/base.py`, `settings/dev.py`, `settings/prod.py`).

3. **Repository hygiene**
   - Ignore local artifacts (`.env`, `db.sqlite3`, caches).
   - Keep `.env.example` updated.

## Phase 1 implementation status (applied)

- [x] Environment-based settings structure added (`base.py`, `dev.py`, `prod.py`).
- [x] Local defaults wired to development settings via `Roboadvisor1/settings/__init__.py`.
- [x] Python version verification and dependency install added to CI workflow (`.github/workflows/phase1-ci.yml`).
- [x] Repository hygiene files added (`.gitignore`, `.env.example`).

## Phase 2 — Upgrade Django stack

1. **Upgrade to current LTS Django**
   - Review compatibility of legacy dependencies (especially charting packages).
   - Replace unmaintained libraries with actively maintained alternatives.

2. **Refactor views and auth flows**
   - Introduce class-based views where useful.
   - Replace broad `except:` blocks with explicit exception handling.

3. **Background tasks modernization**
   - Migrate from legacy Celery APIs to modern task definitions (`@shared_task`) and explicit beat schedules.

## Phase 3 — Quality and observability

1. **Testing**
   - Add unit tests for core portfolio and transaction logic.
   - Add integration tests for key user flows.

2. **Linting and formatting**
   - Add `ruff`, `black`, and `isort`.
   - Add `pre-commit` hooks.

3. **CI/CD**
   - Add pipeline steps for dependency install, `manage.py check`, and test execution.

## Phase 4 — Data layer and performance

1. **Database**
   - Move production environments from SQLite to PostgreSQL.
   - Add indexes on frequent query paths.

2. **Financial domain architecture**
   - Extract financial logic from views into service modules.
   - Version projection logic for reproducibility.

3. **Frontend modernization**
   - Gradually modernize templates with a design system (Bootstrap/Tailwind) or a partial SPA strategy.

## Suggested backlog (priority order)

- [ ] Split settings by environment.
- [ ] Replace unmaintained dependencies.
- [ ] Add a minimum regression test suite.
- [ ] Add CI pipeline for checks and tests.
- [ ] Move non-local environments to PostgreSQL.
