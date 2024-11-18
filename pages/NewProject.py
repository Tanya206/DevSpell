import os
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st
from utils.cognitive_verifier import CognitiveVerifier
from backend.project_generator import ProjectGenerator, ProjectConfig
from typing import Dict, Optional
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
import os
import json
from typing import Dict, List
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Epic(BaseModel):
    title: str = Field(description="Epic title")
    description: str = Field(description="Epic description")
    technical_components: List[str] = Field(description="Technical components involved")
    dependencies: Optional[List[str]] = Field(description="Dependencies on other epics", default=None)
    files: List[str] = Field(description="Files to be created or modified")
    expected_outcomes: List[str] = Field(description="Expected outcomes")
    constraints: Optional[List[str]] = Field(description="Technical requirements and constraints", default=None)

class ProjectEpics(BaseModel):
    epics: List[Epic]


class ProjectImplementer:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-70b-versatile"
        )

    def create_epic_generation_chain(self):
        """Create LCEL chain for generating project epics"""
        # Use Pydantic output parser for strict JSON structure
        pydantic_parser = PydanticOutputParser(pydantic_object=ProjectEpics)

        epic_creation_prompt = ChatPromptTemplate.from_template(
            "You are a senior technical product manager breaking down a project into implementable epics.\n"
            "Project Requirements:\n{prompt}\n\n"
            "Technical Stack:\n"
            "- Frontend: {frontend}\n"
            "- UI Library: {ui_library}\n"
            "- Backend: {backend}\n"
            "- Database: {database}\n"
            "- Authentication: {authentication}\n"
            "- Additional Features: {features}\n\n"
            "{format_instructions}\n\n"
            "Create a complete breakdown of the project into epics with detailed information."
        )

        return (
            RunnablePassthrough.assign(
                features=lambda x: ", ".join(x.get('additional_features', [])) if x.get('additional_features') else "",
                prompt=lambda x: f"""
                Project Name: {x.get('name', 'New Project')}
                Project Type: {x.get('project_type', '')}
                Description: {x.get('description', '')}
                Scale: {x.get('scale', '')}
                Key Requirements: {', '.join(x.get('requirements', []))}
                Deployment: {x.get('deployment', '')}
                """,
                frontend=lambda x: x.get('frontend', ''),
                ui_library=lambda x: x.get('ui_library', ''),
                backend=lambda x: x.get('backend', ''),
                database=lambda x: x.get('database', ''),
                authentication=lambda x: x.get('authentication', ''),
                format_instructions=lambda x: pydantic_parser.get_format_instructions()
            )
            | epic_creation_prompt
            | self.llm
            | pydantic_parser
        )
    def create_epics(self, project_data: dict):
        """Generate project epics and file structure"""
        st.write("Creating project epics...")

        #Generate Project Configurations
        project_config = ProjectConfig(project_data)
        project_generator = ProjectGenerator(project_config)        
        # Create chains
        epic_chain = self.create_epic_generation_chain()
        project_epics = epic_chain.invoke(project_data)

        project_files = project_generator.generate_project_files()
        enhanced_project_files = self._enhance_project_files(project_files, project_epics)   

        return {
            "epics": project_epics,
            "files": enhanced_project_files
        }     

    def _enhance_project_files(self, project_files: dict, project_epics: dict):
        """Enhance project files with epic-driven annotations"""
        for file_path, file_content in project_files.items():
            # Add epic-related comments or metadata
            enhanced_content = self._add_epic_metadata(file_content, project_epics)
            project_files[file_path] = enhanced_content
        
        return project_files
    
    def _add_epic_metadata(self, file_content: str, project_epics: ProjectEpics) -> str:
        """Add epic-related metadata to file content"""
        epic_annotation = "# Project Epics:\n"
        for epic in project_epics.epics:
            epic_annotation += f"# - {epic.title}: {epic.description}\n"
        
        return epic_annotation + "\n" + file_content
    

    def _process_file_structure(self, file_structure):
        """Process and implement file structure"""
        implementation_prompt = ChatPromptTemplate.from_template("""
        Implement file: {file_path}
        Details: {file_details}

        Provide complete, production-ready implementation following:
        1. Best practices
        2. Comprehensive error handling
        3. Detailed documentation
        4. Proper integration
        5. Necessary imports/configurations
        """)

        implemented_files = {}
        for file_path, details in file_structure.items():
            try:
                implementation_chain = (
                    RunnablePassthrough.assign(
                        file_details=lambda x: json.dumps(x, indent=2)
                    )
                    | implementation_prompt
                    | self.llm
                )
                
                implementation = implementation_chain.invoke({
                    "file_path": file_path,
                    **details
                })
                
                implemented_files[file_path] = {
                    "content": implementation.content,
                    "details": details
                }
            except Exception as e:
                st.error(f"Error implementing {file_path}: {e}")
        
        return implemented_files

def initialize_session_state():
    """Initialize session state variables"""
    initial_states = {
        "step": 1,
        "project_data": {},
        "recommendations": None,
        "generated_prompt": None,
        "approved_prompt": None
    }
    for key, value in initial_states.items():
        if key not in st.session_state:
            st.session_state[key] = value


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
    """Generate the final project using ProjectImplementer"""
    implementer = ProjectImplementer()
    project_details = implementer.create_epics(st.session_state.project_data)
    
    # Optional: Display project epics and files
    st.write("Project Epics:", project_details['epics'])

        # Create a ProjectGenerator to generate the zip file
    project_config = ProjectConfig(st.session_state.project_data)
    project_generator = ProjectGenerator(project_config)
    
    # Generate and provide download button for the zip file
    zip_content = project_generator.generate_zip_file()
    st.download_button(
        label="Download Project",
        data=zip_content,
        file_name=f"{st.session_state.project_data['name'].lower().replace(' ', '_')}.zip",
        mime="application/zip"
    )


    return project_details
    
    
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