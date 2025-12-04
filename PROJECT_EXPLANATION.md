# 📚 Computer Network Project - Complete Explanation

## 🎯 Project Overview

This is a **full-stack messaging application** with JWT authentication, built for a Computer Network course. It allows:
- **Employers** to find and message students
- **Students** to receive and respond to messages
- Secure authentication with access & refresh tokens
- File sharing (up to 50MB)
- Real-time message updates

---

## 🏗️ Project Architecture

```
cn-project/
├── backend/          # Flask REST API (Python)
│   ├── app/          # Application package
│   │   ├── models/   # Database models (SQLAlchemy)
│   │   ├── routes/   # API endpoints (blueprints)
│   │   └── utils/    # JWT & decorators
│   ├── instance/     # SQLite database
│   ├── uploads/      # Uploaded files
│   ├── app.py        # Entry point
│   └── config.py     # Configuration
│
└── frontend/         # React SPA
    ├── public/       # Static files
    └── src/
        ├── components/ # React components
        ├── pages/      # Page components
        ├── services/   # API service
        └── utils/      # Helper functions
```

---

## 🔐 How Authentication Works

### 1. **Registration Flow**
```
User fills form → Frontend sends to /api/auth/register → Backend:
  1. Validates data
  2. Hashes password (bcrypt)
  3. Creates user in database
  4. Returns success
```

### 2. **Login Flow**
```
User logs in → Frontend sends to /api/auth/login → Backend:
  1. Verifies username/password
  2. Generates JWT tokens:
     - Access Token (1 hour) - for API requests
     - Refresh Token (30 days) - to get new access tokens
  3. Returns tokens + user data

Frontend:
  1. Stores tokens in localStorage
  2. Redirects to dashboard
```

### 3. **Token Usage**
Every API request includes the access token in the header:
```
Authorization: Bearer <access_token>
```

### 4. **Token Refresh**
When access token expires (401 error):
```
Frontend → Sends refresh_token to /api/auth/refresh → Backend:
  1. Validates refresh token
  2. Issues new access token
  3. Frontend retries original request
```

This happens **automatically** via axios interceptor!

---

## 💬 How Messaging Works

### 1. **Starting a Conversation** (Employer only)
```
Employer clicks "Find Students" → Modal shows all students →
Click "Message" → POST /api/messages/conversations/start →
Creates conversation with 2 participants → Redirects to chat
```

### 2. **Sending Messages**
```
User types message → Optionally attaches file → Click Send →
POST /api/messages/conversations/{id}/send (multipart/form-data)

Backend:
  1. Saves message to database
  2. If file: saves to uploads/ folder with unique name
  3. Updates conversation timestamp
  4. Increments unread count for recipient
  5. Returns message data

Frontend:
  1. Adds message to UI immediately
  2. Polling fetches updates every 3 seconds
```

### 3. **Auto-Refresh System**
The frontend uses **polling** (not WebSockets for simplicity):
- Every 3 seconds: fetches new messages
- Every 5 seconds: refreshes conversation list
- Marks messages as read when viewing

### 4. **File Transfer**
```
Upload:
  User selects file → Frontend validates size (< 50MB) →
  Sends as multipart/form-data → Backend saves with UUID filename

Download:
  User clicks download → GET /api/messages/files/{filename} →
  Backend verifies access → Sends file as download
```

---

## 🗄️ Database Schema

### Users
```sql
- id (Primary Key)
- email (Unique)
- username (Unique)
- password_hash
- user_type (student/employer)
- full_name
- created_at
```

### Conversations
```sql
- id (Primary Key)
- created_at
- updated_at
```

### ConversationParticipants
```sql
- id (Primary Key)
- conversation_id (Foreign Key → Conversations)
- user_id (Foreign Key → Users)
- unread_count (Integer)
- joined_at
```

### Messages
```sql
- id (Primary Key)
- conversation_id (Foreign Key)
- sender_id (Foreign Key → Users)
- content (Text, nullable)
- created_at
- is_system_message (Boolean)
- has_attachment (Boolean)
- file_name
- file_path
- file_size
- file_type
```

### JobApplications
```sql
- id (Primary Key)
- student_id (Foreign Key)
- employer_id (Foreign Key)
- job_title
- status (pending/accepted/rejected)
- applied_at
- updated_at
```

---

## 🔄 Request Flow Example

### Sending a Message

**Frontend (MessageView.js:88-92)**
```javascript
const response = await messagingAPI.sendMessage(
  conversation.id,
  newMessage,
  selectedFile
);
```

