import os
import json
from typing import Dict, List, Any
from pathlib import Path
import yaml
import zipfile
import io

class ProjectConfig:
    """Configuration class for project generation"""
    def __init__(self, project_data: Dict[str, Any]):
        self.project_data = project_data
        self.project_name = project_data.get('name', 'my_project')
        self.project_type = project_data.get('project_type', 'Web Application')
        self.frontend = project_data.get('frontend', 'React')
        self.backend = project_data.get('backend', 'Node.js/Express')
        self.database = project_data.get('database', 'MongoDB')

    def get_project_structure(self) -> Dict[str, Any]:
        """Generate recommended project structure based on tech stack"""
        structure = {
            "frontend": self._get_frontend_structure(),
            "backend": self._get_backend_structure(),
            "database": self._get_database_structure(),
            "configurations": self._get_config_structure()
        }
        return structure

    def _get_frontend_structure(self) -> Dict[str, List[str]]:
        frontend_map = {
            "React": ["src/components", "src/pages", "src/hooks", "src/styles", "public"],
            "Vue.js": ["src/components", "src/views", "src/assets", "public"],
            "Angular": ["src/app", "src/assets", "src/environments"],
            "Next.js": ["pages", "components", "styles", "public"],
            "Svelte": ["src/components", "src/routes", "public"],
            "HTML/CSS/JS(Vanilla)": ["index.html", "css", "js", "assets"]
        }
        return {
            "directories": frontend_map.get(self.frontend, []),
            "framework": self.frontend
        }

    def _get_backend_structure(self) -> Dict[str, List[str]]:
        backend_map = {
            "Node.js/Express": ["src/controllers", "src/routes", "src/models", "src/middleware", "config"],
            "Django": ["app", "models", "views", "templates", "static"],
            "Flask": ["app", "models", "routes", "templates", "static"],
            "FastAPI": ["src/api", "src/models", "src/services", "config"],
            "PHP": ["public", "src", "config", "templates"],
            "Static Files": ["public"]
        }
        return {
            "directories": backend_map.get(self.backend, []),
            "framework": self.backend
        }

    def _get_database_structure(self) -> Dict[str, Any]:
        database_map = {
            "MongoDB": {
                "config": ["database_connection.py", "database_config.json"],
                "models": ["user_model.py", "data_model.py"]
            },
            "PostgreSQL": {
                "migrations": ["initial_schema.sql"],
                "config": ["db_config.py"]
            },
            "SQLite": {
                "database": ["initial_schema.sql"],
                "config": ["db_config.py"]
            },
            "Local Storage": {
                "storage": ["storage_utils.js"]
            }
        }
        return database_map.get(self.database, {})

    def _get_config_structure(self) -> Dict[str, List[str]]:
        return {
            "environment": [".env", ".env.example"],
            "deployment": ["Dockerfile", "docker-compose.yml"],
            "ci_cd": [".github/workflows/main.yml"]
        }

class ProjectGenerator:
    """Generates project files based on project configuration"""
    
    def __init__(self, project_config: ProjectConfig):
        self.config = project_config
        self.project_name = project_config.project_name.lower().replace(" ", "_")
        
    def generate_project_files(self) -> Dict[str, str]:
        """Generate all project files based on configuration"""
        files = {}
        
        # Frontend files
        files.update(self._generate_frontend_files())
        
        # Backend files
        files.update(self._generate_backend_files())
        
        # Database files
        files.update(self._generate_database_files())
        
        # Configuration files
        files.update(self._generate_config_files())
        
        # README
        files[f"{self.project_name}/README.md"] = self._generate_readme()
        
        return files
    
    def _generate_frontend_files(self) -> Dict[str, str]:
        frontend_mapping = {
            "React": self._generate_react_files,
            "Vue.js": self._generate_vue_files,
            "Next.js": self._generate_nextjs_files,
            "HTML/CSS/JS(Vanilla)": self._generate_vanilla_files
        }
        generator = frontend_mapping.get(self.config.frontend, self._generate_default_frontend)
        return generator()
    
    def _generate_react_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/frontend/package.json": json.dumps({
                "name": self.project_name,
                "version": "0.1.0",
                "dependencies": {
                    "react": "^17.0.2",
                    "react-dom": "^17.0.2"
                }
            }, indent=2),
            f"{self.project_name}/frontend/src/App.js": """
import React from 'react';

function App() {
  return (
    <div>
      <h1>{self.project_name} Application</h1>
    </div>
  );
}

export default App;
            """
        }
    
    def _generate_backend_files(self) -> Dict[str, str]:
        backend_mapping = {
            "Node.js/Express": self._generate_express_files,
            "Django": self._generate_django_files,
            "Flask": self._generate_flask_files,
            "Static Files": self._generate_static_files
        }
        generator = backend_mapping.get(self.config.backend, self._generate_default_backend)
        return generator()
    
    def _generate_express_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/backend/package.json": json.dumps({
                "name": f"{self.project_name}-backend",
                "version": "1.0.0",
                "dependencies": {
                    "express": "^4.17.1",
                    "mongoose": "^5.12.3"
                }
            }, indent=2),
            f"{self.project_name}/backend/server.js": """
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Welcome to {self.project_name}');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
            """
        }
    
    def _generate_database_files(self) -> Dict[str, str]:
        db_mapping = {
            "MongoDB": self._generate_mongodb_files,
            "PostgreSQL": self._generate_postgresql_files,
            "SQLite": self._generate_sqlite_files
        }
        generator = db_mapping.get(self.config.database, lambda: {})
        return generator()
    
    def _generate_mongodb_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/database/connection.py": """
