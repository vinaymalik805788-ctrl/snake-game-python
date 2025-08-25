"""
Simple Fashion Shop Website using Flask
--------------------------------------
Run steps:
1) pip install flask
2) python app.py
Open http://127.0.0.1:5000

Features:
- Home page with products
- Product details page
- Cart (session-based)
- Add/Remove items
- Fake checkout

Note: All templates are embedded as strings for single-file demo.
"""

from flask import Flask, render_template_string, request, redirect, url_for, session
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# --- Fake DB ---
PRODUCTS = [
    {
        "id": 1,
        "name": "Classic White Tee",
        "price": Decimal("499.00"),
        "img": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=800",
        "badge": "New",
        "desc": "100% cotton | Regular fit | Breathable fabric"
    },
    {
        "id": 2,
        "name": "Denim Jacket",
        "price": Decimal("2499.00"),
        "img": "https://images.unsplash.com/photo-1520975922284-8b456906c813?w=800",
        "badge": "Trending",
        "desc": "Mid-wash blue | Unisex | All-season layer"
    },
    {
        "id": 3,
        "name": "Black Sneakers",
        "price": Decimal("1799.00"),
        "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800",
        "badge": "Hot",
        "desc": "Cushioned sole | Lightweight | Street style"
    },
    {
        "id": 4,
        "name": "Summer Floral Dress",
        "price": Decimal("1599.00"),
        "img": "https://images.unsplash.com/photo-1520975682031-b3f6a1b7b75b?w=800",
        "badge": "Sale",
        "desc": "Flowy silhouette | Soft rayon | Pockets"
    },
]

# --- Helpers ---
def get_cart():
    cart = session.get("cart", {})
    return {int(k): int(v) for k, v in cart.items()}

def save_cart(cart):
    session["cart"] = {str(k): int(v) for k, v in cart.items()}


def cart_items_and_total(cart):
    items = []
    total = Decimal("0.00")
    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if product:
            line_total = product["price"] * qty
            total += line_total
            items.append({"product": product, "qty": qty, "line_total": line_total})
    return items, total

