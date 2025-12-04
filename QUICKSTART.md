# Quick Start Guide

Follow these steps to run your Computer Network Project.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- pip (Python package manager)
- npm (Node package manager)

## Step 1: Start the Backend

Open a terminal and run:

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

Keep this terminal open!

## Step 2: Start the Frontend

Open a **NEW** terminal and run:

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The browser will automatically open at http://localhost:3000

## Step 3: Test the Application

### Create User Accounts

1. Click "Register" on the login page
2. Create a **Student** account:
   - Email: student@example.com
   - Username: student1
   - Password: password123
   - User Type: Student
   - Full Name: John Student

3. Logout and create an **Employer** account:
   - Email: employer@example.com
   - Username: employer1
   - Password: password123
   - User Type: Employer
   - Full Name: Company HR

### Test the Messaging System

#### Method 1: Using Browser Console (Quick Test)

1. Login as Student
2. Open browser console (F12)
3. Run this to start a conversation with the employer:

```javascript
fetch('http://localhost:5000/api/messages/conversations/start', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  },
  body: JSON.stringify({ recipient_id: 2 }) // Employer ID is 2
})
.then(r => r.json())
.then(console.log)
```

4. Refresh the page - you should see the conversation!
5. Send messages back and forth

#### Method 2: Test Automated Messaging (Job Application)

1. Login as Student, open console, and run:

```javascript
// Apply for a job
fetch('http://localhost:5000/api/jobs/applications', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  },
  body: JSON.stringify({
    employer_id: 2,
    job_title: 'Software Engineer'
  })
})
.then(r => r.json())
.then(data => {
  console.log('Application submitted:', data);
  return data.application.id;
})
```

2. Logout and login as Employer
3. Open console and run (replace APPLICATION_ID with the ID from previous step):

```javascript
// Accept the application
fetch('http://localhost:5000/api/jobs/applications/APPLICATION_ID/accept', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  }
})
.then(r => r.json())
.then(console.log)
```

4. Refresh the page - you'll see:
   - A new conversation created automatically
   - A congratulatory message sent to the student

5. Login as Student to see the automated message!

### Test Token Refresh

The token refresh happens automatically, but to test it quickly:

1. Login as any user
2. Open browser console
3. Modify token expiry (for testing):
   - Go to `backend/config.py`
   - Change `JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)`
   - Restart backend server
4. Wait 1 minute
5. Try sending a message or refreshing conversations
6. The token will auto-refresh and request will succeed!

## Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
# Change port in backend/app.py, line: app.run(debug=True, host='0.0.0.0', port=5001)
# Also update frontend/src/services/api.js: const API_URL = 'http://localhost:5001/api'
```

**Module not found:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
- The terminal will ask if you want to use another port (usually 3001)
- Type 'y' and press Enter

**Dependencies error:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Make sure backend is running
- Check that API_URL in `frontend/src/services/api.js` matches your backend URL

## Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts and opens in browser
- [ ] Can register new users (Student and Employer)
- [ ] Can login with created users
- [ ] Tokens are stored in localStorage
- [ ] Can start a conversation
- [ ] Can send and receive messages
- [ ] Unread counts work correctly
- [ ] Mark as read functionality works
- [ ] Job application creates automated message
- [ ] Token refresh works automatically
- [ ] Logout clears tokens and redirects to login

## Next Steps

Now that your project is working:

1. Review the code in both backend and frontend
2. Understand the JWT token flow
3. Understand the messaging system
4. Test the automated messaging feature
5. Prepare your presentation for Sir Shaheer

## Project Features to Highlight

When presenting to your teacher:

1. **JWT Authentication:**
   - Show token generation on login
   - Demonstrate token storage in localStorage
   - Explain the token refresh mechanism

2. **Authorization System:**
   - Show the decorators in backend
   - Demonstrate role-based access (student vs employer)
   - Explain the Authorization header

3. **Messaging System:**
   - Show the database schema
   - Demonstrate sending messages
   - Show unread counts functionality

4. **Automated Messaging:**
   - Show job application acceptance
   - Demonstrate automatic conversation creation
   - Show the congratulatory message

5. **HTTP/HTTPS Communication:**
   - Explain RESTful API design
   - Show request/response flow
   - Demonstrate CORS handling

Good luck with your project! 🚀
