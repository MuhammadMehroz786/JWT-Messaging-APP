from app import db
from datetime import datetime, timezone

class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    participants = db.relationship('ConversationParticipant', back_populates='conversation', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='conversation', cascade='all, delete-orphan', order_by='Message.created_at')

    def to_dict(self, current_user_id=None):
        """Convert conversation to dictionary"""
        last_message = self.messages[-1] if self.messages else None

        # Get unread count for current user
        unread_count = 0
        other_participant = None
        if current_user_id:
            for participant in self.participants:
                if participant.user_id == current_user_id:
                    unread_count = participant.unread_count
                else:
                    other_participant = participant.user.to_dict()

        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z',
            'last_message': last_message.to_dict() if last_message else None,
            'unread_count': unread_count,
            'other_participant': other_participant,
            'participants': [p.user.to_dict() for p in self.participants]
        }


class ConversationParticipant(db.Model):
    __tablename__ = 'conversation_participants'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    unread_count = db.Column(db.Integer, default=0)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    conversation = db.relationship('Conversation', back_populates='participants')
    user = db.relationship('User', back_populates='conversation_participants')

    # Ensure a user can only be in a conversation once
    __table_args__ = (db.UniqueConstraint('conversation_id', 'user_id', name='unique_conversation_participant'),)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Made nullable for file-only messages
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_system_message = db.Column(db.Boolean, default=False)  # For automated messages

    # File attachment fields
    has_attachment = db.Column(db.Boolean, default=False)
    file_name = db.Column(db.String(255), nullable=True)
    file_path = db.Column(db.String(500), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)  # Size in bytes
    file_type = db.Column(db.String(100), nullable=True)  # MIME type

    # Relationships
    conversation = db.relationship('Conversation', back_populates='messages')
    sender = db.relationship('User', back_populates='messages')

    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'sender': self.sender.to_dict() if self.sender else None,
            'content': self.content,
            'created_at': self.created_at.isoformat() + 'Z',
            'is_system_message': self.is_system_message,
            'has_attachment': self.has_attachment,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_type': self.file_type
        }
