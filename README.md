# ResolveAI

An AI customer support project, built step by step.

## Current functionality

A minimal FastAPI backend with:

- `GET /` — returns a message confirming the API is running.
- `/docs` — interactive API documentation.

## Run locally

Prerequisites: Git and uv.

Clone this repository, enter its directory, then install dependencies:

```bash
uv sync
```

Start the development server:

```bash
uv run uvicorn main:app --reload
```

Open:

- API: http://127.0.0.1:8000/
- Interactive documentation: http://127.0.0.1:8000/docs

Press Control + C in the terminal to stop the server.
