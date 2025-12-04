# Railway Deployment Guide

This guide will help you deploy your CN Project (Computer Network Messaging Application) to Railway.

## Prerequisites

- A Railway account (sign up at https://railway.app)
- A GitHub account
- Git installed on your computer

## Step 1: Push Your Code to GitHub

1. **Check your code is ready:**
   ```bash
   cd "/Users/apple/Desktop/daa/untitled folder/cn-project"
   git status
   ```

2. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   ```

3. **Create a new GitHub repository:**
   - Go to https://github.com/new
   - Name your repository (e.g., "cn-project")
   - Don't initialize with README
   - Click "Create repository"

4. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy Backend to Railway

1. **Create Railway Project:**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Backend:**
   - Railway detects the backend automatically
   - Go to Settings > Root Directory: `backend`

3. **Add Environment Variables:**
   ```
   SECRET_KEY=<generate-random-64-char-string>
   FLASK_ENV=production
   ```

4. **Generate Domain:**
   - Settings > Networking > Generate Domain
   - Copy URL (e.g., https://your-app.railway.app)

## Step 3: Deploy Frontend

**Option A: Railway**
- Add new service from same repo
- Root Directory: `frontend`
- Environment Variable:
  ```
  REACT_APP_API_URL=https://your-backend.railway.app/api
  ```

**Option B: Vercel (Recommended)**
- Import project to Vercel
- Root: `frontend`
- Add environment variable:
  ```
  REACT_APP_API_URL=https://your-backend.railway.app/api
  ```

## Step 4: Test

Visit your frontend URL and test login/messaging!

## Environment Variables Summary

**Backend:**
- `SECRET_KEY`: Random secret key
- `FLASK_ENV`: production

**Frontend:**
- `REACT_APP_API_URL`: Your backend URL + /api

---

**Your app is now live!**
