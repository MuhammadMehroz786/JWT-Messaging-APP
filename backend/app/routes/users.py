from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.utils.decorators import token_required, user_type_required

bp = Blueprint('users', __name__, url_prefix='/api/users')


@bp.route('/students', methods=['GET'])
@token_required
@user_type_required('employer')
def get_all_students(current_user):
    """
    Get all students (Employer-only endpoint)

    Returns:
        {
            "students": [...]
        }
    """
    try:
        students = User.query.filter_by(user_type='student').all()

        return jsonify({
            'students': [student.to_dict() for student in students]
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch students', 'details': str(e)}), 500
