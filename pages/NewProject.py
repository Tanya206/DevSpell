import os
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st
from utils.cognitive_verifier import CognitiveVerifier
from backend.project_generator import ProjectGenerator, ProjectConfig
from typing import Dict
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import json
from typing import Dict, List


epic_creation_prompt = PromptTemplate(
    template="""
    You are a senior technical product manager tasked with breaking down a project into implementable epics.

    Project Requirements:
    {prompt}

    Technical Stack:
    - Frontend: {frontend}
    - UI Library: {ui_library}
    - Backend: {backend}
    - Database: {database}
    - Authentication: {authentication}
    - Additional Features: {features}

    Create a complete breakdown of the project into epics. For each epic, include:
    1. Epic title
    2. Description
    3. Technical components involved
    4. Dependencies on other epics
    5. Files that need to be created or modified
    6. Expected outcomes
    7. Technical requirements and constraints
    Ensure epics are ordered by dependencies (independent epics first).
    """,
    input_variables=["prompt", "frontend", "ui_library", "backend", 
                    "database", "authentication", "features"]
)

file_planning_prompt = PromptTemplate(
    template="""
    You are a senior software developer tasked with writing code for each epic provided to you.

    Project Context:
    {project_context}

    Technical Stack:
    - Frontend: {frontend}
    - UI Library: {ui_library}
    - Backend: {backend}
    - Database: {database}
    - Authentication: {authentication}
    - Additional Features: {features}

    Epics to Consider:
    {epics}

    Create a complete file structure for the project that:
    1. Consolidates all file requirements from all epics
    2. Eliminates redundancy (each file should appear only once)
    3. Provides comprehensive details for each file
    4. Maintains clear relationships between files
    5. Follows best practices for the chosen tech stack

    For each file, provide:
    1. File path (following proper project structure)
    2. Detailed description of the file's purpose
    3. Key components/functions to be implemented
    4. Dependencies and imports
    5. Integration points with other files
    6. Configuration requirements
    7. Technical constraints and considerations

    Format the response as a JSON object with file paths as keys and detailed descriptions as values.
    Do not return anything other than the JSON object. Make sure each file is included only once.
    """,
    input_variables=["project_context", "frontend", "ui_library", "backend", 
                    "database", "authentication", "features", "epics"]
)

