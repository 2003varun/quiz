from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "quizbuddysecret"


# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sqlite3.connect("quiz.db", timeout=10) as db:
            cur = db.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )
            user = cur.fetchone()

        if user:
            session["user"] = username
            return redirect("/quiz")

    return render_template("login.html")


# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            with sqlite3.connect("quiz.db", timeout=10) as db:
                cur = db.cursor()
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )

            return redirect("/")

        except sqlite3.IntegrityError:
            return render_template(
                "signup.html",
                error="Username already exists!"
            )

    return render_template("signup.html")
# ---------- QUIZ ----------
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "user" not in session:
        return redirect("/")

    questions = [
        ("What is Python?", "Language", "Snake", "Car", "Game", "Language"),
        ("HTML stands for?", "Hyper Tool", "Hyper Text Markup Language", "High Text", "None",
         "Hyper Text Markup Language"),
        ("CSS is used for?", "Logic", "Styling", "Database", "Server", "Styling"),
        ("Which HTML tag is used for a paragraph?", "<para>", "<p>", "<paragraph>", "<text>", "<p>"),
        ("Which HTML tag is used to create a hyperlink?", "<link>", "<a>", "<href>", "<url>", "<a>"),
        ("Which CSS property changes text color?", "font-color", "color", "text-style", "background", "color"),
        ("Which HTML tag is used for images?", "<img>", "<image>", "<pic>", "<photo>", "<img>"),
        ("Which CSS property controls text size?", "font-size", "text-size", "size", "font-style", "font-size"),
        ("HTML is a ___ language?", "Programming", "Markup", "Database", "Styling", "Markup"),
        ("Which CSS property adds space inside an element?", "margin", "padding", "spacing", "border", "padding")
    ]

    if request.method == "POST":
        score = 0
        for i, q in enumerate(questions):
            if request.form.get(f"q{i}") == q[5]:
                score += 1

        with sqlite3.connect("quiz.db", timeout=10) as db:
            cur = db.cursor()
            cur.execute(
                "INSERT INTO scores (username, score) VALUES (?, ?)",
                (session["user"], score)
            )

        return render_template("result.html", score=score)

    return render_template("quiz.html", questions=questions)


# ---------- LEADERBOARD ----------
@app.route("/leaderboard")
def leaderboard():
    with sqlite3.connect("quiz.db") as db:
        cur = db.cursor()
        cur.execute("""
            SELECT username, MAX(score)
            FROM scores
            GROUP BY username
            ORDER BY MAX(score) DESC
        """)
        data = cur.fetchall()

    return render_template("leaderboard.html", data=data)


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
#  users login
@app.route("/users")
def users():
    with sqlite3.connect("quiz.db") as db:
        cur = db.cursor()
        cur.execute("SELECT id, username FROM users")
        users = cur.fetchall()

    return render_template("users.html", users=users)