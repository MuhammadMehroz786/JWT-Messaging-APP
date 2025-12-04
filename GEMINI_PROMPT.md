# Prompt for Gemini: Create Web UI for Messaging Application

## Project Overview
I need you to create a complete React-based web UI for a messaging application with JWT authentication. The backend API is already built using Flask and running on `http://localhost:8000/api`.

## Application Features
This is a messaging platform where:
- **Employers** can find and message students
- **Students** can receive and respond to messages (but cannot initiate conversations)
- Users can send text messages and file attachments (up to 50MB)
- Real-time message updates using polling
- JWT-based authentication with automatic token refresh

## Backend API Endpoints

### Authentication
```
POST /api/auth/register
Body: { username, email, password, user_type: "student" | "employer", full_name }
Response: { message, user }

POST /api/auth/login
Body: { username, password }
Response: { access_token, refresh_token, user }

POST /api/auth/refresh
Body: { refresh_token }
Response: { access_token }

GET /api/auth/me
Headers: { Authorization: "Bearer <token>" }
Response: { user }
```

### Messaging
```
GET /api/messages/conversations
Headers: { Authorization: "Bearer <token>" }
Response: { conversations: [...] }

GET /api/messages/conversations/{id}/messages?page=1&per_page=50
Headers: { Authorization: "Bearer <token>" }
Response: { messages: [...], page, per_page, total, pages }

POST /api/messages/conversations/{id}/send
Headers: { Authorization: "Bearer <token>", Content-Type: "multipart/form-data" }
Body: FormData with { content?, file? }
Response: { message: "Message sent successfully", data: {...} }

POST /api/messages/conversations/{id}/mark-read
Headers: { Authorization: "Bearer <token>" }
Response: { message: "Messages marked as read" }

POST /api/messages/conversations/start
Headers: { Authorization: "Bearer <token>" }
Body: { recipient_id }
Response: { message: "Conversation started", conversation: {...} }

GET /api/messages/files/{filename}
Headers: { Authorization: "Bearer <token>" }
Response: File download
```

### Users
```
GET /api/users/students
Headers: { Authorization: "Bearer <token>" }
Response: { students: [...] }
Note: Only accessible by employers
```

## UI Requirements

### 1. Authentication Pages

