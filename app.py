from flask import Flask, request, redirect, session, render_template_string
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "servwell_secret_key"

DB = "database.db"


# ---------------- DATABASE ----------------
def get_db():
    return sqlite3.connect(DB)


def init_db():
    db = get_db()
    c = db.cursor()

    # users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # medicines
    c.execute("""
    CREATE TABLE IF NOT EXISTS medicines(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        qty INTEGER,
        price INTEGER
    )
    """)

    # sales
    c.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        qty INTEGER,
        total INTEGER
    )
    """)

    # default admin
    c.execute("INSERT OR IGNORE INTO users(username,password) VALUES('admin','2020')")

    db.commit()
    db.close()


init_db()


# ---------------- LOGIN ----------------
HTML_LOGIN = """
<h2>ServWell Medicare Login</h2>
<form method="post">
<input name="username" placeholder="Username"><br><br>
<input name="password" type="password" placeholder="Password"><br><br>
<button>Login</button>
</form>
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (request.form["username"], request.form["password"]))
        user = c.fetchone()
        db.close()

        if user:
            session["user"] = request.form["username"]
            return redirect("/")

        return "Wrong login"

    return render_template_string(HTML_LOGIN)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- DASHBOARD ----------------
HTML_HOME = """
<h2>ServWell Medicare Dashboard</h2>
<a href="/logout">Logout</a> |
<a href="/sales">Sales History</a>

<h3>Add Medicine</h3>
<form method="post">
<input name="name" placeholder="Medicine">
<input name="qty" placeholder="Qty">
<input name="price" placeholder="Price">
<button>Add</button>
</form>

<h3>Medicines</h3>
<table border=1>
<tr><th>Name</th><th>Qty</th><th>Price</th><th>Sell</th></tr>
{% for m in meds %}
<tr>
<td>{{m[1]}}</td>
<td>{{m[2]}}</td>
<td>{{m[3]}}</td>
<td>
<form action="/sell/{{m[0]}}" method="post">
<input name="qty" placeholder="Qty" size=3>
<button>Sell</button>
</form>
</td>
</tr>
{% endfor %}
</table>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    db = get_db()
    c = db.cursor()

    if request.method == "POST":
        c.execute("INSERT INTO medicines(name,qty,price) VALUES(?,?,?)",
                  (request.form["name"], request.form["qty"], request.form["price"]))
        db.commit()

    meds = c.execute("SELECT * FROM medicines").fetchall()
    db.close()

    return render_template_string(HTML_HOME, meds=meds)


# ---------------- SELL MEDICINE ----------------
@app.route("/sell/<int:id>", methods=["POST"])
def sell(id):
    db = get_db()
    c = db.cursor()

    qty_sell = int(request.form["qty"])

    med = c.execute("SELECT name, qty, price FROM medicines WHERE id=?", (id,)).fetchone()

    if med and med[1] >= qty_sell:
        new_qty = med[1] - qty_sell
        total = qty_sell * med[2]

        c.execute("UPDATE medicines SET qty=? WHERE id=?", (new_qty, id))
        c.execute("INSERT INTO sales(name, qty, total) VALUES(?,?,?)",
                  (med[0], qty_sell, total))
        db.commit()

    db.close()
    return redirect("/")


# ---------------- SALES HISTORY ----------------
HTML_SALES = """
<h2>Sales History</h2>
<a href="/">Back</a>

<table border=1>
<tr><th>Medicine</th><th>Qty</th><th>Total ₦</th></tr>
{% for s in sales %}
<tr>
<td>{{s[1]}}</td>
<td>{{s[2]}}</td>
<td>{{s[3]}}</td>
</tr>
{% endfor %}
</table>
"""


@app.route("/sales")
def sales():
    db = get_db()
    c = db.cursor()
    sales = c.execute("SELECT * FROM sales").fetchall()
    db.close()

    return render_template_string(HTML_SALES, sales=sales)


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
