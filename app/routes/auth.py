from flask import Blueprint, request, jsonify, make_response
from models.user import User
from app import db
from utils.jwt import generate_token, decode_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ----------------------
# REGISTER
# ----------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data or not data.get("email") or not data.get("password") or not data.get("username"):
        return {"error": "Missing field requirements"}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "Email Already Registered"}, 400

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    token = generate_token(user)

    resp = make_response(jsonify({"message": "User Registered"}))
    resp.set_cookie(
        "jwt",
        token,
        httponly=True,
        samesite="Lax"
    )
    return resp


# ----------------------
# LOGIN
# ----------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid Credentials"}), 401

    token = generate_token(user)

    resp = make_response(jsonify({"message": "Correct Login"}))
    resp.set_cookie(
        "jwt",
        token,
        httponly=True,
        samesite="Lax"
    )
    return resp


# ----------------------
# LOGOUT
# ----------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"message": "Logged out"}))
    resp.delete_cookie("jwt")
    return resp


# ----------------------
# CONTEXT PROCESSOR (for templates)
# ----------------------
@auth_bp.app_context_processor
def inject_user():
    token = request.cookies.get("jwt")

    if not token:
        return dict(is_logged_in=False)

    try:
        decode_token(token)
        return dict(is_logged_in=True)
    except Exception:
        return dict(is_logged_in=False)