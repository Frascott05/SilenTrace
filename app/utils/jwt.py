import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=current_app.config.get("JWT_EXPIRATION_HOURS", 24))
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None