class ProjectImplementer:
    def __init__(self):
        self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), 
                            model="llama-3.1-70b-versatile")
        self.epic_creation_chain = LLMChain(prompt=epic_creation_prompt, 
                                            llm=self.llm)
        self.file_planning_chain = LLMChain(prompt=file_planning_prompt, 
                                            llm=self.llm)
        # self.epic_implementation_chain = LLMChain(prompt=epic_implementation_prompt, 
        #                                         llm=self.llm)
        self.implemented_files: Dict[str, dict] = {}

    def create_epics(self, project_data: dict) -> List[dict]:
        """Generate project epics"""
        st.write("Creating project epics...")
        epics = self.epic_creation_chain.run({
            "prompt": st.session_state.approved_prompt,
            "frontend": project_data["frontend"],
            "ui_library": project_data["ui_library"],
            "backend": project_data["backend"],
            "database": project_data["database"],
            "authentication": project_data["authentication"],
            "features": ", ".join(project_data.get("additional_features", []))
        })
        st.write("Planning file structure...")
        file_structure = self.file_planning_chain.run({
            "project_context": st.session_state.approved_prompt,
            "frontend": project_data["frontend"],
            "ui_library": project_data["ui_library"],
            "backend": project_data["backend"],
            "database": project_data["database"],
            "authentication": project_data["authentication"],
            "features": ", ".join(project_data.get("additional_features", [])),
            "epics": epics
        })
        implemented_files = process_file_structure((file_structure))
        print(implemented_files)
        return implemented_files

    # def format_previous_files(self) -> str:
    #     """Format previously implemented files for context"""
    #     if not self.implemented_files:
    #         return "No files implemented yet."
        
    #     formatted_files = []
    #     for file_path, details in self.implemented_files.items():
    #         formatted_files.append(f"""
    #         File: {file_path}
    #         Purpose: {details.get('purpose', 'N/A')}
    #         Key Components: {details.get('key_components', 'N/A')}
    #         Integration Points: {details.get('integration_points', 'N/A')}
    #         """)
    #     return "\n".join(formatted_files)

    # def implement_file(self, file_path: str, file_details: dict, project_data: dict) -> dict:
    #     """Implement a single file"""
    #     st.write(f"Implementing file: {file_path}")
    #     implementation_json = self.epic_implementation_chain.run({
    #         "project_context": st.session_state.approved_prompt,
    #         "frontend": project_data["frontend"],
    #         "ui_library": project_data["ui_library"],
    #         "backend": project_data["backend"],
    #         "database": project_data["database"],
    #         "authentication": project_data["authentication"],
    #         "features": ", ".join(project_data.get("additional_features", [])),
    #         "file_details": json.dumps({"path": file_path, **file_details}, indent=2),
    #         "previous_files": self.format_previous_files()
    #     })
        
    #     implementation = json.loads(implementation_json)
    #     self.implemented_files[file_path] = implementation
    #     return implementation

    # def implement_project(self, project_data: dict) -> Dict[str, dict]:
    #     """Implement the complete project"""
    #     # Step 1: Create epics
    #     file_structure = self.create_epics(project_data)
        
    #     # Step 2: Plan file structure
    #     # file_structure = self.plan_file_structure(StrOutputParser(epics), project_data)
        
    #     # Step 3: Implement each file
    #     all_files = {}
        
    #     dependency_groups = self.group_files_by_dependencies(file_structure)
        
    #     # Implement files in dependency order
    #     for group in dependency_groups:
    #         for file_path in group:
    #             implementation = self.implement_file(
    #                 file_path, 
    #                 file_structure[file_path], 
    #                 project_data
    #             )
    #             all_files[file_path] = implementation
        
    #     return all_files

    # def group_files_by_dependencies(self, file_structure: Dict[str, dict]) -> List[List[str]]:
    #     """Group files by their dependencies for ordered implementation"""
    #     # Create dependency graph
    #     dependency_graph = {}
    #     for file_path, details in file_structure.items():
    #         dependencies = details.get('dependencies', [])
    #         dependency_graph[file_path] = dependencies
        
    #     # Implement topological sort
    #     grouped_files = []
    #     implemented = set()
        
    #     while len(implemented) < len(file_structure):
    #         current_group = []
    #         for file_path, deps in dependency_graph.items():
    #             if file_path not in implemented and all(d in implemented for d in deps):
    #                 current_group.append(file_path)
            
    #         for file_path in current_group:
    #             implemented.add(file_path)
            
    #         grouped_files.append(current_group)
        
    #     return grouped_files

from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import json
from typing import Dict, Set, List
from collections import defaultdict
import networkx as nx

