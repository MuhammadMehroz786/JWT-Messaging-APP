from functools import wraps
from flask import request, jsonify
import jwt
from app.utils.jwt_utils import decode_token
from app.models.user import User

def token_required(f):
    """
    Decorator to validate JWT access token

    Usage:
        @token_required
        def protected_route(current_user):
            # current_user is automatically passed to the function
            return jsonify({'message': 'Access granted'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is in the Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format. Use: Bearer <token>'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Decode and validate token
            payload = decode_token(token)

            # Verify it's an access token
            if payload.get('type') != 'access':
                return jsonify({'error': 'Invalid token type'}), 401

            # Get user from database
            current_user = User.query.get(payload['user_id'])

            if not current_user:
                return jsonify({'error': 'User not found'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': 'Token validation failed', 'details': str(e)}), 401

        # Pass current_user to the decorated function
        return f(current_user, *args, **kwargs)

    return decorated


def user_type_required(*allowed_types):
    """
    Decorator to check user type (student or employer)

    Usage:
        @token_required
        @user_type_required('employer')
        def employer_only_route(current_user):
            return jsonify({'message': 'Employer access granted'})

        @token_required
        @user_type_required('student', 'employer')
        def multi_type_route(current_user):
            return jsonify({'message': 'Access granted'})
    """
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user.user_type not in allowed_types:
                return jsonify({
                    'error': f'Access denied. Required user type: {", ".join(allowed_types)}'
                }), 403

            return f(current_user, *args, **kwargs)

        return decorated
    return decorator
