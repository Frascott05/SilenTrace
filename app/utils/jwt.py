import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(user):
    """Generate the JWT token for a given user

    :param user: the current user
    :return: Jwt token encoded with the secret key and HS256 algorithm
    """
    payload = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=current_app.config.get("JWT_EXPIRATION_HOURS", 24))
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    """Decodes a given token

    :param token: Token to decode
    :return: the decode of the given token
    :return None: if the token is expired or invalid
    """
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None