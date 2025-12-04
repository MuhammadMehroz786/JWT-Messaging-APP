from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable (for Railway) or use 8000
    port = int(os.environ.get('PORT', 8000))
    # Disable debug in production
    debug = os.environ.get('FLASK_ENV') != 'production'
    # Run the application
    app.run(debug=debug, host='0.0.0.0', port=port)
