from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- Database init ----------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Home ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- Register Page ----------
@app.route("/register")
def register():
    return render_template("register.html")

# ---------- Register Submit ----------
@app.route("/register_submit", methods=["POST"])
def register_submit():
    username = request.form["username"]
    telegram_id = request.form["telegram_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            telegram_id TEXT,
            balance INTEGER DEFAULT 0
        )
    """)

    cur.execute(
        "INSERT INTO users (username, telegram_id) VALUES (?, ?)",
        (username, telegram_id)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ---------- Dashboard ----------
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    user = conn.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    return render_template("dashboard.html", user=user)

if __name__ == "__main__":
    app.run()