def process_file_structure(json_structure: list):
    """
    Process a JSON file structure and generate implementations using LLM.
    
    Args:
        json_structure (str): JSON string containing file structure
            Format: {
                "file_path": {
                    "description": str,
                    "dependencies": List[str],
                    "purpose": str,
                    "components": List[str],
                    ...
                }
            }
    """
    from langchain_groq import ChatGroq
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    import os
    import json
    from typing import Dict, Set, List
    from collections import defaultdict
    import networkx as nx

    class FileImplementer:
        def __init__(self):
            self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), 
                              model="llama-3.1-70b-versatile")
            self.implemented_files: Dict[str, dict] = {}
            self.implementation_chain = self._create_implementation_chain()
            
        def _create_implementation_chain(self) -> LLMChain:
            """Create the LLM chain for file implementation"""
            implementation_prompt = PromptTemplate(
                template=""" 
                You are a senior developer tasked with implementing a specific file in a software project.

                File to Implement:
                Path: {file_path}

                File Details:
                {file_details}

                Context from Previously Implemented Files:
                {implemented_context}

                Requirements:
                1. Create complete, production-ready implementation
                2. Follow best practices for the file type and technology
                3. Include comprehensive error handling
                4. Add detailed documentation and comments
                5. Ensure proper integration with dependent files
                6. Include necessary imports and configurations
                7. Add appropriate tests if needed

                Provide the complete implementation following all requirements.
                Format the response as a JSON object with the following structure:
                {
                    "content": "actual file content",
                    "imports": ["list of required imports"],
                    "dependencies": ["list of file dependencies"],
                    "integration_points": ["description of integration points"],
                    "tests_required": ["list of tests needed"]
                }
                """,
                input_variables=["file_path", "file_details", "implemented_context"]
            )
            # Ensuring the model responds in JSON format using structured output
            return LLMChain(prompt=implementation_prompt, llm=self.llm).with_structured_output(
                {"content": "", "imports": [], "dependencies": [], "integration_points": [], "tests_required": []}, 
                method="json_mode"
            )

        def _get_implemented_context(self, current_file: str) -> str:
            """Get context from previously implemented files"""
            if not self.implemented_files:
                return "No files implemented yet."
            
            context_parts = []
            for file_path, details in self.implemented_files.items():
                if file_path != current_file:  # Skip current file
                    context_parts.append(f"""
                    File: {file_path}
                    Content Summary: {details.get('content', '')[:200]}...
                    Imports: {', '.join(details.get('imports', []))} 
                    Integration Points: {', '.join(details.get('integration_points', []))} 
                    """)
            return "\n".join(context_parts)

        def implement_file(self, file_path: str, file_details: dict) -> dict:
            """Implement a single file using the LLM"""
            try:
                print(f"Implementing file: {file_path}")
                
                implementation_json = self.implementation_chain.run({
                    "file_path": file_path,
                    "file_details": json.dumps(file_details, indent=2),
                    "implemented_context": self._get_implemented_context(file_path)
                })
                
                # Parse the structured JSON output
                implementation = json.loads(implementation_json)
                self.implemented_files[file_path] = implementation
                return implementation
                
            except Exception as e:
                print(f"Error implementing file {file_path}: {str(e)}")
                return {
                    "content": f"// Error implementing file: {str(e)}",
                    "imports": [],
                    "dependencies": [],
                    "integration_points": [],
                    "tests_required": []
                }

        def create_dependency_graph(self, file_structure: Dict[str, dict]) -> nx.DiGraph:
            """Create a directed graph of file dependencies"""
            G = nx.DiGraph()
            
            # Add all files as nodes
            for file_path in file_structure:
                G.add_node(file_path)
            
            # Add dependency edges
            for file_path, details in file_structure.items():
                for dep in details.get('dependencies', []):
                    if dep in file_structure:
                        G.add_edge(dep, file_path)
            
            return G

        def get_implementation_order(self, file_structure: Dict[str, dict]) -> List[str]:
            """Determine the order of file implementation based on dependencies"""
            G = self.create_dependency_graph(file_structure)
            
            try:
                # Try to get topological sort
                return list(nx.topological_sort(G))
            except nx.NetworkXUnfeasible:
                print("Warning: Circular dependencies detected. Using approximate ordering.")
                # Fall back to approximate ordering
                return list(file_structure.keys())

        def implement_files_recursively(self, file_structure: Dict[str, dict]) -> Dict[str, dict]:
            """
            Recursively implement all files in the correct dependency order
            """
            # Get implementation order
            implementation_order = self.get_implementation_order(file_structure)
            
            # Implement files in order
            for file_path in implementation_order:
                if file_path not in self.implemented_files:
                    self.implement_file(file_path, file_structure[file_path])
            
            return self.implemented_files

    def process_structure(json_structure: str) -> Dict[str, dict]:
        """Main function to process the file structure and generate implementations"""
        try:
            # Parse JSON structure
            file_structure = json.loads(json_structure)
            
            # Create implementer and process files
            implementer = FileImplementer()
            implemented_files = implementer.implement_files_recursively(file_structure)
            
            print("Implementation completed successfully!")
            return implemented_files
            
        except json.JSONDecodeError:
            print("Error: Invalid JSON structure provided")
            return {}
        except Exception as e:
            print(f"Error processing file structure: {str(e)}")
            return {}

    return process_structure(json_structure)


def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "project_data" not in st.session_state:
        st.session_state.project_data = {}
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "generated_prompt" not in st.session_state:
        st.session_state.generated_prompt = None
    if "approved_prompt" not in st.session_state:
        st.session_state.approved_prompt = None

