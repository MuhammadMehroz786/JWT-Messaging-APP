# Computer Network Project - Job Application Platform

A full-stack web application featuring JWT-based authentication and real-time messaging system, built for a Computer Network course project.

## Project Overview

This project demonstrates the implementation of:
- **JWT Authentication System** with access and refresh tokens
- **Real-time Messaging** between users
- **Automated Messaging** triggered by job application acceptance
- **HTTP/HTTPS Communication** using RESTful APIs
- **Role-based Authorization** (Student and Employer roles)

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **API**: RESTful HTTP/HTTPS endpoints

### Frontend
- **Framework**: React
- **Routing**: React Router DOM
- **HTTP Client**: Axios with interceptors
- **State Management**: React Hooks + localStorage

## Project Structure

```
cn-project/
├── backend/                 # Flask Backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   └── utils/          # JWT utilities & decorators
│   ├── config.py
│   ├── app.py
│   └── requirements.txt
│
└── frontend/               # React Frontend
    ├── src/
    │   ├── components/     # React components
    │   ├── pages/         # Page components
    │   ├── services/      # API service layer
    │   └── utils/         # Auth utilities
    └── package.json
```

## Key Features

### 1. Authorization System (JWT)

**Token Generation:**
- Access Token: 1 hour expiry
- Refresh Token: 30 days expiry
- Tokens are generated upon login/registration

**Token Storage:**
- Stored in browser's localStorage
- Persists across page refreshes

**Authorization Flow:**
- Access token sent in `Authorization: Bearer <token>` header
- Backend validates token and checks user role
- Decorators: `@token_required`, `@user_type_required`

**Token Refresh Mechanism:**
- Automatic refresh when access token expires
- Frontend interceptor catches 401 errors
- Sends refresh token to get new access token
- Retries failed request with new token

### 2. Messaging System

**Database Structure:**
- **Conversations**: Chat rooms between users
- **ConversationParticipants**: Tracks participants and unread counts
- **Messages**: Individual messages with sender info

**Message Flow:**
- User sends message → Backend saves it
- Updates conversation timestamp
- Increments unread count for other participants

**Automated Messaging:**
- When employer accepts job application:
  - System creates conversation (if doesn't exist)
  - Sends congratulatory message automatically
  - Notifies student with unread count

**Message Retrieval:**
- Pagination support (50 messages per page)
- Mark as read functionality
- Real-time updates

## Installation & Setup

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Server runs on http://localhost:5000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start

# App runs on http://localhost:3000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Messaging
- `GET /api/messages/conversations` - Get all conversations
- `GET /api/messages/conversations/:id/messages` - Get messages
- `POST /api/messages/conversations/:id/send` - Send message
- `POST /api/messages/conversations/:id/mark-read` - Mark as read
- `POST /api/messages/conversations/start` - Start new conversation

### Job Applications
- `POST /api/jobs/applications` - Apply for job (Students)
- `POST /api/jobs/applications/:id/accept` - Accept application (Employers)
- `POST /api/jobs/applications/:id/reject` - Reject application (Employers)
- `GET /api/jobs/applications` - Get applications

## Usage Instructions

### 1. Register Users

1. Open http://localhost:3000
2. Click "Register"
3. Create two accounts:
   - One as **Student**
   - One as **Employer**

### 2. Test Job Application Flow

1. Login as Student
2. Apply for a job (you'll need to implement job posting UI or use API directly)
3. Logout and login as Employer
4. Accept the student's application
5. Check that a conversation was automatically created
6. Verify the congratulatory message was sent

### 3. Test Messaging

1. Both users should see the conversation
2. Send messages back and forth
3. Check unread counts update correctly
4. Mark messages as read

### 4. Test Token Refresh

1. Login and wait for access token to expire (1 hour)
2. Or modify JWT_ACCESS_TOKEN_EXPIRES to 1 minute for testing
3. Make an API request after expiry
4. Token should automatically refresh
5. Request should succeed without re-login

## Security Features

- Password hashing using Werkzeug
- JWT tokens with expiration
- Role-based access control
- Token validation on every request
- Automatic token refresh
- Protected routes

## HTTP/HTTPS Communication

All communication uses HTTP/HTTPS:
- RESTful API design
- JSON request/response format
- Standard HTTP methods (GET, POST)
- Authorization headers
- CORS enabled for cross-origin requests

## Database Schema

### Users Table
- id, email, username, password_hash, user_type, full_name, created_at

### Conversations Table
- id, created_at, updated_at

### ConversationParticipants Table
- id, conversation_id, user_id, unread_count, joined_at

### Messages Table
- id, conversation_id, sender_id, content, created_at, is_system_message

### JobApplications Table
- id, student_id, employer_id, job_title, status, applied_at, updated_at

## Future Enhancements

- WebSocket integration for real-time updates
- File attachments in messages
- Group conversations
- Push notifications
- Message search functionality
- User profiles and avatars

# JWT-Messaging-APP