**API Service (api.js:94-103)**
```javascript
sendMessage: (conversationId, content, file) => {
  const formData = new FormData();
  if (content) formData.append('content', content);
  if (file) formData.append('file', file);
  return api.post(`/messages/conversations/${conversationId}/send`, formData);
}
```

**Backend Route (messaging.py:100-200)**
```python
@bp.route('/conversations/<int:conversation_id>/send', methods=['POST'])
@token_required
def send_message(current_user, conversation_id):
    # 1. Verify user is participant
    # 2. Handle file upload if present
    # 3. Create message in database
    # 4. Update conversation timestamp
    # 5. Increment unread count
    # 6. Return message data
```

**Database Model (conversation.py:78-93)**
```python
def to_dict(self):
    return {
        'id': self.id,
        'sender_id': self.sender_id,
        'content': self.content,
        'created_at': self.created_at.isoformat() + 'Z',
        # ... file fields
    }
```

---

## 🛡️ Security Features

### 1. **Password Security**
- Passwords hashed with `bcrypt` (werkzeug.security)
- Never stored in plain text
- Salt automatically generated

### 2. **JWT Token Security**
- Signed with SECRET_KEY
- Short-lived access tokens (1 hour)
- Refresh tokens for long sessions (30 days)
- Tokens validated on every request

### 3. **Authorization**
```python
@token_required  # Verifies JWT token
@user_type_required('employer')  # Checks user role
def employer_only_endpoint(current_user):
    pass
```

### 4. **File Upload Security**
- File type validation (allowed extensions)
- File size limit (50MB)
- Unique filename generation (UUID)
- Access control (only participants can download)

### 5. **CORS Configuration**
- Configured to accept requests from React frontend
- Prevents unauthorized cross-origin requests

---

## 📊 Data Flow Diagrams

### Authentication Flow
```
┌─────────┐        ┌──────────┐        ┌──────────┐
│ Browser │───────▶│ React App│───────▶│ Flask API│
└─────────┘        └──────────┘        └──────────┘
     │                   │                    │
     │ 1. Login Form     │                    │
     │──────────────────▶│                    │
     │                   │ 2. POST /login     │
     │                   │───────────────────▶│
     │                   │                    │ 3. Verify password
     │                   │                    │    Generate tokens
     │                   │ 4. Return tokens   │
     │                   │◀───────────────────│
     │ 5. Store tokens   │                    │
     │   in localStorage │                    │
     │◀──────────────────│                    │
     │                   │                    │
     │ 6. Redirect to    │                    │
     │    Dashboard      │                    │
     │◀──────────────────│                    │
```

### Message Sending Flow
```
┌──────┐  ┌──────┐  ┌─────────┐  ┌──────────┐
│ User │  │ React│  │ Axios   │  │ Flask API│
└──────┘  └──────┘  └─────────┘  └──────────┘
   │         │          │              │
   │ Type &  │          │              │
   │ Send    │          │              │
   │────────▶│          │              │
   │         │ Validate │              │
   │         │ & Prepare│              │
   │         │ FormData │              │
   │         │─────────▶│              │
   │         │          │ POST with    │
   │         │          │ Bearer token │
   │         │          │─────────────▶│
   │         │          │              │ Verify token
   │         │          │              │ Check access
   │         │          │              │ Save message
   │         │          │              │ Save file
   │         │          │ 201 Created  │
   │         │          │◀─────────────│
   │         │◀─────────│              │
   │ Update  │          │              │
   │ UI      │          │              │
   │◀────────│          │              │
```

---

## 🚀 How to Run the Project

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
# Runs on http://localhost:8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
# Runs on http://localhost:3000
```

### View Database
Open browser: `http://localhost:8000/admin/database`

---

## 📁 Key Files Explained

### Backend

**app.py** - Entry point
- Creates Flask app
- Runs development server on port 8000

**config.py** - Configuration
- Database URL
- JWT expiration times
- File upload settings
- Max file size (50MB)

**app/__init__.py** - App Factory
- Initializes Flask extensions (SQLAlchemy, CORS)
- Registers all blueprints (routes)
- Creates database tables

