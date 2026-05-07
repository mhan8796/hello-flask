import os
from datetime import datetime

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)


HOME_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Hello Flask Backend</title>
    <style>
        body {
            margin: 0;
            padding: 3rem;
            color: #17202a;
            background: #f7fbff;
            font-family: system-ui, sans-serif;
        }
        main {
            max-width: 42rem;
            margin: 0 auto;
        }
        h1 {
            margin: 0;
            font-size: 2.5rem;
        }
        section {
            margin-top: 1.5rem;
            padding: 1rem;
            border: 1px solid #d8e2ea;
            border-radius: 8px;
            background: white;
        }
        pre {
            overflow: auto;
            padding: 1rem;
            border-radius: 8px;
            background: #eef4f8;
        }
    </style>
</head>
<body>
    <main>
        <h1>Hello from Flask</h1>
        <p>The backend is running. The React frontend can call the API routes below.</p>

        <section>
            <h2>Routes</h2>
            <ul>
                <li><a href="/api/health">GET /api/health</a></li>
                <li><a href="/api/hello">GET /api/hello</a></li>
            </ul>
        </section>

        <section>
            <h2>Sample response</h2>
            <pre>{{ sample_response }}</pre>
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
        HOME_PAGE,
        sample_response=hello_response(),
    )


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/hello")
def hello():
    return jsonify(hello_response())


def hello_response():
    return {
        "message": "Hello from the Flask backend!",
        "detail": "React fetched this message from the separate Flask API.",
        "timestamp": datetime.now().strftime("%I:%M:%S %p"),
    }


if __name__ == "__main__":
    app.run(debug=True, port=5002)
