import firebase_admin
from firebase_admin import firestore
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
from .error_handler import FirestoreError
load_dotenv()

class FirestoreDB:
    def __init__(self, db_client=None):
        self.db = db_client or firestore.client()

    def save_chat_history(self, user_id, chat_data):
        """
        Save chat history for a user
        
        Args:
            user_id (str): The user's unique identifier
            chat_data (dict): Dictionary containing chat data
                Expected keys: 
                - user_message (str): The user's message
                - llm_response (str): The LLM's response
                
        Raises:
            FirestoreError: If there's an error saving to Firestore
            ValueError: If the input parameters are invalid
        """
        if not user_id or not isinstance(chat_data, dict):
            raise ValueError("Invalid user_id or chat_data")

        chat_doc = {
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'chat_id': str(uuid.uuid4()),
            'user_message': chat_data.get('user_message', ''),
            'llm_response': chat_data.get('llm_response', ''),
            'metadata': {
                'created_at': datetime.utcnow().isoformat(),
                'type': 'project_generation'
            }
        }

        try:
            doc_ref = self.db.collection('chat_history').document()
            doc_ref.set(chat_doc)
            return doc_ref.id
        except Exception as e:
            raise FirestoreError(f"Failed to save chat history: {str(e)}")

    def save_project(self, user_id, project_data):
        """
        Save generated project data
        
        Raises:
            FirestoreError: If there's an error saving to Firestore
            ValueError: If the input parameters are invalid
        """
        if not user_id or not isinstance(project_data, dict):
            raise ValueError("Invalid user_id or project_data")

        project_doc = {
            'user_id': user_id,
            'project_id': str(uuid.uuid4()),
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            **project_data
        }

        try:
            doc_ref = self.db.collection('projects').document(project_doc['project_id'])
            doc_ref.set(project_doc)
            return project_doc['project_id']
        except Exception as e:
            raise FirestoreError(f"Failed to save project: {str(e)}")

    def get_user_projects(self, user_id, limit=None):
        """
        Retrieve user's projects
        
        Raises:
            FirestoreError: If there's an error retrieving from Firestore
        """
        try:
            query = (self.db.collection('projects')
                    .where("user_id", "==", user_id)
                    .order_by('created_at', direction=firestore.Query.DESCENDING))
            
            if limit:
                query = query.limit(limit)
            
            projects = query.stream()
            return [project.to_dict() for project in projects]
        except Exception as e:
            raise FirestoreError(f"Failed to retrieve user projects: {str(e)}")

    def retrieve_chat_history(self, user_id):
        """Retrieve chat history for a user"""
        chats = (self.db.collection('chat_history')
                .where("user_id", "==", user_id)
                .order_by('timestamp', direction=firestore.Query.DESCENDING)
                .stream())
        
        return [chat.to_dict() for chat in chats]

    def get_user_projects(self, user_id, limit=None):
        """Retrieve user's projects with optional limit"""
        query = (self.db.collection('projects')
                .where("user_id", "==", user_id)
                .order_by('created_at', direction=firestore.Query.DESCENDING))
        
        if limit:
            query = query.limit(limit)
        
        projects = query.stream()
        return [project.to_dict() for project in projects]

    def get_user_by_email(self, email):
        """Get user profile by email"""
        users_ref = self.db.collection('user_profiles').where("email", "==", email)
        docs = users_ref.stream()
        user_record = None
        for doc in docs:
            user_record = doc.to_dict()
            user_record['uid'] = doc.id
            break
        return user_record
    

    def update_user(self, user_id, update_data):
        """Update user profile information"""
        try:
            doc_ref = self.db.collection('user_profiles').document(user_id)
            doc_ref.update({
                **update_data,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as e:
            raise FirestoreError(f"Failed to update user: {str(e)}")
    
def get_db():
    return FirestoreDB(firestore.client())