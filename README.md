# Split React + Flask

A small full-stack app split into separate frontend and backend folders.

```text
backend/    Flask API
frontend/   React frontend
```

## Run Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --port 5002
```

## Run Frontend

From another terminal:

```bash
cd frontend
python3 -m http.server 5173
```

Then open http://127.0.0.1:5173.

The frontend calls the backend at http://127.0.0.1:5002.

## Run With Docker

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:5174
```

The containerized frontend is served by nginx on port `5174`, and the Flask API
is served by gunicorn on port `5002`.
