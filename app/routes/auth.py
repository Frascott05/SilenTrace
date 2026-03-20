from flask import Blueprint, request, jsonify, make_response
from models.user import User
from app import db
from utils.jwt import generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json 
    if not data.get("email") or not data.get("password") or not data.get("username"):
        return {"error": "Dati mancanti"}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "Email già registrata"}, 400

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    token = generate_token(user)

    resp = make_response(jsonify({"message": "Utente registrato"}))
    resp.set_cookie("jwt", token, httponly=True, samesite="Lax")
    return resp


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Credenziali non valide"}), 401

    token = generate_token(user)

    resp = make_response(jsonify({"message": "Utente registrato"}))
    resp.set_cookie("jwt", token, httponly=True, samesite="Lax")
    return resp


#TODO: ADDING THE LOGOUT BUTTON