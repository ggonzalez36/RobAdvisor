# RobAdvisor

Academic MSc project in Data Science and Computational Intelligence (originally built in 2018).

This repository has been updated to make local setup and modernization easier on current Python environments.

## ✅ What was updated

- Clear setup and run documentation.
- Explicit dependencies in `requirements.txt`.
- Django configuration through environment variables.
- Modernization roadmap in `docs/MODERNIZATION_PLAN.md`.

## Requirements

- Python 3.10+
- `pip`
- Virtual environment recommended (`venv`)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment variables

Copy the example file and adjust values for your machine:

```bash
cp .env.example .env
```

Example values:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

If you do not define values:

- `DJANGO_DEBUG` defaults to `True` (development mode).
- `DJANGO_ALLOWED_HOSTS` defaults to `127.0.0.1,localhost`.

## Settings profiles

The project now uses split settings:

- `Roboadvisor1.settings.dev` for local development (default).
- `Roboadvisor1.settings.prod` for production-like runs.

Example:

```bash
DJANGO_SETTINGS_MODULE=Roboadvisor1.settings.prod python manage.py check
```

## Migrations and run

```bash
python manage.py migrate
python manage.py runserver
```

App URL:

- http://127.0.0.1:8000/

## Modernization path

Follow the phased modernization checklist in `docs/MODERNIZATION_PLAN.md`.

## Legacy project note

Because this is a legacy project, some visualization/finance dependencies may need extra adjustments depending on your OS and Python version.
