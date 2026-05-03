# Backend

Flask API for the split React + Flask app.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --port 5002
```

API endpoint:

```text
http://127.0.0.1:5002/api/hello
```

## Deploy

Use this folder as the backend service root.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

Set `FRONTEND_ORIGIN` to your deployed frontend URL, or leave it unset while experimenting.
