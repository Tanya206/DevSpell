from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from backend.project_generator import EnhancedProjectGenerator
from utils.firestore_db import get_db
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent

# Load environment variables
load_dotenv()

# LLM1 Prompt Template (For project structure and requirements)
llm1_prompt_template = PromptTemplate(template="""
You are an expert prompt engineer focusing on creating clear, structured project requirements.
Given the following technical stack and requirements:

Project Name: {project_name}
Project Type: {project_type}
Frontend Framework: {frontend_option}
UI Library: {ui_library}
Backend Framework: {backend_option}
Database: {database_option}
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

Focus on creating a clear, actionable prompt that will guide the development process.
""", input_variables=["project_name", "project_type", "frontend_option", "ui_library", 
                     "backend_option", "database_option", "authentication", "features",
                     "description", "requirements"])

# LLM2 Prompt Template (For implementation)
llm2_prompt_template = PromptTemplate(template="""
You are a senior software architect tasked with generating a complete project implementation.

Project Requirements:
{prompt}

Technical Stack:
- Frontend: {frontend_option}
- UI Library: {ui_library}
- Backend: {backend_option}
- Database: {database_option}
- Authentication: {authentication}
- Additional Features: {features}

Based on the above, create a complete project implementation that:
1. Follows the specified technical stack
2. Implements all required features
3. Includes proper error handling and security measures
4. Is well-documented and maintainable

Include:
1. Complete project structure
2. Key implementation files
3. Configuration setup
4. Database schema
5. API endpoints
6. Deployment instructions

Ensure all code is production-ready and follows modern development standards.
""", input_variables=["prompt", "frontend_option", "ui_library", "backend_option", 
                     "database_option", "authentication", "features"])

def generate_initial_prompt(project_data, user_id):
    """Generate initial prompt focused only on project structure and requirements"""
    llm1 = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="mixtral-8x7b-32768")
    chain = LLMChain(prompt=llm1_prompt_template, llm=llm1)
    
    prompt = chain.run({
        "project_name": project_data["name"],
        "project_type": project_data["project_type"],
        "frontend_option": project_data["frontend"],
        "ui_library": project_data["ui_library"],
        "backend_option": project_data["backend"],
        "database_option": project_data["database"],
        "authentication": project_data["authentication"],
        "features": ", ".join(project_data["additional_features"]),
        "description": project_data["description"],
        "requirements": ", ".join(project_data["requirements"])
    })
    
    # Save to Firestore
    db = get_db()
    db.save_chat_history(user_id, {
        "user_message": "Initial prompt generation",
        "llm_response": prompt
    })
    
    return prompt

def generate_project_files(project_data, approved_prompt):
    """Generate the final project files using LLM2"""
    llm2 = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="mixtral-8x7b-32768")
    chain = LLMChain(prompt=llm2_prompt_template, llm=llm2)
    
    implementation_details = chain.run({
        "prompt": approved_prompt,
        "frontend_option": project_data["frontend"],
        "ui_library": project_data["ui_library"],
        "backend_option": project_data["backend"],
        "database_option": project_data["database"],
        "authentication": project_data["authentication"],
        "features": ", ".join(project_data["additional_features"])
    })
    
    # Generate project using the implementation details
    generator = EnhancedProjectGenerator()
    result = generator.generate_project({
        **project_data,
        "implementation": implementation_details
    })
    
    return result