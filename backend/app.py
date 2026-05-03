import os
from datetime import datetime

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)


BACKEND_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Hello Flask Backend</title>
    <style>
        * {
            box-sizing: border-box;
        }

        :root {
            color-scheme: light;
            --ink: #17202a;
            --muted: #526271;
            --line: rgba(23, 32, 42, 0.12);
            --blue: #1971c2;
            --green: #2a9d8f;
            --gold: #f4b942;
            --panel: rgba(255, 255, 255, 0.84);
        }

        body {
            min-height: 100vh;
            margin: 0;
            color: var(--ink);
            background:
                radial-gradient(circle at 16% 10%, rgba(42, 157, 143, 0.22), transparent 24rem),
                radial-gradient(circle at 84% 4%, rgba(244, 185, 66, 0.28), transparent 21rem),
                linear-gradient(135deg, #f7fbff 0%, #eef5f2 52%, #fff8ed 100%);
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                "Segoe UI", sans-serif;
        }

        main {
            width: min(100%, 72rem);
            min-height: 100vh;
            margin: 0 auto;
            padding: clamp(1rem, 3vw, 2.5rem);
            display: grid;
            align-content: center;
            gap: 1rem;
        }

        .hero {
            padding: clamp(1.5rem, 5vw, 4rem);
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            box-shadow: 0 24px 70px rgba(23, 32, 42, 0.14);
            backdrop-filter: blur(18px);
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 1.35rem;
            padding: 0.5rem 0.8rem;
            border: 1px solid rgba(42, 157, 143, 0.28);
            border-radius: 999px;
            color: #24796f;
            background: rgba(42, 157, 143, 0.1);
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .status-dot {
            width: 0.55rem;
            height: 0.55rem;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 0 0.25rem rgba(42, 157, 143, 0.16);
        }

        h1 {
            max-width: 12ch;
            margin: 0;
            font-size: clamp(3rem, 9vw, 6.5rem);
            line-height: 0.96;
            letter-spacing: 0;
        }

        .intro {
            max-width: 42rem;
            margin: 1.25rem 0 0;
            color: var(--muted);
            font-size: 1.16rem;
            line-height: 1.65;
        }

        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1.75rem;
        }

        a {
            color: inherit;
        }

        .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 2.9rem;
            padding: 0.85rem 1rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 850;
        }

        .primary {
            color: white;
            background: var(--blue);
            box-shadow: 0 12px 28px rgba(25, 113, 194, 0.22);
        }

        .secondary {
            border: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.72);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
        }

        .card {
            min-height: 12rem;
            padding: 1.15rem;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.76);
            box-shadow: 0 14px 42px rgba(23, 32, 42, 0.08);
        }

        .label {
            display: block;
            margin-bottom: 0.75rem;
            color: var(--blue);
            font-size: 0.78rem;
            font-weight: 850;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        h2 {
            margin: 0;
            font-size: 1.35rem;
            letter-spacing: 0;
        }

        .card p {
            margin: 0.7rem 0 0;
            color: var(--muted);
            line-height: 1.55;
        }

        code,
        pre {
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
        }

        code {
            color: #114b7c;
            font-weight: 750;
        }

        pre {
            overflow: auto;
            margin: 0.85rem 0 0;
            padding: 0.9rem;
            border: 1px solid rgba(23, 32, 42, 0.08);
            border-radius: 8px;
            color: #2c3440;
            background: #f8fbfa;
            font-size: 0.86rem;
            line-height: 1.5;
        }

        @media (max-width: 780px) {
            main {
                align-content: start;
            }

            .grid {
                grid-template-columns: 1fr;
            }

            .card {
                min-height: auto;
            }
        }
    </style>
</head>
<body>
    <main>
        <section class="hero" aria-labelledby="page-title">
            <div class="status-pill">
                <span class="status-dot" aria-hidden="true"></span>
                Flask backend online
            </div>
            <h1 id="page-title">Hello from Flask.</h1>
            <p class="intro">
                This backend is serving a friendly status page now, while the API
                stays ready for the React frontend.
            </p>
            <div class="actions" aria-label="Backend links">
                <a class="button primary" href="/api/hello">Open API response</a>
                <a class="button secondary" href="http://127.0.0.1:5174">Open frontend</a>
            </div>
        </section>

        <section class="grid" aria-label="Backend status cards">
            <article class="card">
                <span class="label">Health</span>
                <h2>Everything is green.</h2>
                <p>The service is listening on port <code>5002</code> and returning JSON from <code>/api/health</code>.</p>
            </article>
            <article class="card">
                <span class="label">Endpoint</span>
                <h2><code>GET /api/hello</code></h2>
                <p>React fetches this route and renders the backend greeting with a fresh timestamp.</p>
            </article>
            <article class="card">
                <span class="label">Preview</span>
                <h2>Sample JSON</h2>
                <pre>{
  "message": "Hello from the Flask backend!",
  "timestamp": "{{ timestamp }}"
}</pre>
            </article>
        </section>
    </main>
</body>
</html>
"""


@app.after_request
def add_cors_headers(response):
    frontend_origin = os.environ.get("FRONTEND_ORIGIN", "*")

    response.headers["Access-Control-Allow-Origin"] = frontend_origin
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


@app.get("/")
def home():
    return render_template_string(
        BACKEND_PAGE,
        timestamp=datetime.now().strftime("%I:%M:%S %p"),
    )


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/hello")
def hello():
    return jsonify(
        {
            "message": "Hello from the Flask backend!",
            "detail": "React fetched this message from the separate Flask API.",
            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5002)
