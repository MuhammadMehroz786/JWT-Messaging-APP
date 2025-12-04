# 🚂 Railway Deployment Guide

## Prerequisites
- GitHub account
- Railway account (https://railway.app)
- Project pushed to GitHub

## 📋 Deployment Steps

### 1. Push to GitHub
Your project is already on GitHub at:
```
https://github.com/MuhammadMehroz786/JWT-Messaging-APP
```

### 2. Deploy Backend on Railway

#### Option A: Deploy via Railway Dashboard
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository: `JWT-Messaging-APP`
5. Railway will auto-detect Python and start building

#### Option B: Deploy via Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. Configure Environment Variables

In Railway dashboard, add these environment variables:

```env
# Required
SECRET_KEY=your-super-secret-key-here-change-this-in-production
FLASK_ENV=production
PORT=8000

# Optional - Railway provides DATABASE_URL if you add PostgreSQL
# DATABASE_URL will be auto-configured if you add PostgreSQL service
```

### 4. Add PostgreSQL Database (Optional)

If you want to use PostgreSQL instead of SQLite:

1. In Railway project dashboard, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically set `DATABASE_URL` environment variable
4. Your app will use PostgreSQL automatically

**Note:** For this project, SQLite works fine and will be created automatically.

### 5. Deploy Frontend (Static Site)

#### Option A: Deploy Frontend Separately on Railway

1. Create new Railway service
2. Connect same GitHub repo
3. Configure build settings:
   ```
   Build Command: cd frontend && npm install && npm run build
   Start Command: npx serve -s build -l $PORT
   Root Directory: frontend
   ```

#### Option B: Use Vercel/Netlify for Frontend

**Vercel:**
```bash
npm install -g vercel
cd frontend
vercel --prod
```

**Netlify:**
```bash
npm install -g netlify-cli
cd frontend
npm run build
netlify deploy --prod --dir=build
```

### 6. Update Frontend API URL

After backend is deployed, get your Railway backend URL (e.g., `https://your-app.up.railway.app`)

Update the API URL in `frontend/public/index.html`:

```javascript
// Change this line:
const API_URL = 'http://localhost:8000/api';

// To your Railway backend URL:
const API_URL = 'https://your-backend.up.railway.app/api';
```

### 7. Update CORS Settings

Railway backend URL needs to be allowed in CORS. The current Flask-CORS setup allows all origins, but for production, update `backend/app/__init__.py`:

```python
from flask_cors import CORS

# Allow specific origins
CORS(app, origins=[
    'http://localhost:3000',  # Local development
    'https://your-frontend.vercel.app',  # Your deployed frontend
    'https://your-frontend.netlify.app'
])
```

## 🔧 Railway Configuration Files

Your project now includes:

- `backend/Procfile` - Tells Railway how to start the app
- `backend/runtime.txt` - Specifies Python version
- `railway.json` - Railway project configuration
- `nixpacks.toml` - Build and start commands
- Updated `requirements.txt` - Includes gunicorn

## 📊 Deployment Checklist

- ✅ Gunicorn added to requirements.txt
- ✅ Config updated for Railway environment variables
- ✅ Procfile created
- ✅ Railway configuration files added
- ✅ App.py updated to use PORT environment variable
- ✅ CORS configured for production
- ✅ Database configuration supports both SQLite and PostgreSQL

## 🌐 After Deployment

Your deployed URLs will be:
- **Backend API**: `https://your-project.up.railway.app`
- **API Documentation**: `https://your-project.up.railway.app/admin/database`
- **Frontend**: Deploy separately to Vercel/Netlify

## 🐛 Troubleshooting

### Issue: Database not found
**Solution**: Railway will create SQLite database automatically on first run. For persistent storage, add PostgreSQL database.

### Issue: CORS errors
**Solution**: Make sure frontend URL is in CORS allowed origins in `app/__init__.py`

### Issue: File uploads not working
**Solution**: Railway has ephemeral filesystem. For persistent file storage:
1. Use Railway Volume (paid feature)
2. Or use cloud storage (AWS S3, Cloudinary, etc.)

### Issue: Environment variables not working
**Solution**: Make sure to set all required environment variables in Railway dashboard under "Variables" tab

## 📝 Environment Variables Reference

### Required
- `SECRET_KEY` - Your secret key for JWT signing
- `FLASK_ENV` - Set to `production` for deployment
- `PORT` - Railway sets this automatically

### Optional
- `DATABASE_URL` - Auto-set if PostgreSQL added
- `UPLOAD_FOLDER` - Path for file uploads (default: uploads/)

## 🚀 Quick Deploy Commands

```bash
# 1. Commit all changes
git add .
git commit -m "Prepare for Railway deployment"
git push origin main

# 2. Deploy to Railway (if using CLI)
railway login
railway init
railway up

# 3. Open Railway dashboard
railway open
```

## 🎉 Success!

Once deployed, you can:
- Access your API at the Railway URL
- Test all endpoints
- Share the frontend link with users
- Monitor logs in Railway dashboard
- Scale as needed

## 📚 Resources

- Railway Docs: https://docs.railway.app
- Flask Deployment: https://flask.palletsprojects.com/en/3.0.x/deploying/
- Gunicorn Docs: https://docs.gunicorn.org/

---

**Project**: JWT Messaging Application
**Created for**: Computer Network Course
**Instructor**: Sir Shaheer
