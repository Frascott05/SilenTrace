from functools import wraps
from flask import request, jsonify
from utils.jwt import decode_token
from models.user import User

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Legge il token dal cookie HttpOnly
        token = request.cookies.get("jwt")

        if not token:
            return jsonify({"error": "Token mancante"}), 401

        data = decode_token(token)
        if not data:
            return jsonify({"error": "Token non valido"}), 401

        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"error": "Utente non trovato"}), 401

        return f(user, *args, **kwargs)

    return decorated