from pathlib import Path
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import tempfile
import zipfile
import os

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
            "Static Website": {
                "structure": ["public", "assets", "css", "js", "images"],
                "files": {
                    "index.html": self._generate_static_html,
                    "css/style.css": self._generate_css,
                    "js/main.js": self._generate_js
                }
            },
            "React": {
                "structure": [
                    "src/components", "src/pages", "src/hooks", "src/context",
                    "src/assets", "src/styles", "src/utils", "src/services",
                    "public"
                ],
                "files": {
                    "src/App.jsx": self._generate_react_app,
                    "src/index.jsx": self._generate_react_index,
                    "vite.config.js": self._generate_vite_config,
                    "package.json": self._generate_react_package_json,
                    "tailwind.config.js": self._generate_tailwind_config,
                    "postcss.config.js": self._generate_postcss_config
                }
            },
            "Vue.js": {
                "structure": [
                    "src/components", "src/views", "src/router", "src/store",
                    "src/assets", "src/styles", "src/utils", "src/services",
                    "public"
                ],
                "files": {
                    "src/App.vue": self._generate_vue_app,
                    "src/main.js": self._generate_vue_main,
                    "vue.config.js": self._generate_vue_config,
                    "package.json": self._generate_vue_package_json
                }
            },
            "Next.js": {
                "structure": [
                    "pages", "components", "styles", "public", "lib",
                    "hooks", "context", "utils", "services"
                ],
                "files": {
                    "pages/_app.js": self._generate_nextjs_app,
                    "pages/index.js": self._generate_nextjs_index,
                    "next.config.js": self._generate_nextjs_config,
                    "package.json": self._generate_nextjs_package_json
                }
            }
        }

        self.backend_configs = {
            "Node.js/Express": {
                "structure": [
                    "src/routes", "src/controllers", "src/models",
                    "src/middleware", "src/services", "src/utils",
                    "src/config"
                ],
                "files": {
                    "src/app.js": self._generate_express_app,
                    "src/server.js": self._generate_express_server,
                    "package.json": self._generate_express_package_json
                }
            },
            "Django": {
                "structure": [
                    "project_name", "project_name/apps",
                    "project_name/static", "project_name/templates",
                    "project_name/media"
                ],
                "files": {
                    "manage.py": self._generate_django_manage,
                    "requirements.txt": self._generate_django_requirements,
                    "project_name/settings.py": self._generate_django_settings
                }
            },
            "FastAPI": {
                "structure": [
                    "app", "app/api", "app/core", "app/models",
                    "app/schemas", "app/services", "app/tests"
                ],
                "files": {
                    "app/main.py": self._generate_fastapi_main,
                    "requirements.txt": self._generate_fastapi_requirements,
                    "Dockerfile": self._generate_fastapi_dockerfile
                }
            }
        }

        self.database_configs = {
            "PostgreSQL": {
                "files": {
                    "migrations/init.sql": self._generate_postgres_init,
                    "src/config/database.js": self._generate_postgres_config
                }
            },
            "MongoDB": {
                "files": {
                    "src/config/database.js": self._generate_mongodb_config,
                    "src/models/schema.js": self._generate_mongodb_schema
                }
            },
            "MySQL": {
                "files": {
                    "migrations/init.sql": self._generate_mysql_init,
                    "src/config/database.js": self._generate_mysql_config
                }
            }
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
        gitignore = self._generate_gitignore(config)
        self._write_file(base_path / ".gitignore", gitignore)
        
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
        path.write_text(content)

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