# --- Templates ---
BASE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title or 'Fashion Shop' }}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body{background:#0f1115;color:#e8e8ea}
    .navbar{background:#141824}
    .card{background:#161a26;border:1px solid #22283a;color:#e8e8ea}
    .btn-primary{background:#6c5ce7;border-color:#6c5ce7}
    .btn-outline-light{border-color:#353b50;color:#e8e8ea}
    .price{color:#a3f7bf}
    .badge-soft{background:#22283a;color:#c8c9cc;border:1px solid #2e3550}
    .footer{color:#9aa3b2}
    .hero{background:linear-gradient(135deg,#1a1f2e 0%, #0f1115 60%);border-radius:16px}
    a{color:#b3c7ff;text-decoration:none}
    a:hover{color:#d6e1ff}
  </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark">
  <div class="container">
    <a class="navbar-brand fw-bold" href="{{ url_for('home') }}">Fashion<span class="text-primary">Hub</span></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample07" aria-controls="navbarsExample07" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarsExample07">
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
        <li class="nav-item"><a class="nav-link" href="{{ url_for('home') }}">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Men</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Women</a></li>
        <li class="nav-item"><a class="nav-link" href="#">New Arrivals</a></li>
        <li class="nav-item"><a class="nav-link position-relative" href="{{ url_for('cart') }}">
          Cart
          {% set cart_count = (session.get('cart')|default({})).values()|sum %}
          {% if cart_count %}
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">{{ cart_count }}</span>
          {% endif %}
        </a></li>
      </ul>
    </div>
  </div>
</nav>

<main class="container my-4">
  {% block content %}{% endblock %}
</main>

<footer class="container py-4">
  <div class="footer small">© {{ 2025 }} FashionHub. Built with Flask. Made by Vinay.</div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

HOME_HTML = """
{% extends 'base.html' %}
{% block content %}
<section class="hero p-4 p-md-5 mb-4">
  <div class="row align-items-center">
    <div class="col-md-7">
      <h1 class="display-5 fw-bold">Step into Style</h1>
      <p class="lead">Trendy fits, comfy fabrics, and everyday essentials—delivered with love. Free shipping over ₹999.</p>
      <a href="#catalog" class="btn btn-primary btn-lg">Shop Now</a>
      <a href="{{ url_for('cart') }}" class="btn btn-outline-light btn-lg ms-2">View Cart</a>
    </div>
    <div class="col-md-5 text-center">
      <img class="img-fluid rounded" src="https://images.unsplash.com/photo-1520975682031-b3f6a1b7b75b?w=1200" alt="Hero">
    </div>
  </div>
</section>

<h2 id="catalog" class="mb-3">Featured Products</h2>
<div class="row g-3">
  {% for p in products %}
  <div class="col-12 col-sm-6 col-md-4 col-lg-3">
    <div class="card h-100">
      <img src="{{ p.img }}" class="card-img-top" alt="{{ p.name }}">
      <div class="card-body d-flex flex-column">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <h5 class="card-title mb-0">{{ p.name }}</h5>
          {% if p.badge %}<span class="badge badge-soft">{{ p.badge }}</span>{% endif %}
        </div>
        <p class="card-text small">{{ p.desc }}</p>
        <div class="mt-auto d-flex justify-content-between align-items-center">
          <span class="price fw-bold">₹ {{ '%.2f'|format(p.price) }}</span>
          <div>
            <a href="{{ url_for('product_detail', pid=p.id) }}" class="btn btn-sm btn-outline-light">View</a>
            <a href="{{ url_for('add_to_cart', pid=p.id) }}" class="btn btn-sm btn-primary">Add</a>
          </div>
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
{% endblock %}
"""

PRODUCT_HTML = """
{% extends 'base.html' %}
{% block content %}
<div class="row g-4">
  <div class="col-md-6">
    <img src="{{ product.img }}" class="img-fluid rounded" alt="{{ product.name }}">
  </div>
  <div class="col-md-6">
    <h2 class="fw-bold">{{ product.name }}</h2>
    <p class="lead price">₹ {{ '%.2f'|format(product.price) }}</p>
    <p>{{ product.desc }}</p>

    <form action="{{ url_for('add_to_cart', pid=product.id) }}" method="post" class="d-flex align-items-center gap-2">
      <input type="number" min="1" value="1" class="form-control" name="qty" style="max-width:120px">
      <button class="btn btn-primary" type="submit">Add to Cart</button>
      <a href="{{ url_for('cart') }}" class="btn btn-outline-light">Go to Cart</a>
    </form>
  </div>
</div>
{% endblock %}
"""

CART_HTML = """
{% extends 'base.html' %}
{% block content %}
<h2 class="mb-3">Your Cart</h2>
{% if items %}
<table class="table table-dark table-striped align-middle">
  <thead><tr><th>Product</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr></thead>
  <tbody>
    {% for row in items %}
    <tr>
      <td>{{ row.product.name }}</td>
      <td>₹ {{ '%.2f'|format(row.product.price) }}</td>
      <td>{{ row.qty }}</td>
      <td>₹ {{ '%.2f'|format(row.line_total) }}</td>
      <td>
        <a class="btn btn-sm btn-outline-light" href="{{ url_for('remove_from_cart', pid=row.product.id) }}">Remove</a>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
<div class="d-flex justify-content-between">
  <h4>Total: <span class="price">₹ {{ '%.2f'|format(total) }}</span></h4>
  <div>
    <a href="{{ url_for('home') }}" class="btn btn-outline-light">Continue Shopping</a>
    <a href="{{ url_for('checkout') }}" class="btn btn-primary">Checkout</a>
  </div>
</div>
{% else %}
  <p>Your cart is empty.</p>
  <a href="{{ url_for('home') }}" class="btn btn-primary">Shop Now</a>
{% endif %}
{% endblock %}
"""

CHECKOUT_HTML = """
{% extends 'base.html' %}
{% block content %}
<h2>Checkout</h2>
<p class="mb-3">This is a demo checkout. No real payments.</p>
<form method="post" class="row g-3">
  <div class="col-md-6">
    <label class="form-label">Full Name</label>
    <input class="form-control" name="name" required>
  </div>
  <div class="col-md-6">
    <label class="form-label">Email</label>
    <input type="email" class="form-control" name="email" required>
  </div>
  <div class="col-12">
    <label class="form-label">Address</label>
    <input class="form-control" name="address" required>
  </div>
  <div class="col-md-6">
    <label class="form-label">City</label>
    <input class="form-control" name="city" required>
  </div>
  <div class="col-md-6">
    <label class="form-label">Pincode</label>
    <input class="form-control" name="zip" required>
  </div>
  <div class="col-12 d-flex justify-content-between align-items-center">
    <a href="{{ url_for('cart') }}" class="btn btn-outline-light">Back to Cart</a>
    <button class="btn btn-primary" type="submit">Place Order</button>
  </div>
</form>
{% if placed %}
<div class="alert alert-success mt-3">Order placed! (Demo)</div>
{% endif %}
{% endblock %}
"""

# --- Routes ---
@app.route("/")
def home():
    return render_template_string(HOME_HTML, products=PRODUCTS)

@app.route("/product/<int:pid>")
def product_detail(pid):
    product = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not product:
        return redirect(url_for('home'))
    return render_template_string(PRODUCT_HTML, product=product)

@app.route("/add/<int:pid>", methods=["GET", "POST"])
def add_to_cart(pid):
    qty = 1
    if request.method == "POST":
        try:
            qty = max(1, int(request.form.get("qty", 1)))
        except ValueError:
            qty = 1
    cart = get_cart()
    cart[pid] = cart.get(pid, 0) + qty
    save_cart(cart)
    return redirect(url_for('cart'))

@app.route("/remove/<int:pid>")
def remove_from_cart(pid):
    cart = get_cart()
    if pid in cart:
        del cart[pid]
        save_cart(cart)
    return redirect(url_for('cart'))

@app.route("/cart")
def cart():
    cart = get_cart()
    items, total = cart_items_and_total(cart)
    return render_template_string(CART_HTML, items=items, total=total)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    placed = False
    if request.method == "POST":
        # In real app: save order, clear cart, process payment
        session.pop("cart", None)
        placed = True
    return render_template_string(CHECKOUT_HTML, placed=placed)

# Register base template in Jinja loader via context_processor
@app.context_processor
def inject_base():
    return {"session": session}

# Manually add base template so render_template_string can extend it
@app.before_request
def add_base_template():
    app.jinja_env.globals['base'] = BASE_HTML
    app.jinja_loader = app.create_global_jinja_loader()
    app.jinja_env.loader = app.jinja_env.loader
    app.jinja_env.globals['url_for'] = url_for
    app.jinja_env.from_string(BASE_HTML)
    app.jinja_env.get_or_select_template(["base.html"]).render

# Minimal loader override to make extends 'base.html' work
from jinja2 import DictLoader
app.jinja_loader = DictLoader({
    'base.html': BASE_HTML
})

if __name__ == "__main__":
    app.run(debug=True)