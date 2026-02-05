from flask import Flask, request, redirect, session, render_template_string
import os

app = Flask(__name__)
app.secret_key = "servwell_secret"

USERNAME = "admin"
PASSWORD = "2020"

inventory = []


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect("/")
        else:
            return "<h3>Invalid login</h3><a href='/login'>Try again</a>"

    return render_template_string(HTML_LOGIN)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        inventory.append({
            "name": request.form["name"],
            "qty": request.form["qty"],
            "price": request.form["price"]
        })

    return render_template_string(HTML_HOME, inventory=inventory)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

inventory = []

USERNAME = "admin"
PASSWORD = "2020"

HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
<title>Login - ServWell Medicare</title>
</head>
<body style="font-family:Arial;text-align:center;margin-top:100px;">
<h2>ServWell Medicare Login</h2>
<form method="POST">
<input name="username" placeholder="Username" required><br><br>
<input name="password" type="password" placeholder="Password" required><br><br>
<button type="submit">Login</button>
</form>
</body>
</html>
"""

HTML_HOME = """
<!DOCTYPE html>
<html>
<head>
<title>ServWell Medicare</title>
</head>
<body style="font-family:Arial;">
<h1>ServWell Medicare</h1>
<a href="/logout">Logout</a>

<h2>Add Medicine</h2>
<form method="POST">
<input name="name" placeholder="Medicine name" required>
<input name="qty" placeholder="Quantity" required>
<input name="price" placeholder="Price" required>
<button type="submit">Add</button>
</form>

<h2>Inventory</h2>
<table border="1" cellpadding="10">
<tr><th>Name</th><th>Qty</th><th>Price</th></tr>
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect("/")
    return render_template_string(HTML_LOGIN)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        inventory.append({
            "name": request.form["name"],
            "qty": request.form["qty"],
            "price": request.form["price"]
        })

    return render_template_string(HTML_HOME, inventory=inventory)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
