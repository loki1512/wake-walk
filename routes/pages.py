from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def index():
    return render_template("index.html")

@pages_bp.route("/login")
def login_page():
    return render_template("login.html")

@pages_bp.route("/signup")
def signup_page():
    return render_template("signup.html")
