from flask import Flask, render_template, jsonify, request
import json
import random
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect("leaderboard.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- LOAD QUESTIONS ----------
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- HOME ----------
@app.route("/")
def index():
    return render_template("quiz.html")

# ---------- QUESTIONS API ----------
@app.route("/get_questions", methods=["POST"])
def get_questions():
    data = request.json or {}
    category = data.get("category", "").lower()
    difficulty = data.get("difficulty", "").lower()

    questions = load_questions()

    filtered = [
        q for q in questions
        if q["category"].lower() == category
        and q["difficulty"].lower() == difficulty
    ]

    random.shuffle(filtered)
    return jsonify(filtered)

# ---------- SAVE SCORE ----------
@app.route("/save_score", methods=["POST"])
def save_score():
    data = request.json
    name = data.get("name")
    score = data.get("score")

    conn = get_db()
    conn.execute(
        "INSERT INTO leaderboard (name, score) VALUES (?, ?)",
        (name, score)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

# ---------- GET LEADERBOARD ----------
@app.route("/leaderboard")
def leaderboard():
    conn = get_db()
    rows = conn.execute(
        "SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT 10"
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    app.run(debug=True)
