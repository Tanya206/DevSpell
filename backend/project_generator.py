from pathlib import Path
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import tempfile
import zipfile
import os

import yaml

@dataclass
class ProjectConfig:
    name: str
    project_type: str
    description: str
    frontend: str
    ui_library: str = "None"  # Add default values
    backend: str = "None"
    database: str = "None"
    authentication: str = "None"
    features: List[str] = None
    requirements: List[str] = None
    deployment_platform: str = "None"
    static_site_generator: str = "None"
    css_technologies: List[str] = None
    js_technologies: List[str] = None
    cache_service: str = "None"
    cms: str = "None"

    def __post_init__(self):
        # Initialize empty lists if None
        if self.features is None:
            self.features = []
        if self.requirements is None:
            self.requirements = []
        if self.css_technologies is None:
            self.css_technologies = []
        if self.js_technologies is None:
            self.js_technologies = []
class ProjectGenerator:
    def __init__(self):
        self.template_configs = {
            "HTML/CSS/JS(Vanilla)": {
                "structure": ["public", "assets", "css", "js", "images"],
                "files": {
                    "index.html": self._generate_static_html,
                    "css/style.css": self._generate_css,
                    "js/main.js": self._generate_js
                }
            },
            # "React": {
            #     "structure": [
            #         "src/components", "src/pages", "src/hooks", "src/context",
            #         "src/assets", "src/styles", "src/utils", "src/services",
            #         "public"
            #     ],
            #     "files": {
            #         "src/App.jsx": self._generate_react_app,
            #         "src/index.jsx": self._generate_react_index,
            #         "vite.config.js": self._generate_vite_config,
            #         "package.json": self._generate_react_package_json,
            #         "tailwind.config.js": self._generate_tailwind_config,
            #         "postcss.config.js": self._generate_postcss_config
            #     }
            # },
            # "Vue.js": {
            #     "structure": [
            #         "src/components", "src/views", "src/router", "src/store",
            #         "src/assets", "src/styles", "src/utils", "src/services",
            #         "public"
            #     ],
            #     "files": {
            #         "src/App.vue": self._generate_vue_app,
            #         "src/main.js": self._generate_vue_main,
            #         "vue.config.js": self._generate_vue_config,
            #         "package.json": self._generate_vue_package_json
            #     }
            # },
            # "Next.js": {
            #     "structure": [
            #         "pages", "components", "styles", "public", "lib",
            #         "hooks", "context", "utils", "services"
            #     ],
            #     "files": {
            #         "pages/_app.js": self._generate_nextjs_app,
            #         "pages/index.js": self._generate_nextjs_index,
            #         "next.config.js": self._generate_nextjs_config,
            #         "package.json": self._generate_nextjs_package_json
            #     }
            # }
        }

        self.backend_configs = {
            # "Node.js/Express": {
            #     "structure": [
            #         "src/routes", "src/controllers", "src/models",
            #         "src/middleware", "src/services", "src/utils",
            #         "src/config"
            #     ],
            #     "files": {
            #         "src/app.js": self._generate_express_app,
            #         "src/server.js": self._generate_express_server,
            #         "package.json": self._generate_express_package_json
            #     }
            # },
            # "Django": {
            #     "structure": [
            #         "project_name", "project_name/apps",
            #         "project_name/static", "project_name/templates",
            #         "project_name/media"
            #     ],
            #     "files": {
            #         "manage.py": self._generate_django_manage,
            #         "requirements.txt": self._generate_django_requirements,
            #         "project_name/settings.py": self._generate_django_settings
            #     }
            # },
            # "FastAPI": {
            #     "structure": [
            #         "app", "app/api", "app/core", "app/models",
            #         "app/schemas", "app/services", "app/tests"
            #     ],
            #     "files": {
            #         "app/main.py": self._generate_fastapi_main,
            #         "requirements.txt": self._generate_fastapi_requirements,
            #         "Dockerfile": self._generate_fastapi_dockerfile
            #     }
            # }
        }

        self.database_configs = {
            # "PostgreSQL": {
            #     "files": {
            #         "migrations/init.sql": self._generate_postgres_init,
            #         "src/config/database.js": self._generate_postgres_config
            #     }
            # },
            # "MongoDB": {
            #     "files": {
            #         "src/config/database.js": self._generate_mongodb_config,
            #         "src/models/schema.js": self._generate_mongodb_schema
            #     }
            # },
            # "MySQL": {
            #     "files": {
            #         "migrations/init.sql": self._generate_mysql_init,
            #         "src/config/database.js": self._generate_mysql_config
            #     }
            # }
        }

    def generate_project(self, config: ProjectConfig, implementation_details: str) -> Optional[Dict]:
        """Generate project files based on configuration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            
            # Create basic project structure
            self._create_base_structure(base_path)
            
            # Generate frontend files
            self._generate_frontend_files(base_path, config)
            
            # Generate backend files
            if config.backend != "None":
                self._generate_backend_files(base_path, config)
            
            # Generate database files
            if config.database != "None":
                self._generate_database_files(base_path, config)
            
            # Generate configuration files
            self._generate_config_files(base_path, config)
            
            # Generate documentation
            self._generate_documentation(base_path, config)
            
            # Create deployment files
            self._generate_deployment_files(base_path, config)
            
            # Parse and generate implementation files
            self._generate_implementation_files(base_path, implementation_details)
            
            # Create ZIP archive
            return self._create_zip_archive(base_path)

    def _create_base_structure(self, base_path: Path):
        """Create common project structure"""
        common_dirs = ["docs", "tests", "scripts"]
        for dir_name in common_dirs:
            (base_path / dir_name).mkdir(parents=True, exist_ok=True)

    def _generate_frontend_files(self, base_path: Path, config: ProjectConfig):
        """Generate frontend-specific files"""
        print(config.frontend)
        if config.frontend in self.template_configs:
            template = self.template_configs[config.frontend]
            
            # Create directory structure
            for dir_name in template["structure"]:
                (base_path / dir_name).mkdir(parents=True, exist_ok=True)
            
            # Generate files
            for file_path, generator in template["files"].items():
                content = generator(config)
                self._write_file(base_path / file_path, content)

    def _generate_backend_files(self, base_path: Path, config: ProjectConfig):
        """Generate backend-specific files"""
        if config.backend in self.backend_configs:
            template = self.backend_configs[config.backend]
            
            # Create directory structure
            for dir_name in template["structure"]:
                (base_path / dir_name).mkdir(parents=True, exist_ok=True)
            
            # Generate files
            for file_path, generator in template["files"].items():
                content = generator(config)
                self._write_file(base_path / file_path, content)

    def _generate_database_files(self, base_path: Path, config: ProjectConfig):
        """Generate database-specific files"""
        if config.database in self.database_configs:
            template = self.database_configs[config.database]
            
            # Generate files
            for file_path, generator in template["files"].items():
                content = generator(config)
                self._write_file(base_path / file_path, content)

    def _generate_config_files(self, base_path: Path, config: ProjectConfig):
        """Generate configuration files"""
        # Generate environment files
        env_vars = self._generate_env_vars(config)
        self._write_file(base_path / ".env.example", env_vars)
        
        # Generate gitignore
        # gitignore = self._generate_gitignore(config)
        # self._write_file(base_path / ".gitignore", gitignore)
        
        # Generate package.json if needed
        if config.frontend in ["React", "Vue.js", "Next.js"] or config.backend == "Node.js/Express":
            package_json = self._generate_package_json(config)
            self._write_json(base_path / "package.json", package_json)

    def _generate_deployment_files(self, base_path: Path, config: ProjectConfig):
        """Generate deployment configuration files"""
        if config.deployment_platform == "Docker":
            dockerfile = self._generate_dockerfile(config)
            self._write_file(base_path / "Dockerfile", dockerfile)
            
            docker_compose = self._generate_docker_compose(config)
            self._write_file(base_path / "docker-compose.yml", docker_compose)
        
        elif config.deployment_platform == "Vercel":
            vercel_config = self._generate_vercel_config(config)
            self._write_json(base_path / "vercel.json", vercel_config)
        
        elif config.deployment_platform == "Netlify":
            netlify_config = self._generate_netlify_config(config)
            self._write_file(base_path / "netlify.toml", netlify_config)

    def _generate_documentation(self, base_path: Path, config: ProjectConfig):
        """Generate project documentation"""
        # Generate README.md
        readme = self._generate_readme(config)
        self._write_file(base_path / "README.md", readme)
        
        # Generate API documentation if needed
        if config.backend != "None":
            api_docs = self._generate_api_docs(config)
            self._write_file(base_path / "docs/api.md", api_docs)

    # File content generators
    def _generate_static_html(self, config: ProjectConfig) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div id="root"></div>
    <script src="js/main.js"></script>
</body>
</html>""".format(config.name)

    def _generate_react_app(self, config: ProjectConfig) -> str:
        return """import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/globals.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;"""

    # Add more generator methods for different file types...

    @staticmethod
    def _write_file(path: Path, content: str):
        """Helper method to write file content"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    @staticmethod
    def _write_json(path: Path, content: dict):
        """Helper method to write JSON content"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content, indent=2))

    def _create_zip_archive(self, base_path: Path) -> Dict:
        """Create ZIP archive of the generated project"""
        files = []
        zip_path = base_path / "project.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, filenames in os.walk(base_path):
                for filename in filenames:
                    if filename != "project.zip":
                        file_path = Path(root) / filename
                        arcname = file_path.relative_to(base_path)
                        zipf.write(file_path, arcname)
                        files.append({
                            "path": str(arcname),
                            "content": file_path.read_text()
                        })
        
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
        
        return {
            'zip_content': zip_content,
            'files': files
        }
    # Add these methods to the ProjectGenerator class

    def _generate_css(self, config: ProjectConfig) -> str:
        """Generate base CSS file"""
        if "Tailwind CSS" in config.css_technologies:
            return """@tailwind base;
    @tailwind components;
    @tailwind utilities;

    /* Custom styles */
    :root {
        --primary-color: #3b82f6;
        --secondary-color: #1e40af;
    }"""
        else:
            return """/* Base styles */
    :root {
        --primary-color: #3b82f6;
        --secondary-color: #1e40af;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
        color: #333;
    }

    .container {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .container {
            padding: 0 0.5rem;
        }
    }"""

    def _generate_js(self, config: ProjectConfig) -> str:
        """Generate main JavaScript file"""
        return """// Main JavaScript file
    document.addEventListener('DOMContentLoaded', () => {
        console.log('Application initialized');
    });

    // Add your custom JavaScript code here
    """

    def _generate_react_index(self, config: ProjectConfig) -> str:
        """Generate React index file"""
        return """import React from 'react';
    import ReactDOM from 'react-dom/client';
    import App from './App';
    import './styles/globals.css';

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    );"""

    def _generate_vite_config(self, config: ProjectConfig) -> str:
        """Generate Vite configuration"""
        return """import { defineConfig } from 'vite';
    import react from '@vitejs/plugin-react';

    export default defineConfig({
        plugins: [react()],
        server: {
            port: 3000
        },
        build: {
            outDir: 'dist',
            sourcemap: true
        }
    });"""

    def _generate_react_package_json(self, config: ProjectConfig) -> str:
        """Generate package.json for React projects"""
        return """{
        "name": "%s",
        "private": true,
        "version": "0.1.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.0"
        },
        "devDependencies": {
            "@types/react": "^18.0.27",
            "@types/react-dom": "^18.0.10",
            "@vitejs/plugin-react": "^3.1.0",
            "vite": "^4.1.0"
        }
    }""" % config.name

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

    # In the ProjectGenerator class

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


    def _generate_env_vars(self, config: ProjectConfig) -> str:
        """Generate environment variables template"""
        env_vars = [
            "# Environment Variables",
            "NODE_ENV=development",
            "",
            "# Server Configuration",
            "PORT=3000",
            "HOST=localhost",
            ""
        ]
        
        if config.database != "None":
            env_vars.extend([
                "# Database Configuration",
                "DB_HOST=localhost",
                "DB_PORT=5432",
                "DB_NAME=your_database",
                "DB_USER=your_username",
                "DB_PASSWORD=your_password",
                ""
            ])
        
        if config.authentication != "None":
            env_vars.extend([
                "# Authentication",
                "JWT_SECRET=your_jwt_secret",
                "JWT_EXPIRATION=24h",
                ""
            ])
        
        return "\n".join(env_vars)

    def _generate_readme(self, config: ProjectConfig) -> str:
        """Generate README.md file"""
        return f"""# {config.name}

        {config.description}

        ## Technology Stack

        - Frontend: {config.frontend}
        - UI Library: {config.ui_library}
        - Backend: {config.backend}
        - Database: {config.database}
        - Authentication: {config.authentication}

        ## Getting Started

        1. Clone the repository
        2. Install dependencies: `npm install` or `yarn`
        3. Copy `.env.example` to `.env` and configure environment variables
        4. Start development server: `npm run dev` or `yarn dev`

        ## Features

        {chr(10).join([f"- {feature}" for feature in config.features])}

        ## Project Structure

        ```
        src/
        ├── components/    # Reusable UI components
        ├── pages/         # Page components/routes
        ├── styles/        # Global styles and theme
        ├── utils/         # Utility functions
        └── services/      # API services and data fetching
        ```

        ## Contributing

        1. Fork the repository
        2. Create a new branch
        3. Make your changes
        4. Submit a pull request

        ## License

        MIT
        """

    def _generate_nextjs_package_json(self, project_name: str) -> Dict:
        return {
            "name": project_name,
            "version": "1.0.0",
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "^13.0.0",
                "react": "^18.0.0",
                "react-dom": "^18.0.0"
            }
        }

    def _generate_node_express_package_json(self, project_name: str) -> Dict:
        return {
            "name": project_name,
            "version": "1.0.0",
            "main": "index.js",
            "scripts": {
                "start": "node index.js",
                "dev": "nodemon index.js"
            },
            "dependencies": {
                "express": "^4.18.0"
            },
            "devDependencies": {
                "nodemon": "^2.0.0"
            }
        }
    def _generate_express_app(self, config: ProjectConfig) -> str:
        """Generate Express app.js file"""
        return """const express = require('express');
    const cors = require('cors');
    const helmet = require('helmet');
    const compression = require('compression');
    const routes = require('./routes');

    const app = express();

    // Middleware
    app.use(helmet());
    app.use(cors());
    app.use(compression());
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));

    // Routes
    app.use('/api', routes);

    // Error handling middleware
    app.use((err, req, res, next) => {
        console.error(err.stack);
        res.status(500).send('Something broke!');
    });

    module.exports = app;"""

    def _generate_express_server(self, config: ProjectConfig) -> str:
        """Generate Express server.js file"""
        return """const app = require('./app');
    require('dotenv').config();

    const PORT = process.env.PORT || 3000;
    const HOST = process.env.HOST || 'localhost';

    app.listen(PORT, () => {
        console.log(`Server running at http://${HOST}:${PORT}`);
    });"""

    def _generate_express_package_json(self, config: ProjectConfig) -> str:
        """Generate package.json for Express projects"""
        return """{
        "name": "%s",
        "version": "1.0.0",
        "description": "Express.js backend for %s",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js",
            "test": "jest"
        },
        "dependencies": {
            "compression": "^1.7.4",
            "cors": "^2.8.5",
            "dotenv": "^16.0.3",
            "express": "^4.18.2",
            "helmet": "^6.0.1"
        },
        "devDependencies": {
            "jest": "^29.4.3",
            "nodemon": "^2.0.20"
        }
    }""" % (config.name, config.name)

    def _generate_express_server(self, config: ProjectConfig) -> str:
        """Generate Express server.js file"""
        return """const app = require('./app');
    require('dotenv').config();

    const PORT = process.env.PORT || 3000;
    const HOST = process.env.HOST || 'localhost';

    app.listen(PORT, () => {
        console.log(`Server running at http://${HOST}:${PORT}`);
    });"""

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

    def _generate_implementation_files(self, base_path: Path, implementation_details: str) -> None:
        """Generate implementation-specific files based on provided details"""
        try:
            details = json.loads(implementation_details)
            for file_info in details:
                file_path = base_path / file_info['path']
                content = file_info['content']
                self._write_file(file_path, content)
        except json.JSONDecodeError:
            print("Invalid implementation details format")
        except KeyError:
            print("Missing required implementation details")

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

    def _get_auth_docs(self, config: ProjectConfig) -> str:
        """Generate authentication documentation based on config"""
        if config.authentication == "JWT":
            return """Authentication is handled via JWT tokens.
    Include the token in the Authorization header:
    `Authorization: Bearer <token>`"""
        elif config.authentication == "OAuth":
            return """Authentication is handled via OAuth 2.0.
    Follow the standard OAuth flow to obtain access tokens."""
        else:
            return "No authentication required for public endpoints."