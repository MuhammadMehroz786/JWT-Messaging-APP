from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.utils.jwt_utils import generate_access_token, generate_refresh_token, decode_token
from app.utils.decorators import token_required
import jwt

import logging

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

logging.basicConfig(level=logging.INFO)


@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user

    Request JSON:
        {
            "email": "user@example.com",
            "username": "username",
            "password": "password123",
            "user_type": "student" or "employer",
            "full_name": "Full Name" (optional)
        }

    Returns:
        {
            "message": "User registered successfully",
            "user": {...},
            "access_token": "...",
            "refresh_token": "..."
        }
    """
    try:
        print(f"Register request headers: {request.headers}", flush=True)
        print(f"Register request body raw: {request.get_data(as_text=True)}", flush=True)
        data = request.get_json()
        print(f"Register request json: {data}", flush=True)

        # Validate required fields
        required_fields = ['email', 'username', 'password', 'user_type']
        for field in required_fields:
            if not data.get(field):
                print(f"Missing field: {field} in {data}", flush=True)
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Validate user_type
        if data['user_type'] not in ['student', 'employer']:
            return jsonify({'error': 'user_type must be either "student" or "employer"'}), 400

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400

        # Create new user
        user = User(
            email=data['email'],
            username=data['username'],
            user_type=data['user_type'],
            full_name=data.get('full_name', '')
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Generate tokens
        access_token = generate_access_token(user.id, user.user_type)
        refresh_token = generate_refresh_token(user.id)

        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
    Login user

    Request JSON:
        {
            "email": "user@example.com",
            "password": "password123"
        }

    Returns:
        {
            "message": "Login successful",
            "user": {...},
            "access_token": "...",
            "refresh_token": "..."
        }
    """
    try:
        # Get JSON data
        data = request.get_json()

        # Validate data exists
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields - accept both 'email' and 'username' for compatibility
        email = data.get('email', '') or data.get('username', '')
        email = email.strip() if email else ''
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Find user by email
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate tokens
        access_token = generate_access_token(user.id, user.user_type)
        refresh_token = generate_refresh_token(user.id)

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500


@bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh access token using refresh token

    Request JSON:
        {
            "refresh_token": "..."
        }

    Returns:
        {
            "access_token": "..."
        }
    """
    try:
        data = request.get_json()

        if not data.get('refresh_token'):
            return jsonify({'error': 'Refresh token is required'}), 400

        # Decode and validate refresh token
        try:
            payload = decode_token(data['refresh_token'])

            # Verify it's a refresh token
            if payload.get('type') != 'refresh':
                return jsonify({'error': 'Invalid token type'}), 401

            # Get user
            user = User.query.get(payload['user_id'])

            if not user:
                return jsonify({'error': 'User not found'}), 401

            # Generate new access token
            access_token = generate_access_token(user.id, user.user_type)

            return jsonify({
                'access_token': access_token
            }), 200

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Refresh token has expired. Please login again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid refresh token'}), 401

    except Exception as e:
        return jsonify({'error': 'Token refresh failed', 'details': str(e)}), 500


@bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """
    Get current user information

    Returns:
        {
            "user": {...}
        }
    """
    return jsonify({
        'user': current_user.to_dict()
    }), 200