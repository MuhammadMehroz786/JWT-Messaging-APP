from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# Initialize extensions
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Configure CORS to allow requests from frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "https://*.vercel.app"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })


    # Register blueprints
    from app.routes import auth, messaging, jobs, users, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(messaging.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(admin.bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
