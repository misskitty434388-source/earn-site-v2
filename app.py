from flask import Flask, render_template, request, redirect, session
import time
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- Database init ----------
def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        telegram TEXT,
        password TEXT,
        balance INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

init_db()
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

# -------- Watch Ad Page --------
@app.route("/watch_ad")
def watch_ad():
    return render_template("watch_ad.html")


# -------- Claim Reward --------
@app.route("/claim_reward")
def claim_reward():
    conn = get_db()
    cur = conn.cursor()

    # আপাতত লাস্ট ইউজারের ব্যালেন্স বাড়াচ্ছি
    cur.execute("""
        UPDATE users
        SET balance = balance + 5
        WHERE id = (SELECT id FROM users ORDER BY id DESC LIMIT 1)
    """)

    conn.commit()
    conn.close()

    return redirect("/dashboard")
if __name__ == "__main__":
    app.run()
