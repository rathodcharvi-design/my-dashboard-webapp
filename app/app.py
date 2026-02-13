from flask import Flask, jsonify
import os
import time
import socket

# Configure static folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)

START = time.time()

@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>My Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 0;
            }}

            .container {{
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }}

            .header {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 30px;
            }}

            .header img {{
                width: 50px;
            }}

            h1 {{
                margin: 0;
                font-size: 30px;
            }}

            .card {{
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            }}

            .row {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }}

            .row:last-child {{
                border-bottom: none;
            }}

            .left {{
                display: flex;
                align-items: center;
                gap: 10px;
                font-weight: 600;
            }}

            .left img {{
                width: 22px;
            }}

            a {{
                color: #0077ff;
                text-decoration: none;
            }}

            .links {{
                margin-top: 15px;
                font-size: 14px;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <div class="header">
                <img src="/static/do-logo.svg">
                <h1>My Dashboard</h1>
            </div>

            <div class="card">

                <div class="row">
                    <div class="left">
                        <img src="/static/kubernetes.svg">
                        Platform
                    </div>
                    <div>DOKS (Kubernetes)</div>
                </div>

                <div class="row">
                    <div class="left">
                        <img src="/static/pod-icon.svg">
                        Pod (hostname)
                    </div>
                    <div>{socket.gethostname()}</div>
                </div>

                <div class="row">
                    <div class="left">
                        <img src="/static/pod-icon.svg">
                        Service
                    </div>
                    <div>my-dashboard</div>
                </div>

                <div class="row">
                    <div class="left">
                        <img src="/static/pod-icon.svg">
                        Version
                    </div>
                    <div>{os.getenv("APP_VERSION", "dev")}</div>
                </div>

                <div class="row">
                    <div class="left">
                        <img src="/static/pod-icon.svg">
                        Environment
                    </div>
                    <div>{os.getenv("ENVIRONMENT", "local")}</div>
                </div>

                <div class="row">
                    <div class="left">
                        <img src="/static/pod-icon.svg">
                        Uptime (seconds)
                    </div>
                    <div>{int(time.time() - START)}</div>
                </div>

                <div class="links">
                    Health endpoints:
                    <a href="/healthz">/healthz</a> |
                    <a href="/readyz">/readyz</a> |
                    <a href="/status">/status</a>
                </div>

            </div>
        </div>
    </body>
    </html>
    """

@app.route("/healthz")
def healthz():
    return jsonify(status="alive"), 200

@app.route("/readyz")
def readyz():
    return jsonify(status="ready"), 200

@app.route("/status")
def status():
    return jsonify(
        service="my-dashboard",
        hostname=socket.gethostname(),
        uptime_seconds=int(time.time() - START),
        environment=os.getenv("ENVIRONMENT", "local"),
        version=os.getenv("APP_VERSION", "dev")
    ), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

