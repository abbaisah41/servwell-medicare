from flask import Flask, request, redirect, session, render_template_string
import os

app = Flask(__name__)

# Secret key for session login
app.secret_key = "servwell_secret_key"

# Login details
USERNAME = "admin"
PASSWORD = "2020"

# Simple in-memory inventory list
inventory = []


# ---------------- LOGIN PAGE ----------------
HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
    <title>ServWell Medicare Login</title>
</head>
<body style="text-align:center; font-family:Arial;">

<h2>ServWell Medicare Login</h2>

<form method="post">
    <input name="username" placeholder="Username"><br><br>
    <input name="password" type="password" placeholder="Password"><br><br>
    <button type="submit">Login</button>
</form>

</body>
</html>
"""


# ---------------- DASHBOARD PAGE ----------------
HTML_HOME = """
<!DOCTYPE html>
<html>
<head>
    <title>ServWell Medicare Dashboard</title>
</head>
<body style="font-family:Arial; padding:20px;">

<h2>ServWell Medicare Dashboard</h2>
<a href="/logout">Logout</a>

<h3>Add Medicine</h3>
<form method="post">
    <input name="name" placeholder="Medicine Name" required>
    <input name="qty" placeholder="Quantity" required>
    <input name="price" placeholder="Price" required>
    <button type="submit">Add</button>
</form>

<h3>Inventory List</h3>
<table border="1" cellpadding="8">
<tr>
    <th>Name</th>
    <th>Quantity</th>
    <th>Price</th>
</tr>

{% for item in inventory %}
<tr>
    <td>{{ item.name }}</td>
    <td>{{ item.qty }}</td>
    <td>{{ item.price }}</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""


# ---------------- LOGIN ROUTE ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid username or password"

    return render_template_string(HTML_LOGIN)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- HOME / DASHBOARD ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    # Require login
    if "user" not in session:
        return redirect("/login")

    # Add medicine
    if request.method == "POST":
        inventory.append({
            "name": request.form["name"],
            "qty": request.form["qty"],
            "price": request.form["price"]
        })

    return render_template_string(HTML_HOME, inventory=inventory)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
