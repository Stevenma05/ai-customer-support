# ResolveAI

An AI customer support project, built step by step.

## Current functionality

A minimal FastAPI backend with:

- `GET /` — returns a message confirming the API is running.
- `/docs` — interactive API documentation.
- `POST /chat` — accepts a required text message and returns a fixed reply.
  Leading and trailing whitespace is removed; empty or whitespace-only
  messages are rejected with HTTP 422.

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

## Test the chat endpoint

With the server running, open http://127.0.0.1:8000/docs.

Expand `POST /chat`, click **Try it out**, and submit:

```json
{ "message": "How do I reset my password?" }
```

Expected response: HTTP 200 with:

```json
{ "reply": "Thanks for your message. Support is on the way." }
```

Requests with a missing, empty, or whitespace-only message return HTTP 422.

The reply is currently fixed; no AI model is connected yet.

## Run tests

Install the project dependencies, including development tools:

```bash
uv sync
```

Run the automated tests:

```bash
uv run python -m pytest -v
```

The tests check that `/chat` accepts a valid message and rejects missing,
empty, and whitespace-only messages. No running server or API key is needed.

## Configure OpenAI

Copy the example configuration:

```bash
cp .env.example .env
```

Open `.env` and set `OPENAI_API_KEY` to your own OpenAI API key.
The application loads this file using python-dotenv.

Real chat requests use the OpenAI API and incur usage charges.
Automated endpoint tests replace the AI function and make no OpenAI requests.
