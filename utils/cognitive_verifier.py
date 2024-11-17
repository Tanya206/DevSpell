from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os

class CognitiveVerifier:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-70b-versatile"
        )
        
        self.stack_recommendation_template = PromptTemplate(
            template="""
            As an expert software architect, analyze the following project requirements and recommend the most suitable technology stack.
            
            Project Type: {project_type}
            Project Description: {description}
            Key Requirements: {requirements}
            Scale Requirements: {scale}
            
            Please recommend:
            1. Frontend Framework and UI Library
            2. Backend Framework
            3. Database
            4. Additional Services (caching, messaging, etc.)
            5. Deployment Strategy
            
            For each recommendation, provide a brief justification.
        
            """,
            input_variables=["project_type", "description", "requirements", "scale"]
        )
        
        self.compatibility_check_template = PromptTemplate(
            template="""
            Analyze the compatibility of the following technology choices:
            
            Frontend: {frontend} with {ui_library}
            Backend: {backend}
            Database: {database}
            Authentication: {auth_method}
            
            Please identify:
            1. Any potential compatibility issues
            2. Performance implications
            3. Development complexity
            4. Recommended adjustments
            Also draw a architecture diagram.
            """,
            input_variables=["frontend", "ui_library", "backend", "database", "auth_method"]
        )
    
    def get_stack_recommendation(self, project_type, description, requirements, scale):
        chain = LLMChain(prompt=self.stack_recommendation_template, llm=self.llm)
        result = chain.run({
            "project_type": project_type,
            "description": description,
            "requirements": requirements,
            "scale": scale
        })
        return self._parse_recommendations(result)
    
    def verify_compatibility(self, frontend, ui_library, backend, database, auth_method):
        chain = LLMChain(prompt=self.compatibility_check_template, llm=self.llm)
        result = chain.run({
            "frontend": frontend,
            "ui_library": ui_library,
            "backend": backend,
            "database": database,
            "auth_method": auth_method
        })
        return self._parse_compatibility(result)
    
    def _parse_recommendations(self, result):
        # Implementation to parse LLM response into structured recommendations
        # This is a placeholder - you would implement proper parsing logic
        return {
            "frontend": {"framework": "React", "ui_library": "Material-UI"},
            "backend": "Node.js/Express",
            "database": "MongoDB",
            "additional_services": ["Redis", "RabbitMQ"],
            "deployment": "AWS ECS"
        }
    
    def _parse_compatibility(self, result):
        # Implementation to parse LLM response into structured compatibility analysis
        # This is a placeholder - you would implement proper parsing logic
        return {
            "compatible": True,
            "issues": [],
            "recommendations": []
        }
