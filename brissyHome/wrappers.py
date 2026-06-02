from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("main.login"))
        return func(*args, **kwargs)
    return wrapper


def buyer_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("main.login"))

        if session["user"]["role"] != "buyer":
            flash("Buyer/Tenant access required.", "error")
            return redirect(url_for("main.index"))

        return func(*args, **kwargs)
    return wrapper


def seller_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("main.login"))

        # Allow both sellers and admins to access seller management pages
        if session["user"]["role"] not in ["seller", "admin"]:
            flash("Seller/Agent access required.", "error")
            return redirect(url_for("main.index"))

        return func(*args, **kwargs)
    return wrapper