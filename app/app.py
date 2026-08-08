import os
import sqlite3, random, string
from flask import Flask, request, redirect, jsonify, abort

app = Flask(__name__)
DB = "urls.db"
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS urls (
            code TEXT PRIMARY KEY,
            original TEXT NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

def gen_code(n=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "url required"}), 400
    code = data.get("alias") or gen_code()
    with get_db() as db:
        try:
            db.execute("INSERT INTO urls (code, original) VALUES (?, ?)", (code, url))
        except sqlite3.IntegrityError:
            return jsonify({"error": "alias already taken"}), 409
    return jsonify({"short": f"{BASE_URL}/{code}", "code": code}), 201

@app.route("/<code>")
def redirect_url(code):
    with get_db() as db:
        row = db.execute("SELECT original FROM urls WHERE code=?", (code,)).fetchone()
        if not row:
            abort(404)
        db.execute("UPDATE urls SET clicks=clicks+1 WHERE code=?", (code,))
    return redirect(row["original"])

@app.route("/stats/<code>")
def stats(code):
    with get_db() as db:
        row = db.execute("SELECT * FROM urls WHERE code=?", (code,)).fetchone()
        if not row:
            abort(404)
        return jsonify(dict(row))

@app.route("/<code>", methods=["DELETE"])
def delete(code):
    with get_db() as db:
        db.execute("DELETE FROM urls WHERE code=?", (code,))
    return "", 204

init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
