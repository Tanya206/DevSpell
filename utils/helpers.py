# utils/helpers.py
import re

def validate_email(email):
    """Validates if the email format is correct."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def format_customization(customizations):
    """Formats customization details to make them more readable."""
    return customizations.strip().replace("\n", "; ")

def prepare_prompt(frontend, backend, database, customizations, uploaded_files, linked_resources):
    """Prepares a formatted prompt string from user inputs."""
    return f"Frontend: {frontend}, Backend: {backend}, Database: {database}, Customizations: {customizations}, Uploaded Files: {uploaded_files}, Linked Resources: {linked_resources}"


def format_project_requirements(project_data):
    """Formats project requirements into a structured dictionary."""
    return {
        "project_type": project_data["project_type"],
        "name": project_data["name"],
        "description": project_data["description"],
        "scale": project_data["scale"],
        "key_requirements": project_data["requirements"],
        "tech_stack": {
            "frontend": project_data["frontend"],
            "ui_library": project_data["ui_library"],
            "backend": project_data["backend"],
            "database": project_data["database"]
        }
    }

def validate_prompt(prompt):
    """Validates if the generated prompt contains all necessary components."""
    required_sections = [
        "Project Overview",
        "Technical Stack",
        "Architecture",
        "Features",
        "Implementation Plan"
    ]
    return all(section.lower() in prompt.lower() for section in required_sections)