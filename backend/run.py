"""
Flask application entry point for the Fake News Image Detection Platform.
This script creates and runs the Flask application with the specified configuration.
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
