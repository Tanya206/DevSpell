    def _generate_tailwind_config(self, config: ProjectConfig) -> str:
        """Generate Tailwind configuration"""
        return """/** @type {import('tailwindcss').Config} */
    module.exports = {
        content: [
            "./src/**/*.{js,jsx,ts,tsx}",
        ],
        theme: {
            extend: {},
        },
        plugins: [],
    }"""

    def _generate_postcss_config(self, config: ProjectConfig) -> str:
        """Generate PostCSS configuration"""
        return """module.exports = {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        },
    }"""

    def _generate_vue_app(self, config: ProjectConfig) -> str:
        """Generate Vue.js App.vue file"""
        return """<template>
        <div id="app">
            <router-view></router-view>
        </div>
    </template>

    <script>
    export default {
        name: 'App'
    }
    </script>

    <style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
    </style>"""

    def _generate_vue_main(self, config: ProjectConfig) -> str:
        """Generate Vue.js main.js file"""
        return """import { createApp } from 'vue'
    import App from './App.vue'
    import router from './router'
    import store from './store'

    const app = createApp(App)
    app.use(router)
    app.use(store)
    app.mount('#app')"""

    def _generate_vue_config(self, config: ProjectConfig) -> str:
        """Generate Vue.js configuration"""
        return """module.exports = {
        publicPath: '/',
        lintOnSave: false,
        productionSourceMap: false
    }"""

    def _generate_nextjs_app(self, config: ProjectConfig) -> str:
        """Generate Next.js _app.js file"""
        return """import '../styles/globals.css'

    function MyApp({ Component, pageProps }) {
        return <Component {...pageProps} />
    }

    export default MyApp"""

    def _generate_nextjs_index(self, config: ProjectConfig) -> str:
        """Generate Next.js index page"""
        return """export default function Home() {
        return (
            <div>
                <h1>Welcome to {config.name}</h1>
            </div>
        )
    }"""

    def _generate_nextjs_config(self, config: ProjectConfig) -> str:
        """Generate Next.js configuration"""
        return """/** @type {import('next').NextConfig} */
    module.exports = {
        reactStrictMode: true,
        swcMinify: true,
    }"""


    def _generate_vue_package_json(self, project_name: str) -> Dict:
        """
        Generates a package.json file for a Vue.js project.

        Args:
            project_name (str): Name of the Vue.js project.

        Returns:
            Dict: A dictionary representing the contents of package.json.
        """
        return {
            "name": project_name,
            "version": "1.0.0",
            "description": f"{project_name} - Vue.js Project",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "serve": "vite preview"
            },
            "dependencies": {
                "vue": "^3.2.0"
            },
            "devDependencies": {
                "vite": "^4.0.0"
            }
        }

    def _generate_django_manage(self, config: ProjectConfig) -> str:
        """Generate Django manage.py file"""
        return """#!/usr/bin/env python
    import os
    import sys

    def main():
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
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
        main()"""

    def _generate_django_requirements(self, config: ProjectConfig) -> str:
        """Generate Django requirements.txt file"""
        return """Django>=4.2.0
    djangorestframework>=3.14.0
    django-cors-headers>=4.0.0
    python-dotenv>=1.0.0
    psycopg2-binary>=2.9.6
    gunicorn>=20.1.0"""

    def _generate_django_settings(self, config: ProjectConfig) -> str:
        """Generate Django settings.py file"""
        return """import os
    from pathlib import Path
    from dotenv import load_dotenv

    load_dotenv()

    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'

    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'corsheaders',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'project_name.urls'
    WSGI_APPLICATION = 'project_name.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    STATIC_URL = 'static/'
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'"""

    def _generate_fastapi_main(self, config: ProjectConfig) -> str:
        """Generate FastAPI main.py file"""
        return """from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="FastAPI Backend",
        description="API Documentation",
        version="1.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {"message": "Welcome to the API"}"""

    def _generate_fastapi_requirements(self, config: ProjectConfig) -> str:
        """Generate FastAPI requirements.txt file"""
        return """fastapi>=0.95.0
    uvicorn>=0.21.0
    python-dotenv>=1.0.0
    sqlalchemy>=2.0.0
    pydantic>=1.10.0
    alembic>=1.10.0"""

    def _generate_fastapi_dockerfile(self, config: ProjectConfig) -> str:
        """Generate FastAPI Dockerfile"""
        return """FROM python:3.9-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]"""


    def _generate_postgres_init(self, config: ProjectConfig) -> str:
        """Generate initial PostgreSQL migration file"""
        return """-- Initial database schema
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- Add your table definitions here
    """

    def _generate_postgres_config(self, config: ProjectConfig) -> str:
        """Generate PostgreSQL configuration file"""
        return """const { Pool } = require('pg');
    require('dotenv').config();

    const pool = new Pool({
        user: process.env.DB_USER,
        host: process.env.DB_HOST,
        database: process.env.DB_NAME,
        password: process.env.DB_PASSWORD,
        port: process.env.DB_PORT,
    });

    module.exports = pool;
    """

    def _generate_mongodb_config(self, config: ProjectConfig) -> str:
        """Generate MongoDB configuration file"""
        return """const mongoose = require('mongoose');
    require('dotenv').config();

    const connectDB = async () => {
        try {
            await mongoose.connect(process.env.MONGODB_URI, {
                useNewUrlParser: true,
                useUnifiedTopology: true,
            });
            console.log('MongoDB connected successfully');
        } catch (error) {
            console.error('MongoDB connection error:', error);
            process.exit(1);
        }
    };

    module.exports = connectDB;
    """

    def _generate_mongodb_schema(self, config: ProjectConfig) -> str:
        """Generate MongoDB schema file"""
        return """const mongoose = require('mongoose');

    const userSchema = new mongoose.Schema({
        username: {
            type: String,
            required: true,
            unique: true,
        },
        email: {
            type: String,
            required: true,
            unique: true,
        },
        createdAt: {
            type: Date,
            default: Date.now,
        },
    });

    module.exports = mongoose.model('User', userSchema);
    """

    def _generate_mysql_init(self, config: ProjectConfig) -> str:
        """Generate initial MySQL migration file"""
        return """-- Initial database schema
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    -- Add your table definitions here
    """

    def _generate_mysql_config(self, config: ProjectConfig) -> str:
        """Generate MySQL configuration file"""
        return """const mysql = require('mysql2');
    require('dotenv').config();

    const pool = mysql.createPool({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME,
        waitForConnections: true,
        connectionLimit: 10,
        queueLimit: 0
    });

    module.exports = pool.promise();
    """