#### Login Page
- Clean, centered login form
- Fields: Username, Password
- "Login" button
- Link to register page
- Display error messages for failed login
- Gradient purple theme (#667eea to #764ba2)

#### Register Page
- Registration form with fields:
  - Username (required, unique)
  - Email (required, unique)
  - Password (required, min 6 characters)
  - Full Name (required)
  - User Type (dropdown: Student or Employer)
- "Register" button
- Link to login page
- Show validation errors
- Same gradient purple theme

### 2. Dashboard/Main Page

#### Layout
```
┌─────────────────────────────────────────────────┐
│  Navbar (Logo, User Info, Logout)              │
├──────────────┬──────────────────────────────────┤
│              │                                   │
│ Conversation │    Message View                  │
│ List         │    (Chat Interface)              │
│ (350px)      │                                   │
│              │                                   │
│              │                                   │
│              │                                   │
└──────────────┴──────────────────────────────────┘
```

#### Conversation List (Left Sidebar)
- Header: "Messages"
- "Find Students" button (only for employers)
- List of conversations showing:
  - Avatar with first letter of name (circular, gradient background)
  - Participant name (other person in conversation)
  - Last message preview (truncated)
  - Timestamp (relative: "Just now", "5m ago", "2h ago", etc.)
  - Unread badge (purple circle with count)
- Active conversation highlighted with light blue background
- Hover effect on conversation items
- Scrollable list

#### Message View (Right Main Area)
- Header showing:
  - Avatar of other participant
  - Name of other participant
  - User type badge (Student/Employer)
- Messages area:
  - Messages displayed in chat bubble format
  - Sent messages: Right-aligned, purple gradient background, white text
  - Received messages: Left-aligned, white background, dark text
  - File attachments shown with:
    - File icon (📎)
    - File name
    - File size
    - Download button
  - Timestamps below each message
  - Auto-scroll to bottom on new messages
- Input area at bottom:
  - File attachment button (📎 icon, left side)
  - Text input field (rounded corners)
  - Send button (purple gradient)
  - Show selected file preview with remove option
  - Disable send when empty (no text and no file)

#### Empty State
When no conversation is selected, show centered text:
"Select a conversation to start messaging" with "Start Conversation" button for employers

### 3. Find Students Modal (Employer Only)
- Modal overlay with centered dialog
- Title: "Find Students"
- Close button (×) in top right
- List of all students:
  - Avatar (circular with first letter)
  - Full name
  - Email
  - "Message" button on right
- Clicking "Message" creates conversation and opens chat
- Show "No students registered yet" if empty

### 4. Navbar
- Logo/App name on left
- User info on right:
  - Username
  - User type badge
  - Logout button

## Technical Requirements

### State Management
- Use React hooks (useState, useEffect)
- Store tokens in localStorage:
  - `access_token`
  - `refresh_token`
  - `user` (user object)

### API Communication
- Use axios for HTTP requests
- Create axios instance with base URL: `http://localhost:8000/api`
- Request interceptor: Add Bearer token to Authorization header
- Response interceptor: Handle 401 errors by refreshing token automatically
- If token refresh fails, clear localStorage and redirect to login

### Routing
- Use React Router v6
- Routes:
  - `/` - Redirect to /login or /dashboard based on auth
  - `/login` - Login page
  - `/register` - Register page
  - `/dashboard` - Main messaging interface (protected)
- Protected routes: Check if tokens exist in localStorage

### Auto-Refresh
- Poll for new messages every 3 seconds when viewing a conversation
- Poll for conversation list updates every 5 seconds
- Stop polling when component unmounts

### File Upload
- Validate file size < 50MB before upload
- Use FormData to send file with message
- Show preview of selected file before sending
- Display error if file too large

### Time Formatting
- Convert ISO 8601 timestamps to relative time:
  - < 1 minute: "Just now"
  - < 60 minutes: "Xm ago"
  - < 24 hours: "Xh ago"
  - < 7 days: "Xd ago"
  - Older: Show date (MM/DD/YYYY)

## Design Specifications

### Color Scheme
```css
Primary Gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Background: #f8f9fa
White: #ffffff
Text Dark: #333333
Text Light: #666666
Text Muted: #999999
Border: #e0e0e0
Hover Background: #f8f9fa
Selected Background: #e3f2fd
```

### Typography
```css
Font Family: Arial, sans-serif
Button Font: 600 weight
Header: 18-20px
Body: 14px
Small: 12px
Timestamps: 11px
```

### Spacing
```css
Container Padding: 20px
Card Padding: 15px
Button Padding: 12px 30px
Input Padding: 12px 15px
Gap Between Elements: 10-15px
```

### Components Styling

#### Buttons
- Border radius: 25px (rounded pills)
- Purple gradient background
- White text
- Hover: opacity 0.9
- Disabled: opacity 0.5

#### Inputs
- Border: 1px solid #e0e0e0
- Border radius: 25px
- Focus: border color #667eea
- Padding: 12px 15px

#### Cards/Containers
- Background: white
- Border radius: 8px
- Box shadow: 0 2px 4px rgba(0,0,0,0.1)

#### Avatars
- Circular (border-radius: 50%)
- Size: 50px for conversations, 40px for header
- Gradient background matching primary
- White text, centered, bold

## Project Structure
```
src/
├── App.js                 # Main component with routing
├── index.js              # Entry point
├── index.css             # Global styles
├── components/
│   ├── auth/
│   │   ├── Login.js
│   │   ├── Register.js
│   │   └── Auth.css
│   └── messaging/
│       ├── Messaging.js            # Main container
│       ├── ConversationList.js     # Left sidebar
│       ├── MessageView.js          # Chat interface
│       ├── StartConversationModal.js
│       └── Messaging.css
├── pages/
│   ├── Dashboard.js
│   └── Dashboard.css
├── services/
│   └── api.js            # Axios instance and API methods
└── utils/
    └── auth.js           # Auth helper functions
```

## API Service Structure

### api.js
Should include:
```javascript
// Axios instance with interceptors
const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

// Request interceptor - add token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle 401
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401 && !error.config._retry) {
      // Try to refresh token
      // If successful, retry original request
      // If failed, logout
    }
    return Promise.reject(error);
  }
);

// Export API methods
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  refreshToken: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),
  getCurrentUser: () => api.get('/auth/me')
};

export const messagingAPI = {
  getConversations: () => api.get('/messages/conversations'),
  getMessages: (conversationId, page = 1) => api.get(`/messages/conversations/${conversationId}/messages`, { params: { page, per_page: 50 } }),
  sendMessage: (conversationId, content, file) => {
    const formData = new FormData();
    if (content) formData.append('content', content);
    if (file) formData.append('file', file);
    return api.post(`/messages/conversations/${conversationId}/send`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  markAsRead: (conversationId) => api.post(`/messages/conversations/${conversationId}/mark-read`),
  startConversation: (recipientId) => api.post('/messages/conversations/start', { recipient_id: recipientId }),
  downloadFile: (filename) => api.get(`/messages/files/${filename}`, { responseType: 'blob' })
};

export const usersAPI = {
  getStudents: () => api.get('/users/students')
};
```

## Implementation Steps

1. **Setup React Project**
   - Create React app
   - Install dependencies: react-router-dom, axios
   - Setup folder structure

2. **Create API Service**
   - Implement axios instance
   - Add interceptors for auth
   - Create all API methods

3. **Build Authentication**
   - Login component
   - Register component
   - Auth utilities (isAuthenticated, logout)
   - Protected routes

4. **Build Messaging UI**
   - Conversation list component
   - Message view component
   - Find students modal
   - Main messaging container

5. **Implement Features**
   - File upload/download
   - Auto-refresh with polling
   - Unread badges
   - Time formatting
   - Mark as read

6. **Styling**
   - Apply purple gradient theme
   - Responsive design
   - Hover effects
   - Loading states

## Important Notes

- All timestamps from backend end with 'Z' (UTC timezone)
- Parse them with `new Date(timestamp)` in JavaScript
- File uploads use multipart/form-data, not JSON
- Token refresh should be automatic and transparent
- Students cannot see "Find Students" button
- Max file size: 50MB (validate before upload)
- Empty message with no file cannot be sent

## Example Response Formats

### User Object
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "user_type": "employer",
  "full_name": "John Doe",
  "created_at": "2025-12-04T00:00:00Z"
}
```

### Conversation Object
```json
{
  "id": 1,
  "created_at": "2025-12-04T00:00:00Z",
  "updated_at": "2025-12-04T00:30:00Z",
  "last_message": {
    "id": 5,
    "content": "Hello!",
    "created_at": "2025-12-04T00:30:00Z",
    "sender_id": 2
  },
  "unread_count": 3,
  "other_participant": {
    "id": 2,
    "username": "jane_smith",
    "full_name": "Jane Smith",
    "user_type": "student"
  }
}
```

### Message Object
```json
{
  "id": 1,
  "conversation_id": 1,
  "sender_id": 2,
  "content": "Hello there!",
  "created_at": "2025-12-04T00:30:00Z",
  "has_attachment": true,
  "file_name": "document.pdf",
  "file_path": "abc123.pdf",
  "file_size": 1048576,
  "file_type": "application/pdf"
}
```

## Additional Features to Consider

1. **Loading States**
   - Show spinner while fetching data
   - Disable buttons during API calls

2. **Error Handling**
   - Display error messages for failed requests
   - Show validation errors from backend

3. **Empty States**
   - "No conversations yet" when list is empty
   - "No messages yet" when conversation is empty
   - "No students registered" in find modal

4. **Accessibility**
   - Proper ARIA labels
   - Keyboard navigation
   - Focus management in modals

5. **Responsive Design**
   - Mobile-friendly layout
   - Collapsible sidebar on small screens

## Success Criteria

The UI is complete when:
- ✅ Users can register and login
- ✅ Employers can find and message students
- ✅ Students can respond to messages
- ✅ Messages update automatically (polling)
- ✅ Files can be uploaded and downloaded
- ✅ Tokens refresh automatically
- ✅ UI matches the purple gradient design
- ✅ All API endpoints are integrated
- ✅ Unread badges work correctly
- ✅ Timestamps display correctly

---

Please create a complete React application following these specifications. Include all components, styling, and functionality described above. Make sure to implement proper error handling, loading states, and a polished user experience.