def collect_project_requirements():
    """Step 1: Collect project requirements"""
    st.subheader("Step 1: Project Requirements")
    
    with st.form("project_requirements"):
        project_name = st.text_input("Project Name", 
                                   value=st.session_state.project_data.get("name", ""),
                                   help="Enter a descriptive name for your project")
        
        project_type = st.selectbox(
            "Project Type",
            [
                "Static Website",
                "Landing Page",
                "Portfolio Site",
                "Blog",
                "Web Application",
                "Mobile App",
                "Desktop Application",
                "API Service",
                "E-commerce Site",
                "Data Pipeline",
                "IoT Application",
                "Machine Learning",
                "Blockchain",
                "Dashboard",
                "Documentation Site",
                "Social Media Platform",
                "Content Management System",
                "Other"
            ],
            index=0 if "project_type" not in st.session_state.project_data 
            else list(st.session_state.project_data.keys()).index(st.session_state.project_data.get("project_type"))
        )
        
        project_description = st.text_area(
            "Project Description",
            value=st.session_state.project_data.get("description", ""),
            help="Provide a detailed description of your project",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            scale_requirements = st.select_slider(
                "Expected Scale",
                options=["Minimal", "Prototype", "Small", "Medium", "Large", "Enterprise"],
                value=st.session_state.project_data.get("scale", "Small")
            )
        
        with col2:
            deployment_preference = st.selectbox(
                "Preferred Deployment",
                ["Static Hosting", "GitHub Pages", "Netlify", "Vercel",
                 "Cloud (AWS)", "Cloud (Azure)", "Cloud (GCP)", 
                 "On-Premise", "Hybrid", "Not Sure"],
                index=0 if "deployment" not in st.session_state.project_data 
                else ["Static Hosting", "GitHub Pages", "Netlify", "Vercel",
                      "Cloud (AWS)", "Cloud (Azure)", "Cloud (GCP)", 
                      "On-Premise", "Hybrid", "Not Sure"]
                .index(st.session_state.project_data.get("deployment"))
            )
        
        key_requirements = st.multiselect(
            "Key Requirements",
            [
                "Static Content",
                "Responsive Design",
                "Contact Form",
                "Image Gallery",
                "Blog Posts",
                "SEO Optimization",
                "User Authentication",
                "User Profiles",
                "Real-time Updates",
                "File Storage",
                "Search Functionality",
                "Comments/Reviews",
                "Payment Processing",
                "Analytics",
                "Multi-language Support",
                "Email Notifications",
                "Mobile Responsiveness",
                "Offline Support",
                "Third-party Integrations",
                "API Documentation",
                "Admin Dashboard",
                "Content Management",
                "Social Media Integration",
                "Data Visualization"
            ],
            default=st.session_state.project_data.get("requirements", [])
        )
        
        submit_requirements = st.form_submit_button("Analyze Requirements")
        
        if submit_requirements:
            if not project_name or not project_description or not key_requirements:
                st.error("Please fill in all required fields")
                return False
            
            st.session_state.project_data.update({
                "name": project_name,
                "project_type": project_type,
                "description": project_description,
                "scale": scale_requirements,
                "deployment": deployment_preference,
                "requirements": key_requirements
            })
            
            return True
    
    return False

# Rest of your existing select_technology_stack() function remains the same
def select_technology_stack():
    """Step 2: Technology stack selection based on AI recommendations"""
    st.subheader("Step 2: Technology Stack Selection")
    
    verifier = CognitiveVerifier()
    
    with st.spinner("Analyzing requirements for optimal tech stack..."):
        recommendations = verifier.get_stack_recommendation(
            st.session_state.project_data["project_type"],
            st.session_state.project_data["description"],
            st.session_state.project_data["requirements"],
            st.session_state.project_data["scale"]
        )
        st.session_state.recommendations = recommendations
    
    with st.form("tech_stack_selection"):
        st.write("AI-Recommended Technology Stack:")
        
        # Basic Technologies Section
        st.subheader("Basic Technologies")
        basic_col1, basic_col2 = st.columns(2)
        
        with basic_col1:
            html_version = st.selectbox(
                "HTML Version",
                ["None", "HTML5", "HTML4", "XHTML"],
                index=1
            )
            
            css_choice = st.multiselect(
                "CSS Technologies",
                ["None", "CSS3", "SASS/SCSS", "Less", "PostCSS"],
                default=["CSS3"]
            )
        
        with basic_col2:
            js_choice = st.multiselect(
                "JavaScript Features",
                ["None", "Vanilla JS", "ES6+", "TypeScript", "jQuery"],
                default=["ES6+"]
            )
        
        # Frontend Section
        st.subheader("Frontend Technologies")
        col1, col2 = st.columns(2)
        
        with col1:
            frontend_option = st.selectbox(
                "Frontend Framework/Library",
                [
                    "None",  # Added None option
                    "HTML/CSS/JS(Vanilla)",  # Basic option
                    "React",
                    "Vue.js",
                    "Angular",
                    "Next.js",
                    "Nuxt.js",
                    "Svelte",
                    "SvelteKit",
                    "Flutter",
                    "React Native",
                    "jQuery",  # Added for simpler projects
                    "Bootstrap (Framework)",  # Added for simpler projects
                    "Other"
                ],
                index=0 if recommendations["frontend"]["framework"] == "None" else None
            )
            
            ui_library = st.selectbox(
                "UI Framework/Library",
                [
                    "None",  # Added None option
                    "Custom CSS",  # Basic option
                    "Bootstrap",
                    "Tailwind CSS",
                    "Material-UI",
                    "Chakra UI",
                    "Ant Design",
                    "Semantic UI",
                    "Bulma",  # Added more options
                    "Foundation",
                    "Other"
                ],
                index=0 if recommendations["frontend"]["ui_library"] == "None" else None
            )
            
            # New: Static Site Generator selection
            static_site_generator = st.selectbox(
                "Static Site Generator",
                [
                    "None",
                    "Jekyll",
                    "Hugo",
                    "Gatsby",
                    "11ty",
                    "Astro",
                    "VuePress",
                    "Other"
                ],
                index=0
            )
        
        # Backend Section
        st.subheader("Backend Technologies")
        col3, col4 = st.columns(2)
        
        with col3:
            backend_option = st.selectbox(
                "Backend Framework/Technology",
                [
                    "None",  # Added None option
                    "Static Files",  # Basic option
                    "PHP",  # Basic option
                    "Node.js/Express",
                    "Django",
                    "Flask",  # Added
                    "FastAPI",
                    "Spring Boot",
                    "Laravel",
                    "Ruby on Rails",
                    ".NET Core",
                    "Deno",  # Added
                    "Other"
                ],
                index=0 if recommendations["backend"] == "None" else None
            )
            
            database_option = st.selectbox(
                "Database",
                [
                    "None",  # Added None option
                    "Local Storage",  # Basic option
                    "SQLite",  # Basic option
                    "PostgreSQL",
                    "MongoDB",
                    "MySQL",
                    "Firebase",
                    "Redis",
                    "ElasticSearch",
                    "DynamoDB",
                    "Supabase",  # Added
                    "Other"
                ],
                index=0 if recommendations["database"] == "None" else None
            )
        
        # Additional Services Section
        st.subheader("Additional Services (Optional)")
        col5, col6 = st.columns(2)
        
        with col5:
            cache_service = st.selectbox(
                "Caching Solution",
                ["None", "Browser Cache", "Redis", "Memcached", "CDN", "Other"],
                index=0
            )
            
            cms_option = st.selectbox(
                "Content Management",
                ["None", "Markdown Files", "Headless CMS", "WordPress", "Strapi", "Other"],
                index=0
            )
        
        with col6:
            authentication = st.selectbox(
                "Authentication",
                ["None", "Local Auth", "OAuth", "JWT", "Firebase Auth", "Auth0", "Other"],
                index=0
            )
            
            deployment_platform = st.selectbox(
                "Deployment Platform",
                [
                    "None",
                    "GitHub Pages",
                    "Netlify",
                    "Vercel",
                    "Heroku",
                    "AWS",
                    "Digital Ocean",
                    "Azure",
                    "GCP",
                    "Other"
                ],
                index=0
            )
        
        # Project Features
        st.subheader("Additional Features")
        features = st.multiselect(
            "Select Additional Features",
            [
                "SEO Optimization",
                "Analytics Integration",
                "Social Media Integration",
                "Newsletter Integration",
                "Contact Form",
                "Image Optimization",
                "PWA Support",
                "Internationalization",
                "Dark Mode",
                "RSS Feed",
                "Sitemap",
                "Print Stylesheet"
            ]
        )
        
        submit_stack = st.form_submit_button("Verify Stack Compatibility")
        
        if submit_stack:
            with st.spinner("Verifying technology stack compatibility..."):
                compatibility = verifier.verify_compatibility(
                    frontend_option,
                    ui_library,
                    backend_option,
                    database_option,
                    authentication
                )
                
                if compatibility["compatible"]:
                    st.session_state.project_data.update({
                        "html_version": html_version,
                        "css_technologies": css_choice,
                        "js_technologies": js_choice,
                        "frontend": frontend_option,
                        "ui_library": ui_library,
                        "static_site_generator": static_site_generator,
                        "backend": backend_option,
                        "database": database_option,
                        "cache_service": cache_service,
                        "cms": cms_option,
                        "authentication": authentication,
                        "deployment_platform": deployment_platform,
                        "additional_features": features
                    })
                    return True
                else:
                    st.error("⚠️ Stack Compatibility Issues Detected:")
                    for issue in compatibility["issues"]:
                        st.warning(f"- {issue}")
                    st.info("Recommendations:")
                    for rec in compatibility["recommendations"]:
                        st.write(f"- {rec}")
                    return False
    
    return False

def review_generated_prompt():
    """Step 3: Generate and review initial prompt"""
    st.subheader("Step 3: Review Generated Prompt")
    
    if st.session_state.generated_prompt is None:
        with st.spinner("Generating initial prompt..."):
            # Updated to pass project_data as a single argument
            initial_prompt = generate_initial_prompt(st.session_state.project_data)
            st.session_state.generated_prompt = initial_prompt
    
    st.write("Please review the generated prompt below:")
    
    prompt_text = st.text_area(
        "Generated Prompt",
        value=st.session_state.generated_prompt,
        height=400
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Regenerate Prompt"):
            st.session_state.generated_prompt = None
            st.rerun()
    
    with col2:
        if st.button("Edit Prompt"):
            st.session_state.generated_prompt = prompt_text
    
    with col3:
        if st.button("Approve Prompt"):
            st.session_state.approved_prompt = prompt_text
            return True
    
    return False

def generate_initial_prompt(project_data: Dict) -> str:
    """Generate initial prompt based on project requirements"""
    prompt_template = PromptTemplate(
        template="""
        You are an expert prompt engineer focusing on creating clear, structured project requirements.
        Given the following technical stack and requirements:

        Project Name: {project_name}
        Project Type: {project_type}
        Frontend Framework: {frontend}
        UI Library: {ui_library}
        Backend Framework: {backend}
        Database: {database}
        Authentication: {authentication}
        Additional Features: {features}

        Project Description:
        {description}

        Key Requirements:
        {requirements}

        Generate a comprehensive project prompt that includes:
        1. Project Overview and Goals
        2. Detailed Technical Requirements
        3. Core Features and Functionality
        4. Project Structure Overview
        5. Development Guidelines
        6. Architecture Diagram

        Focus on creating a clear, actionable prompt that will guide the development process.
        """,
        input_variables=["project_name", "project_type", "frontend", "ui_library", 
                        "backend", "database", "authentication", "features",
                        "description", "requirements"]
    )
    
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-70b-versatile")
    chain = LLMChain(prompt=prompt_template, llm=llm)
    
    return chain.run({
        "project_name": project_data["name"],
        "project_type": project_data["project_type"],
        "frontend": project_data["frontend"],
        "ui_library": project_data["ui_library"],
        "backend": project_data["backend"],
        "database": project_data["database"],
        "authentication": project_data["authentication"],
        "features": ", ".join(project_data.get("additional_features", [])),
        "description": project_data["description"],
        "requirements": ", ".join(project_data["requirements"])
    })

def generate_final_project():
    """Generate the final project files using three-step LLM process"""

    implementer = ProjectImplementer()
    implemented_files = implementer.create_epics(st.session_state.project_data)
    return implemented_files
    

    # Main execution
    

    # # Create project configuration
    # config = ProjectConfig(
    #     name=st.session_state.project_data["name"],
    #     project_type=st.session_state.project_data["project_type"],
    #     description=st.session_state.project_data["description"],
    #     frontend=st.session_state.project_data["frontend"],
    #     ui_library=st.session_state.project_data.get("ui_library", "None"),
    #     backend=st.session_state.project_data.get("backend", "None"),
    #     database=st.session_state.project_data.get("database", "None"),
    #     authentication=st.session_state.project_data.get("authentication", "None"),
    #     features=st.session_state.project_data.get("additional_features", []),
    #     requirements=st.session_state.project_data.get("requirements", []),
    #     deployment_platform=st.session_state.project_data.get("deployment_platform", "None"),
    #     static_site_generator=st.session_state.project_data.get("static_site_generator", "None"),
    #     css_technologies=st.session_state.project_data.get("css_technologies", []),
    #     js_technologies=st.session_state.project_data.get("js_technologies", []),
    #     cache_service=st.session_state.project_data.get("cache_service", "None"),
    #     cms=st.session_state.project_data.get("cms", "None")
    # )

    # # Prepare files for ProjectGenerator
    # files_for_generator = []
    # for file_path, details in implemented_files.items():
    #     files_for_generator.append({
    #         "path": file_path,
    #         "content": details["content"],
    #         "purpose": details.get("purpose", ""),
    #         "key_components": details.get("key_components", []),
    #         "integration_points": details.get("integration_points", [])
    #     })

    # implementation_details = {
    #     "files": files_for_generator
    # }
    
    # generator = ProjectGenerator()
    # result = generator.generate_project(config, json.dumps(implementation_details, indent=4))
    
    # if result:
    #     with st.expander("Project Structure"):
    #         for file_info in result['files']:
    #             st.text(file_info['path'])
    #             if st.checkbox(f"View {file_info['path']}", key=file_info['path']):
    #                 st.code(file_info['content'])
        
    #     st.download_button(
    #         "Download Project",
    #         result['zip_content'],
    #         "project.zip",
    #         mime="application/zip"
    #     )
    # # Main execution
    # implementer = ProjectImplementer()
    # implemented_files = implementer.implement_project(st.session_state.project_data)

    # Create project configuration
    # config = ProjectConfig(
    #     name=st.session_state.project_data["name"],
    #     project_type=st.session_state.project_data["project_type"],
    #     description=st.session_state.project_data["description"],
    #     frontend=st.session_state.project_data["frontend"],
    #     ui_library=st.session_state.project_data.get("ui_library", "None"),
    #     backend=st.session_state.project_data.get("backend", "None"),
    #     database=st.session_state.project_data.get("database", "None"),
    #     authentication=st.session_state.project_data.get("authentication", "None"),
    #     features=st.session_state.project_data.get("additional_features", []),
    #     requirements=st.session_state.project_data.get("requirements", []),
    #     deployment_platform=st.session_state.project_data.get("deployment_platform", "None"),
    #     static_site_generator=st.session_state.project_data.get("static_site_generator", "None"),
    #     css_technologies=st.session_state.project_data.get("css_technologies", []),
    #     js_technologies=st.session_state.project_data.get("js_technologies", []),
    #     cache_service=st.session_state.project_data.get("cache_service", "None"),
    #     cms=st.session_state.project_data.get("cms", "None")
    # )

    # Prepare files for ProjectGenerator
    # files_for_generator = []
    # for file_path, details in implemented_files.items():
    #     files_for_generator.append({
    #         "path": file_path,
    #         "content": details["content"],
    #         "purpose": details.get("purpose", ""),
    #         "key_components": details.get("key_components", []),
    #         "integration_points": details.get("integration_points", [])
    #     })

    # implementation_details = {
    #     "files": files_for_generator
    # }
    
    # generator = ProjectGenerator()
    # result = generator.generate_project(config, json.dumps(implementation_details, indent=4))
    
    # if result:
    #     with st.expander("Project Structure"):
    #         for file_info in result['files']:
    #             st.text(file_info['path'])
    #             if st.checkbox(f"View {file_info['path']}", key=file_info['path']):
    #                 st.code(file_info['content'])
        
    #     st.download_button(
    #         "Download Project",
    #         result['zip_content'],
    #         "project.zip",
    #         mime="application/zip"
    #     )
def new_project_page():
    """Main function to handle the new project page"""
    st.title("🪄 Intelligent Project Generator")
    
    initialize_session_state()
    
    progress = st.progress(0)
    
    if st.session_state.step == 1:
        progress.progress(25)
        if collect_project_requirements():
            st.session_state.step = 2
            st.rerun()
    
    elif st.session_state.step == 2:
        progress.progress(50)
        if select_technology_stack():
            st.session_state.step = 3
            st.rerun()
        
        if st.button("Back to Requirements"):
            st.session_state.step = 1
            st.rerun()
    
    elif st.session_state.step == 3:
        progress.progress(75)
        if review_generated_prompt():
            st.session_state.step = 4
            st.rerun()
        
        if st.button("Back to Tech Stack"):
            st.session_state.step = 2
            st.rerun()
    
    elif st.session_state.step == 4:
        progress.progress(100)
        generate_final_project()
        
        if st.button("Back to Prompt Review"):
            st.session_state.step = 3
            st.rerun()

if __name__ == "__main__":
    new_project_page()