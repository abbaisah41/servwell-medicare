from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "servwell_secret"

DATABASE = "database.db"


# ---------------- DATABASE ---------------- #
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            qty INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------------- LOGIN ---------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------------- DASHBOARD ---------------- #
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    if request.method == "POST":
        name = request.form["name"]
        qty = request.form["qty"]
        price = request.form["price"]

        conn.execute(
            "INSERT INTO medicines (name, qty, price) VALUES (?, ?, ?)",
            (name, qty, price),
        )
        conn.commit()

    medicines = conn.execute("SELECT * FROM medicines").fetchall()
    conn.close()

    return render_template("dashboard.html", medicines=medicines)


# ---------------- SELL ---------------- #
@app.route("/sell/<int:id>")
def sell(id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    medicine = conn.execute(
        "SELECT * FROM medicines WHERE id=?", (id,)
    ).fetchone()

    if medicine and medicine["qty"] > 0:
        conn.execute(
            "UPDATE medicines SET qty = qty - 1 WHERE id=?", (id,)
        )
        conn.commit()

    conn.close()
    return redirect(url_for("dashboard"))


# ---------------- LOGOUT ---------------- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
