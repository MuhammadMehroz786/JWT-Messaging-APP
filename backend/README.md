# Computer Network Project - Backend

Flask-based REST API with JWT authentication and messaging system.

## Features

- **JWT Authentication**: Access tokens (1 hour) and refresh tokens (30 days)
- **User Types**: Student and Employer roles
- **Messaging System**: Real-time messaging with unread counts
- **Automated Messaging**: Auto-generated messages when job applications are accepted
- **HTTP/HTTPS Communication**: RESTful API endpoints

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Database

SQLite database will be automatically created at `instance/cn_project.db` on first run.

## API Endpoints

### Authentication (`/api/auth`)

#### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "user_type": "student",  // or "employer"
  "full_name": "Full Name"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Refresh Token
```bash
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "your_refresh_token_here"
}
```

#### Get Current User
```bash
GET /api/auth/me
Authorization: Bearer <access_token>
```

### Messaging (`/api/messages`)

#### Get All Conversations
```bash
GET /api/messages/conversations
Authorization: Bearer <access_token>
```

#### Get Messages in a Conversation
```bash
GET /api/messages/conversations/<conversation_id>/messages?page=1&per_page=50
Authorization: Bearer <access_token>
```

#### Send Message
```bash
POST /api/messages/conversations/<conversation_id>/send
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "content": "Your message here"
}
```

#### Mark Messages as Read
```bash
POST /api/messages/conversations/<conversation_id>/mark-read
Authorization: Bearer <access_token>
```

#### Start New Conversation
```bash
POST /api/messages/conversations/start
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "recipient_id": 123
}
```

### Job Applications (`/api/jobs`)

#### Apply for Job (Students only)
```bash
POST /api/jobs/applications
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "employer_id": 123,
  "job_title": "Software Engineer"
}
```

#### Accept Application (Employers only)
```bash
POST /api/jobs/applications/<application_id>/accept
Authorization: Bearer <access_token>
```

This automatically:
- Creates a conversation between student and employer
- Sends a congratulatory message

#### Reject Application (Employers only)
```bash
POST /api/jobs/applications/<application_id>/reject
Authorization: Bearer <access_token>
```

#### Get All Applications
```bash
GET /api/jobs/applications
Authorization: Bearer <access_token>
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── job_application.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── messaging.py
│   │   └── jobs.py
│   └── utils/               # Utilities
│       ├── jwt_utils.py     # Token generation/validation
│       └── decorators.py    # Auth decorators
├── instance/                # SQLite database (auto-created)
├── config.py               # Configuration
├── app.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

## Database Schema

### Users
- id, email, username, password_hash, user_type, full_name, created_at

### Conversations
- id, created_at, updated_at

### ConversationParticipants
- id, conversation_id, user_id, unread_count, joined_at

### Messages
- id, conversation_id, sender_id, content, created_at, is_system_message

### JobApplications
- id, student_id, employer_id, job_title, status, applied_at, updated_at

## Security Notes

- Change `SECRET_KEY` in production (use environment variable)
- Passwords are hashed using Werkzeug's security functions
- JWT tokens are signed and verified
- Authorization decorators protect endpoints
- User type validation ensures role-based access
