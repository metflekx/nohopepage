from flask import render_template, redirect, session
from functools import wraps


def fail(message):
    """renders a fail page wich prints out error"""
    return render_template("fail.html", message=message)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("name") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
