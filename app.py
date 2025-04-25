
import os
from flask import Flask, redirect, request, session, url_for
import stripe
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
YOUR_DOMAIN = os.getenv("DOMAIN", "http://localhost:5000")

@app.route("/")
def index():
    if 'user' not in session:
        return redirect(url_for("login"))
    return redirect(url_for("create_checkout_session"))

@app.route("/login")
def login():
    session["user"] = "user_id"  # Mock login
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/create-checkout-session")
def create_checkout_session():
    if 'user' not in session:
        return redirect(url_for("login"))
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "brl",
                    "product_data": {
                        "name": "Plano Premium",
                    },
                    "unit_amount": 6990,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success",
            cancel_url=YOUR_DOMAIN + "/cancel",
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)

@app.route("/success")
def success():
    return "<h1>Pagamento realizado com sucesso!</h1>"

@app.route("/cancel")
def cancel():
    return "<h1>Pagamento cancelado.</h1>"

if __name__ == "__main__":
    app.run(debug=True)