import pymongo
from pymongo import MongoClient

def get_database():
    # Replace with your MongoDB connection string
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['{self.project_name}_db']
            """
        }
    
    def _generate_config_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/.env.example": """
# Project Configuration
PROJECT_NAME={self.project_name}
ENVIRONMENT=development

# Database Configuration
DB_HOST=localhost
DB_PORT=27017
DB_NAME={self.project_name}_db

# Server Configuration
PORT=5000
            """,
            f"{self.project_name}/.github/workflows/main.yml": """
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python -m unittest discover tests
            """
        }
    
    def _generate_readme(self) -> str:
        return f"""
# {self.project_name.replace('_', ' ').title()}

## Project Overview
A {self.config.project_type} built with {self.config.frontend} and {self.config.backend}.

## Technology Stack
- Frontend: {self.config.frontend}
- Backend: {self.config.backend}
- Database: {self.config.database}

## Setup Instructions
1. Clone the repository
2. Install dependencies
3. Configure environment variables
4. Run the application
"""
    
    # Add more methods for other specific file generations as needed

    def _generate_default_frontend(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/frontend/index.html": """
<!DOCTYPE html>
<html>
<head>
    <title>{self.project_name}</title>
</head>
<body>
    <h1>Welcome to {self.project_name}</h1>
</body>
</html>
            """
        }

    def _generate_default_backend(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/backend/main.py": """
def main():
    print("Default backend for {self.project_name}")

if __name__ == "__main__":
    main()
            """
        }
    
    def _generate_vue_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/frontend/package.json": json.dumps({
                "name": self.project_name,
                "version": "0.1.0",
                "dependencies": {
                    "vue": "^3.2.31",
                    "vue-router": "^4.0.12"
                }
            }, indent=2),
            f"{self.project_name}/frontend/src/App.vue": """
<template>
  <div id="app">
    <h1>{{ projectName }} Application</h1>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      projectName: '{self.project_name}'
    }
  }
}
</script>
            """
        }
    
    def _generate_nextjs_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/frontend/package.json": json.dumps({
                "name": self.project_name,
                "version": "0.1.0",
                "dependencies": {
                    "next": "^12.1.0",
                    "react": "^17.0.2",
                    "react-dom": "^17.0.2"
                }
            }, indent=2),
            f"{self.project_name}/frontend/pages/index.js": """
import Head from 'next/head'

export default function Home() {
  return (
    <div>
      <Head>
        <title>{self.project_name}</title>
      </Head>

      <main>
        <h1>{self.project_name} Application</h1>
      </main>
    </div>
  )
}
            """
        }
    
    def _generate_vanilla_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/frontend/index.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{self.project_name}</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <h1>{self.project_name} Application</h1>
    <script src="js/main.js"></script>
</body>
</html>
            """,
            f"{self.project_name}/frontend/css/styles.css": """
body {
    font-family: Arial, sans-serif;
    text-align: center;
    padding: 20px;
}
            """,
            f"{self.project_name}/frontend/js/main.js": """
document.addEventListener('DOMContentLoaded', () => {
    console.log('{self.project_name} is running');
});
            """
        }
    
    def _generate_django_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/backend/requirements.txt": """
Django==3.2.9
gunicorn==20.1.0
            """,
            f"{self.project_name}/backend/manage.py": """
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
            """
        }
    
    def _generate_flask_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/backend/requirements.txt": """
Flask==2.0.2
gunicorn==20.1.0
            """,
            f"{self.project_name}/backend/app.py": """
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to {self.project_name}'

if __name__ == '__main__':
    app.run(debug=True)
            """
        }
    
    def _generate_static_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/backend/index.html": """
<!DOCTYPE html>
<html>
<head>
    <title>{self.project_name}</title>
</head>
<body>
    <h1>Static Site for {self.project_name}</h1>
</body>
</html>
            """
        }
    
    def _generate_postgresql_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/database/init.sql": """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
            """
        }
    
    def _generate_sqlite_files(self) -> Dict[str, str]:
        return {
            f"{self.project_name}/database/init.sql": """
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL
);
            """
        }   
    
  

    def generate_zip_file(self) -> bytes:
        """Generate a zip file containing all project files"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path, content in self.generate_project_files().items():
                zip_file.writestr(file_path, content)
        
        zip_buffer.seek(0)
        return zip_buffer.read()