**app/models/** - Database Models
- Define table structure
- Include relationships
- Provide `to_dict()` methods for JSON serialization

**app/routes/** - API Endpoints
- **auth.py**: Register, Login, Refresh Token
- **messaging.py**: Conversations, Messages, File Upload
- **users.py**: Get students list (employer only)
- **jobs.py**: Job applications
- **admin.py**: Database viewer

**app/utils/jwt_utils.py** - Token Management
- `generate_access_token()`: Creates 1-hour token
- `generate_refresh_token()`: Creates 30-day token
- `decode_token()`: Validates and decodes tokens

**app/utils/decorators.py** - Authorization
- `@token_required`: Verifies JWT on every request
- `@user_type_required()`: Checks user role

### Frontend

**src/index.js** - Entry Point
- Renders App component
- Sets up React

**src/App.js** - Main Component
- React Router configuration
- Protected routes
- Authentication checks

**src/services/api.js** - API Communication
- Axios instance with base URL
- Request interceptor: Adds Bearer token
- Response interceptor: Auto-refreshes expired tokens
- All API methods (login, register, sendMessage, etc.)

**src/components/auth/** - Authentication UI
- Login.js: Login form
- Register.js: Registration form

**src/components/messaging/** - Messaging UI
- Messaging.js: Main container (conversations + chat)
- ConversationList.js: Shows all conversations
- MessageView.js: Chat interface + file upload
- StartConversationModal.js: Find students modal

**src/pages/Dashboard.js** - Main Page
- Shows after login
- Displays messaging interface

---

## 🔧 Configuration Details

### JWT Configuration
```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)    # Short-lived
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)   # Long-lived
SECRET_KEY = 'dev-secret-key-change-in-production'
```

### File Upload Configuration
```python
UPLOAD_FOLDER = 'uploads/'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg',
                     'gif', 'doc', 'docx', 'xls', 'xlsx',
                     'zip', 'rar'}
```

### CORS Configuration
```python
CORS(app)  # Allows React frontend to make requests
```

---

## 🐛 Common Issues & Solutions

### Issue: "Failed to start conversation"
**Solution**: Database was out of sync. Fixed by recreating database with file attachment fields.

### Issue: "5 hrs ago" timestamp bug
**Solution**: Added 'Z' suffix to timestamps to indicate UTC timezone.

### Issue: Port 5000 already in use
**Solution**: macOS AirPlay uses 5000. Changed backend to port 8000.

---

## 📝 API Endpoints Summary

### Authentication
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Messaging
- `GET /api/messages/conversations` - Get all conversations
- `GET /api/messages/conversations/{id}/messages` - Get messages
- `POST /api/messages/conversations/{id}/send` - Send message
- `POST /api/messages/conversations/{id}/mark-read` - Mark as read
- `POST /api/messages/conversations/start` - Start new conversation
- `GET /api/messages/files/{filename}` - Download file

### Users
- `GET /api/users/students` - Get all students (employer only)

### Job Applications
- `POST /api/jobs/applications` - Apply for job
- `POST /api/jobs/applications/{id}/accept` - Accept application
- `POST /api/jobs/applications/{id}/reject` - Reject application
- `GET /api/jobs/applications` - Get all applications

### Admin
- `GET /admin/database` - View database (HTML)
- `GET /admin/database/json` - View database (JSON)

---

## 🎓 Technologies Used

**Backend:**
- Flask (Web framework)
- SQLAlchemy (ORM)
- SQLite (Database)
- PyJWT (JWT tokens)
- Werkzeug (Password hashing)
- Flask-CORS (Cross-origin requests)

**Frontend:**
- React (UI framework)
- React Router (Navigation)
- Axios (HTTP client)
- CSS3 (Styling)

---

## 📊 Project Features Checklist

✅ JWT Authentication (Access + Refresh tokens)
✅ User Registration & Login
✅ Automatic token refresh
✅ Role-based authorization (Student/Employer)
✅ Messaging system
✅ Conversation management
✅ File upload/download (50MB limit)
✅ Real-time updates (polling)
✅ Unread message badges
✅ Mark messages as read
✅ Employer can find students
✅ Students cannot initiate conversations
✅ Job application system
✅ Automated messaging on job acceptance
✅ Database viewer (admin panel)

---

## 🎯 Learning Objectives Achieved

1. ✅ **Computer Networking Concepts**
   - HTTP/HTTPS protocol
   - RESTful API design
   - Request/Response cycle
   - Client-Server architecture

2. ✅ **Security**
   - JWT token-based authentication
   - Password hashing
   - Authorization & access control
   - Secure file handling

3. ✅ **Full-Stack Development**
   - Backend API development
   - Frontend SPA development
   - Database design & relationships
   - API integration

4. ✅ **Real-World Application**
   - User authentication flow
   - Real-time messaging
   - File transfer
   - Role-based features

---

## 📚 Further Reading

- **JWT**: https://jwt.io/introduction
- **Flask Documentation**: https://flask.palletsprojects.com/
- **React Documentation**: https://react.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **HTTP Status Codes**: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

---

**Created for Computer Network Course**
**Instructor: Sir Shaheer**
**Technology Stack: Flask + React + JWT + SQLite*
