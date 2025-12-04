from app import db
from datetime import datetime

class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', foreign_keys=[student_id])
    employer = db.relationship('User', foreign_keys=[employer_id])

    def to_dict(self):
        """Convert job application to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'employer_id': self.employer_id,
            'job_title': self.job_title,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z'
        }
