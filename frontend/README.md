# Frontend - JWT Messaging Application

## Dark-Themed Modern UI

This frontend features a beautiful, modern dark-themed interface built with vanilla JavaScript and integrated with the Flask backend.

### Features

- **Modern Dark Theme**: Sleek purple-to-blue gradient design (#7c4dff → #448aff)
- **JWT Authentication**: Login/Register with automatic token refresh
- **Real-time Messaging**: Auto-updates every 3 seconds via polling
- **File Upload/Download**: Support for files up to 50MB
- **Role-Based UI**: Different features for Students and Employers
- **Responsive Design**: Works on mobile and desktop
- **Font Awesome Icons**: Beautiful iconography throughout

### How to Run

```bash
npm install
npm start
```

The app will open at http://localhost:3000

### UI Components

#### Authentication
- Login form with username/password
- Registration form with user type selection
- Error handling with visual feedback
- Success messages

#### Dashboard
- **Navbar**: User info, logout button
- **Sidebar**: Conversation list with unread badges
- **Chat Area**: Message bubbles, file attachments, input field
- **Find Students Modal**: For employers to start conversations

#### Features
- Automatic token refresh on 401 errors
- Real-time polling for new messages (3s) and conversations (5s)
- File upload with size validation (50MB max)
- Download files from messages
- Mark messages as read automatically
- Relative timestamps (e.g., "5m ago", "2h ago")

### API Integration

All API endpoints are fully integrated:
- `/api/auth/login` - User authentication
- `/api/auth/register` - New user registration
- `/api/auth/refresh` - Token refresh
- `/api/messages/conversations` - Get all conversations
- `/api/messages/conversations/:id/messages` - Get messages
- `/api/messages/conversations/:id/send` - Send message with optional file
- `/api/messages/conversations/:id/mark-read` - Mark as read
- `/api/messages/conversations/start` - Start new conversation
- `/api/messages/files/:filename` - Download file
- `/api/users/students` - Get all students (employer only)

### Design System

**Colors:**
- Primary Gradient: `linear-gradient(135deg, #7c4dff 0%, #448aff 100%)`
- Background: `#121212` (Deep black)
- Surface: `#1e1e1e` (Cards/Navbar)
- Text Primary: `#e0e0e0`
- Text Secondary: `#b0b0b0`
- Text Muted: `#6e6e6e`

**Typography:**
- Font: Segoe UI, Roboto, Helvetica, Arial, sans-serif
- Regular: 14px
- Small: 12px
- Large: 16-20px

**Components:**
- Rounded buttons with gradient background
- Pill-shaped input fields
- Circular avatars with gradient background
- Role badges (Student/Employer)
- Unread count badges
- File attachment cards

### Files

- `public/index.html` - Main dark-themed UI (default)
- `public/index.html.backup` - Original React entry point (backup)
- `public/dark-ui.html` - Standalone dark UI (copy)
- `src/` - Original React components (alternative UI)

### Technology Stack

- HTML5
- CSS3 (Custom properties, Flexbox, Grid)
- JavaScript (ES6+)
- Axios for HTTP requests
- Font Awesome for icons

### Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

### Notes

- The UI is fully standalone and doesn't require React
- All state is managed in vanilla JavaScript
- Tokens are stored in localStorage
- Polling intervals are automatically cleaned up on logout
- File size limit is enforced on both frontend and backend
