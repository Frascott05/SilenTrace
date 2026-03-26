from functools import wraps
from flask import request, jsonify
from utils.jwt import decode_token
from models.user import User

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """Reads the token from the http request
        """
        token = request.cookies.get("jwt")

        if not token:
            return jsonify({"error": "Missing Token"}), 401

        data = decode_token(token)
        if not data:
            return jsonify({"error": "Token not valid"}), 401

        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 401

        return f(user, *args, **kwargs)

    return decorated