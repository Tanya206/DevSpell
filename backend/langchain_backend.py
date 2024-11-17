from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from backend.project_generator import generate_project
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
llm3_prompt_template=PromptTemplate(template="""
You are working in a software development agency and a project manager and software architect approach you telling you that you're assigned to work on a new project.
You are working on an app called {project_name} and you need to create a detailed development plan so that developers can start developing the app.
The description of the project is {llm2_result}
                                    
Before we go into the coding part, your job is to split the development process of creating this app into smaller epics.
Now, based on the project details provided, think epic by epic and create the entire development plan for new feature. Start from the project setup and specify each epic until the moment when the entire app should be fully working
""", input_variables=["project_name","result"])
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
2. Implementation files
3. Configuration setup
4. Database schema
5. API endpoints
6. Deployment instructions

Ensure all code is production-ready and follows modern development standards.
""", input_variables=["prompt", "frontend_option", "ui_library", "backend_option", 
                     "database_option", "authentication", "features"])

def generate_initial_prompt(project_data, user_id):
    """Generate initial prompt focused only on project structure and requirements"""
    llm1 = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-70b-versatile")
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
    """Generate project files epic by epic, with each epic handled by a separate LLM"""
    
    # Step 1: Generate epics
    epics = generate_epics(project_data, approved_prompt)
    previous_files_info = []  # To maintain context of all previously created files
    
    final_output = {}
    
    # Step 2: Iterate through each epic
    for idx, epic in enumerate(epics.split("\n")):  # Assuming epics are returned as newline-separated
        if not epic.strip():  # Skip empty lines
            continue
        
        # Create a new LLM for this epic
        llm_for_epic = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-70b-versatile")
        chain = LLMChain(prompt=PromptTemplate(template=f"""
        You are assigned to work on the epic: "{epic}". 
        Below is the description of all previously created files:

        {previous_files_info}

        Based on the epic details, generate:
        1. Complete implementation files for this epic.
        2. Any necessary configurations, APIs, or data schemas.
        3. A brief description of the files you generated.

        Focus on modularity, error handling, and adherence to project standards.
        """, input_variables=["epic", "previous_files_info"]), llm=llm_for_epic)
        
        # Generate implementation for the current epic
        epic_output = chain.run({"epic": epic, "previous_files_info": "\n".join(previous_files_info)})
        
        # Parse the result to separate files and description
        # Assuming the result is structured with a "FILES" and "DESCRIPTION" section
        files_section = epic_output.split("FILES:")[1].split("DESCRIPTION:")[0].strip()
        description_section = epic_output.split("DESCRIPTION:")[1].strip()
        
        # Update previous files info with the new description
        previous_files_info.append(description_section)
        
        # Save files and descriptions
        final_output[f"Epic_{idx+1}"] = {
            "files": files_section,
            "description": description_section
        }
        print(final_output)
    generator = generate_project()
    result = generator(
        **project_data,
        "implementation": final_output
    )
    return result


def generate_epics(project_data, approved_prompt):
    """Generate a list of development epics using LLM3"""
    llm3 = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-70b-versatile")
    chain = LLMChain(prompt=llm3_prompt_template, llm=llm3)
    
    epics = chain.run({
        "project_name": project_data["name"],
        "result": approved_prompt
    })
    
    # Save epics to Firestore
    db = get_db()
    db.save_chat_history(project_data["user_id"], {
        "user_message": "Epic generation",
        "llm_response": epics
    })
    print(epics)
    return epics
