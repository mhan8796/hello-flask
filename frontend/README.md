# Frontend

Static React frontend for the split React + Flask app.

## Run Locally

```bash
python3 -m http.server 5173
```

Then open http://127.0.0.1:5173.

The frontend calls the Flask backend at `http://127.0.0.1:5002`.
For deployment, update `window.API_BASE_URL` in `index.html` to your deployed
backend URL.
