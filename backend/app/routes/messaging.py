from flask import Blueprint, request, jsonify, send_from_directory, current_app
from app import db
from app.models.user import User
from app.models.conversation import Conversation, ConversationParticipant, Message
from app.utils.decorators import token_required
from sqlalchemy import or_, and_
from werkzeug.utils import secure_filename
import os
import uuid

bp = Blueprint('messaging', __name__, url_prefix='/api/messages')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations(current_user):
    """
    Get all conversations for the current user

    Returns:
        {
            "conversations": [...]
        }
    """
    try:
        # Get all conversation participants for current user
        participants = ConversationParticipant.query.filter_by(user_id=current_user.id).all()

        conversations = []
        for participant in participants:
            conversation = participant.conversation
            conversations.append(conversation.to_dict(current_user.id))

        # Sort by most recent message
        conversations.sort(key=lambda x: x['updated_at'], reverse=True)

        return jsonify({
            'conversations': conversations
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch conversations', 'details': str(e)}), 500


@bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, conversation_id):
    """
    Get all messages in a conversation with pagination

    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Messages per page (default: 50)

    Returns:
        {
            "messages": [...],
            "page": 1,
            "per_page": 50,
            "total": 100
        }
    """
    try:
        # Verify user is part of the conversation
        participant = ConversationParticipant.query.filter_by(
            conversation_id=conversation_id,
            user_id=current_user.id
        ).first()

        if not participant:
            return jsonify({'error': 'You are not part of this conversation'}), 403

        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        # Get messages with pagination
        messages_query = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at.asc())
        paginated = messages_query.paginate(page=page, per_page=per_page, error_out=False)

        messages = [msg.to_dict() for msg in paginated.items]

        return jsonify({
            'messages': messages,
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch messages', 'details': str(e)}), 500


@bp.route('/conversations/<int:conversation_id>/send', methods=['POST'])
@token_required
def send_message(current_user, conversation_id):
    """
    Send a message in a conversation (with optional file attachment)

    Request Form Data:
        content: Message content (optional if file is provided)
        file: File attachment (optional)

    Returns:
        {
            "message": "Message sent successfully",
            "data": {...}
        }
    """
    try:
        # Get form data
        content = request.form.get('content', '')
        file = request.files.get('file')

        # Require either content or file
        if not content and not file:
            return jsonify({'error': 'Message content or file is required'}), 400

        # Verify user is part of the conversation
        participant = ConversationParticipant.query.filter_by(
            conversation_id=conversation_id,
            user_id=current_user.id
        ).first()

        if not participant:
            return jsonify({'error': 'You are not part of this conversation'}), 403

        # Handle file upload
        file_name = None
        file_path = None
        file_size = None
        file_type = None
        has_attachment = False

        if file and file.filename:
            if not allowed_file(file.filename):
                return jsonify({'error': 'File type not allowed'}), 400

            # Generate unique filename
            original_filename = secure_filename(file.filename)
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

            # Save file
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)

            # Get file info
            file_name = original_filename
            file_size = os.path.getsize(file_path)
            file_type = file.content_type
            has_attachment = True

        # Create message
        message = Message(
            conversation_id=conversation_id,
            sender_id=current_user.id,
            content=content if content else None,
            has_attachment=has_attachment,
            file_name=file_name,
            file_path=unique_filename if has_attachment else None,  # Store only filename, not full path
            file_size=file_size,
            file_type=file_type
        )
        db.session.add(message)

        # Update conversation timestamp
        conversation = Conversation.query.get(conversation_id)
        from datetime import datetime
        conversation.updated_at = datetime.utcnow()

        # Increment unread count for other participants
        other_participants = ConversationParticipant.query.filter(
            and_(
                ConversationParticipant.conversation_id == conversation_id,
                ConversationParticipant.user_id != current_user.id
            )
        ).all()

        for other_participant in other_participants:
            other_participant.unread_count += 1

        db.session.commit()

        return jsonify({
            'message': 'Message sent successfully',
            'data': message.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to send message', 'details': str(e)}), 500


@bp.route('/conversations/<int:conversation_id>/mark-read', methods=['POST'])
@token_required
def mark_as_read(current_user, conversation_id):
    """
    Mark all messages in a conversation as read (reset unread count)

    Returns:
        {
            "message": "Messages marked as read"
        }
    """
    try:
        # Find participant
        participant = ConversationParticipant.query.filter_by(
            conversation_id=conversation_id,
            user_id=current_user.id
        ).first()

        if not participant:
            return jsonify({'error': 'You are not part of this conversation'}), 403

        # Reset unread count
        participant.unread_count = 0
        db.session.commit()

        return jsonify({
            'message': 'Messages marked as read'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to mark messages as read', 'details': str(e)}), 500


@bp.route('/conversations/start', methods=['POST'])
@token_required
def start_conversation(current_user):
    """
    Start a new conversation with another user

    Request JSON:
        {
            "recipient_id": 123
        }

    Returns:
        {
            "message": "Conversation started",
            "conversation": {...}
        }
    """
    try:
        data = request.get_json()

        if not data.get('recipient_id'):
            return jsonify({'error': 'Recipient ID is required'}), 400

        recipient_id = data['recipient_id']

        # Check if recipient exists
        recipient = User.query.get(recipient_id)
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404

        # Check if conversation already exists between these two users
        existing_conversation = db.session.query(Conversation).join(
            ConversationParticipant, Conversation.id == ConversationParticipant.conversation_id
        ).filter(
            ConversationParticipant.user_id.in_([current_user.id, recipient_id])
        ).group_by(Conversation.id).having(
            db.func.count(ConversationParticipant.user_id) == 2
        ).first()

        if existing_conversation:
            # Check if both users are actually in this conversation
            participants_ids = [p.user_id for p in existing_conversation.participants]
            if current_user.id in participants_ids and recipient_id in participants_ids:
                return jsonify({
                    'message': 'Conversation already exists',
                    'conversation': existing_conversation.to_dict(current_user.id)
                }), 200

        # Create new conversation
        conversation = Conversation()
        db.session.add(conversation)
        db.session.flush()  # Get conversation ID

        # Add participants
        participant1 = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=current_user.id
        )
        participant2 = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=recipient_id
        )

        db.session.add(participant1)
        db.session.add(participant2)
        db.session.commit()

        return jsonify({
            'message': 'Conversation started',
            'conversation': conversation.to_dict(current_user.id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to start conversation', 'details': str(e)}), 500


@bp.route('/files/<filename>', methods=['GET'])
@token_required
def download_file(current_user, filename):
    """
    Download a file attachment

    Returns:
        File download
    """
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Verify the file exists and the user has access to it
        message = Message.query.filter_by(file_path=filename).first()
        
        if not message:
            return jsonify({'error': 'File not found'}), 404
        
        # Check if user is part of the conversation
        participant = ConversationParticipant.query.filter_by(
            conversation_id=message.conversation_id,
            user_id=current_user.id
        ).first()
        
        if not participant:
            return jsonify({'error': 'Access denied'}), 403
        
        # Send file
        return send_from_directory(
            upload_folder,
            filename,
            as_attachment=True,
            download_name=message.file_name
        )
        
    except Exception as e:
        return jsonify({'error': 'Failed to download file', 'details': str(e)}), 500
