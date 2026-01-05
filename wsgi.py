"""
WSGI file untuk deployment PythonAnywhere
"""
import sys
import os

# Tambahkan path project ke sys.path
project_home = '/home/YOUR_USERNAME/recycly'  # Ganti YOUR_USERNAME dengan username PythonAnywhere Anda
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Import FastAPI app
from app.main import app

# ASGI to WSGI wrapper
from fastapi.middleware.wsgi import WSGIMiddleware
application = app
