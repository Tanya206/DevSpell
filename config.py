import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_CONFIG = {
    'client_id': os.getenv('GITHUB_CLIENT_ID'),
    'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
    'redirect_uri': 'http://localhost:8501/Callback',
    'scope': 'repo user'
}

FIREBASE_CONFIG = {
    'config_path': os.getenv('FIREBASE_CONFIG_PATH'),
    'project_id': os.getenv('FIREBASE_PROJECT_ID')
}