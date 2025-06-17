import os
import sys

# Add your project directory to the sys.path
project_home = '/home/yourusername/fake-news-detector/ml_service'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your app from main
from main import app

# This is the PythonAnywhere WSGI configuration
application = app
