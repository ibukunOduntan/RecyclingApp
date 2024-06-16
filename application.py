from app import app  # Importing the Flask app instance from app.py

# This is the entry point for Gunicorn
application = app  # Rename app to application as required by some WSGI servers
