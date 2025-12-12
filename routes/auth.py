from flask import Blueprint, request, jsonify
from models import User
from database import db
import jwt
from config import Config
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

def make_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    pw = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username taken"}), 400

    u = User(username=username, email=email)
    u.set_password(pw)
    db.session.add(u)
    db.session.commit()

    return jsonify({"token": make_token(u)})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    pw = data.get("password")

    u = User.query.filter_by(username=username).first()
    if not u or not u.check_password(pw):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"token": make_token(u)})
