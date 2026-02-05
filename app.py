from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
inventory = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ServWell Medicare</title>
<style>
body { font-family: Arial; background:#f4f6f8; margin:0; }
header { background:#2e7d32; color:white; padding:20px; text-align:center; }
main { padding:20px; }
section { background:white; padding:15px; margin-bottom:20px; border-radius:8px; }
input, button { padding:8px; margin:5px; }
button { background:#2e7d32; color:white; border:none; }
table { width:100%; border-collapse:collapse; }
th, td { border:1px solid #ccc; padding:8px; text-align:center; }
footer { background:#222; color:white; text-align:center; padding:10px; }
</style>
</head>
<body>

<header>
<h1>ServWell Medicare</h1>
<p>Online Pharmacy Inventory System</p>
</header>

<main>
<section>
<h2>Add Medicine</h2>
<form method="POST">
<input name="name" placeholder="Medicine name" required>
<input name="qty" type="number" placeholder="Quantity" required>
<input name="price" type="number" placeholder="Price (₦)" required>
<button type="submit">Add</button>
</form>
</section>

<section>
<h2>Inventory</h2>
<table>
<tr><th>Name</th><th>Qty</th><th>Price</th></tr>
{% for med in inventory %}
<tr>
<td>{{ med.name }}</td>
<td>{{ med.qty }}</td>
<td>{{ med.price }}</td>
</tr>
{% endfor %}
</table>
</section>
</main>

<footer>
<p>Phone: 07066235915</p>
<p>Thank you for choosing us</p>
</footer>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        qty = request.form.get("qty")
        price = request.form.get("price")

        if name and qty and price:
            inventory.append({"name": name, "qty": qty, "price": price})

        return redirect("/")

    return render_template_string(HTML, inventory=inventory)

if __name__ == "__main__":
    app.run()
