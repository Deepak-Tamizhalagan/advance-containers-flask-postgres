from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

from .db import get_conn 

app = Flask(__name__)


LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"
handler = RotatingFileHandler(LOG_FILE, maxBytes=512_000, backupCount=2)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def log_request():
    app.logger.info(
        "REQ %s %s | body=%s",
        request.method, request.path, request.get_data(as_text=True)[:1000]
    )

@app.after_request
def log_response(response):
    app.logger.info(
        "RES %s %s | status=%s",
        request.method, request.path, response.status
    )
    return response

@app.get("/")
def health():
    return jsonify(status="ok"), 200

@app.post("/user")
def create_user():
    data = request.get_json(silent=True) or {}
    required = {"id", "first_name", "last_name"}
    if not required <= data.keys():
        return jsonify(error=f"Expected keys: {sorted(required)}"), 400

    try:
        uid = int(data["id"])
        first = str(data["first_name"]).strip()
        last = str(data["last_name"]).strip()
        if not first or not last:
            return jsonify(error="first_name/last_name cannot be empty"), 400
    except Exception as e:
        return jsonify(error=f"Bad input: {e}"), 400

    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (id, first_name, last_name) VALUES (%s, %s, %s) "
                "ON CONFLICT (id) DO UPDATE SET first_name=EXCLUDED.first_name, last_name=EXCLUDED.last_name;",
                (uid, first, last),
            )
        return jsonify(message="created", user={"id": uid, "first_name": first, "last_name": last}), 201
    except Exception as e:
        app.logger.exception("DB insert failed")
        return jsonify(error=f"database error: {e}"), 500

@app.get("/user/<int:user_id>")
def get_user(user_id: int):
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT id, first_name, last_name FROM users WHERE id=%s;", (user_id,))
            row = cur.fetchone()
            if not row:
                return jsonify(error="not found"), 404
            uid, first, last = row
            return jsonify(user={"id": uid, "first_name": first, "last_name": last}), 200
    except Exception as e:
        app.logger.exception("DB select failed")
        return jsonify(error=f"database error: {e}"), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
