"""
Project NEON backend server.

Run:
    python backend/server.py
"""

from pathlib import Path
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

try:
    from flask import Flask, jsonify, request
except ImportError:
    Flask = None
    jsonify = None
    request = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

for import_path in (PROJECT_ROOT, DATA_DIR):
    import_path_text = str(import_path)
    if import_path_text not in sys.path:
        sys.path.insert(0, import_path_text)

try:
    from brain import generate_reply
except Exception as error:
    generate_reply = None
    BRAIN_IMPORT_ERROR = error
else:
    BRAIN_IMPORT_ERROR = None


def backend_health():
    return {
        "status": "online",
        "system": "NEON backend",
        "brain_loaded": generate_reply is not None,
    }


def make_reply(message):
    if generate_reply is None:
        return None, f"brain import failed: {BRAIN_IMPORT_ERROR}"

    try:
        reply = generate_reply(message)
    except Exception as error:
        return None, str(error)

    return str(reply or ""), None


if Flask is not None:
    app = Flask(__name__)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    @app.get("/")
    def index():
        return jsonify(backend_health())

    @app.get("/health")
    def health():
        return jsonify(backend_health())

    @app.post("/chat")
    def chat():
        data = request.get_json(silent=True) or {}
        message = str(data.get("message", "")).strip()

        if not message:
            return jsonify({"reply": ""})

        reply, error = make_reply(message)
        if error:
            return jsonify({"reply": None, "error": error}), 500

        return jsonify({"reply": reply})

else:
    app = None

    class NeonRequestHandler(BaseHTTPRequestHandler):
        def _request_path(self):
            path = urlsplit(str(self.path)).path
            return path.rstrip("/") or "/"

        def _send_json(self, payload, status=200):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self):
            self._send_json({})

        def do_GET(self):
            path = self._request_path()

            if path in ("/", "/health"):
                self._send_json(backend_health())
                return

            self._send_json({"error": "not found"}, 404)

        def do_POST(self):
            path = self._request_path()

            if path != "/chat":
                self._send_json({"error": "not found"}, 404)
                return

            length = int(self.headers.get("Content-Length", "0") or 0)
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"

            try:
                data = json.loads(raw or "{}")
            except json.JSONDecodeError:
                self._send_json({"reply": None, "error": "invalid json"}, 400)
                return

            message = str(data.get("message", "")).strip()
            if not message:
                self._send_json({"reply": ""})
                return

            reply, error = make_reply(message)
            if error:
                self._send_json({"reply": None, "error": error}, 500)
                return

            self._send_json({"reply": reply})

        def log_message(self, format, *args):
            print("[NEON SERVER]", format % args)


def run_server(host="127.0.0.1", port=5050):
    if Flask is not None:
        app.run(host=host, port=port, debug=False)
        return

    server = ThreadingHTTPServer((host, port), NeonRequestHandler)
    print(f"Project NEON backend running at http://{host}:{port}")
    print("Flask is not installed, using built-in HTTP server.")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
