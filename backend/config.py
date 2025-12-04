import os
from datetime import timedelta

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for JWT - use environment variable in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database configuration - Railway compatible
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or ('sqlite:///' + os.path.join(basedir, 'instance', 'cn_project.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar'}

    # CORS configuration
    CORS_HEADERS = 'Content-Type'

    # Railway deployment settings
    PORT = int(os.environ.get('PORT', 8000))
