from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.job_application import JobApplication
from app.models.conversation import Conversation, ConversationParticipant, Message
from app.utils.decorators import token_required, user_type_required
from datetime import datetime

bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')


@bp.route('/applications', methods=['POST'])
@token_required
@user_type_required('student')
def apply_for_job(current_user):
    """
    Student applies for a job

    Request JSON:
        {
            "employer_id": 123,
            "job_title": "Software Engineer"
        }

    Returns:
        {
            "message": "Application submitted successfully",
            "application": {...}
        }
    """
    try:
        data = request.get_json()

        if not data.get('employer_id') or not data.get('job_title'):
            return jsonify({'error': 'Employer ID and job title are required'}), 400

        # Check if employer exists
        employer = User.query.filter_by(id=data['employer_id'], user_type='employer').first()
        if not employer:
            return jsonify({'error': 'Employer not found'}), 404

        # Create job application
        application = JobApplication(
            student_id=current_user.id,
            employer_id=data['employer_id'],
            job_title=data['job_title'],
            status='pending'
        )

        db.session.add(application)
        db.session.commit()

        return jsonify({
            'message': 'Application submitted successfully',
            'application': application.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit application', 'details': str(e)}), 500


@bp.route('/applications/<int:application_id>/accept', methods=['POST'])
@token_required
@user_type_required('employer')
def accept_application(current_user, application_id):
    """
    Employer accepts a job application
    Automatically creates a conversation and sends a congratulatory message

    Returns:
        {
            "message": "Application accepted",
            "application": {...},
            "conversation": {...}
        }
    """
    try:
        # Find application
        application = JobApplication.query.get(application_id)

        if not application:
            return jsonify({'error': 'Application not found'}), 404

        # Verify employer owns this application
        if application.employer_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Update application status
        application.status = 'accepted'
        application.updated_at = datetime.utcnow()

        # Check if conversation already exists
        existing_conversation = db.session.query(Conversation).join(
            ConversationParticipant, Conversation.id == ConversationParticipant.conversation_id
        ).filter(
            ConversationParticipant.user_id.in_([current_user.id, application.student_id])
        ).group_by(Conversation.id).having(
            db.func.count(ConversationParticipant.user_id) == 2
        ).first()

        if existing_conversation:
            # Check if both users are actually in this conversation
            participants_ids = [p.user_id for p in existing_conversation.participants]
            if current_user.id in participants_ids and application.student_id in participants_ids:
                conversation = existing_conversation
            else:
                # Create new conversation
                conversation = Conversation()
                db.session.add(conversation)
                db.session.flush()

                # Add participants
                participant1 = ConversationParticipant(
                    conversation_id=conversation.id,
                    user_id=current_user.id
                )
                participant2 = ConversationParticipant(
                    conversation_id=conversation.id,
                    user_id=application.student_id
                )
                db.session.add(participant1)
                db.session.add(participant2)
        else:
            # Create new conversation
            conversation = Conversation()
            db.session.add(conversation)
            db.session.flush()

            # Add participants
            participant1 = ConversationParticipant(
                conversation_id=conversation.id,
                user_id=current_user.id
            )
            participant2 = ConversationParticipant(
                conversation_id=conversation.id,
                user_id=application.student_id
            )
            db.session.add(participant1)
            db.session.add(participant2)

        # Create automated congratulatory message
        student = User.query.get(application.student_id)
        congrats_message = Message(
            conversation_id=conversation.id,
            sender_id=current_user.id,
            content=f"Congratulations {student.full_name or student.username}! 🎉 Your application for the position of '{application.job_title}' has been accepted. We're excited to have you on board! Let's discuss the next steps.",
            is_system_message=True
        )
        db.session.add(congrats_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()

        # Increment unread count for student
        student_participant = ConversationParticipant.query.filter_by(
            conversation_id=conversation.id,
            user_id=application.student_id
        ).first()
        student_participant.unread_count += 1

        db.session.commit()

        return jsonify({
            'message': 'Application accepted and conversation created',
            'application': application.to_dict(),
            'conversation': conversation.to_dict(current_user.id)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to accept application', 'details': str(e)}), 500


@bp.route('/applications/<int:application_id>/reject', methods=['POST'])
@token_required
@user_type_required('employer')
def reject_application(current_user, application_id):
    """
    Employer rejects a job application

    Returns:
        {
            "message": "Application rejected",
            "application": {...}
        }
    """
    try:
        # Find application
        application = JobApplication.query.get(application_id)

        if not application:
            return jsonify({'error': 'Application not found'}), 404

        # Verify employer owns this application
        if application.employer_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Update application status
        application.status = 'rejected'
        application.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'message': 'Application rejected',
            'application': application.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to reject application', 'details': str(e)}), 500


@bp.route('/applications', methods=['GET'])
@token_required
def get_applications(current_user):
    """
    Get all job applications
    - Students see their own applications
    - Employers see applications to their jobs

    Returns:
        {
            "applications": [...]
        }
    """
    try:
        if current_user.user_type == 'student':
            applications = JobApplication.query.filter_by(student_id=current_user.id).all()
        else:  # employer
            applications = JobApplication.query.filter_by(employer_id=current_user.id).all()

        return jsonify({
            'applications': [app.to_dict() for app in applications]
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch applications', 'details': str(e)}), 500
