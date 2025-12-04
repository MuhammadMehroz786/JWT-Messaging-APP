"""WSGI entry point for production servers like Gunicorn"""
from app import create_app
import os

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