def _generate_docker_compose(self, config: ProjectConfig) -> str:
        """Generate docker-compose.yml file"""
        services = {
            "app": {
                "build": ".",
                "ports": ["3000:3000"],
                "environment": [
                    "NODE_ENV=development"
                ],
                "volumes": ["./:/app"],
                "depends_on": []
            }
        }
        
        if config.database == "PostgreSQL":
            services["postgres"] = {
                "image": "postgres:latest",
                "environment": [
                    "POSTGRES_USER=postgres",
                    "POSTGRES_PASSWORD=postgres",
                    "POSTGRES_DB=app"
                ],
                "ports": ["5432:5432"]
            }
            services["app"]["depends_on"].append("postgres")
        
        elif config.database == "MongoDB":
            services["mongodb"] = {
                "image": "mongo:latest",
                "ports": ["27017:27017"]
            }
            services["app"]["depends_on"].append("mongodb")
        
        return f"""version: '3.8'

    services:
    {yaml.dump(services, default_flow_style=False)}"""

    def _generate_vercel_config(self, config: ProjectConfig) -> dict:
        """Generate Vercel configuration"""
        return {
            "version": 2,
            "builds": [
                {
                    "src": "package.json",
                    "use": "@vercel/node"
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "/"
                }
            ]
        }

    def _generate_netlify_config(self, config: ProjectConfig) -> str:
        """Generate Netlify configuration"""
        return """[build]
    command = "npm run build"
    publish = "dist"

    [dev]
    command = "npm run dev"
    port = 3000

    [[redirects]]
    from = "/*"
    to = "/index.html"
    status = 200
    """

    def _generate_api_docs(self, config: ProjectConfig) -> str:
        """Generate API documentation"""
        return f"""# API Documentation

    ## Overview
    This document provides documentation for the {config.name} API.

    ## Authentication
    {self._get_auth_docs(config)}

    ## Endpoints

    ### Users
    - `GET /api/users`
    - List all users
    - Requires authentication

    - `POST /api/users`
    - Create a new user
    - Public endpoint

    ### Authentication
    - `POST /api/auth/login`
    - User login
    - Returns JWT token

    - `POST /api/auth/register`
    - User registration
    - Creates new user account

    ## Error Handling
    All endpoints follow standard HTTP status codes and return JSON responses.

    ## Rate Limiting
    API requests are limited to 100 requests per minute per IP address.
    """
