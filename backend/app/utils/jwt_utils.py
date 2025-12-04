import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_access_token(user_id, user_type):
    """
    Generate JWT access token (short-lived: 1 hour)

    Args:
        user_id: User's ID
        user_type: User's type ('student' or 'employer')

    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'type': 'access',
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return token


def generate_refresh_token(user_id):
    """
    Generate JWT refresh token (long-lived: 30 days)

    Args:
        user_id: User's ID

    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
        'iat': datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return token


def decode_token(token):
    """
    Decode and validate JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded payload dictionary if valid

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Token has expired')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Invalid token')
