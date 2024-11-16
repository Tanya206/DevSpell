# error_handler.py
import streamlit as st
from functools import wraps
from firebase_admin import exceptions as firebase_exceptions
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DevSpellError(Exception):
    """Base exception class for DevSpell"""
    pass

class FirestoreError(DevSpellError):
    """Exception class for Firestore-related errors"""
    pass

class DocumentProcessingError(DevSpellError):
    """Exception class for document processing errors"""
    pass

class LLMError(DevSpellError):
    """Exception class for LLM-related errors"""
    pass

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except firebase_exceptions.FirebaseError as e:
            error_message = str(e)
            logger.error(f"Firebase Error in {func.__name__}: {error_message}")
            st.error(f"Authentication Error: {error_message}")
            return None
        except FirestoreError as e:
            error_message = str(e)
            logger.error(f"Firestore Error in {func.__name__}: {error_message}")
            st.error(f"Database Error: {error_message}")
            return None
        except DocumentProcessingError as e:
            error_message = str(e)
            logger.error(f"Document Processing Error in {func.__name__}: {error_message}")
            st.error(f"Document Processing Error: {error_message}")
            return None
        except LLMError as e:
            error_message = str(e)
            logger.error(f"LLM Error in {func.__name__}: {error_message}")
            st.error(f"AI Processing Error: {error_message}")
            return None
        except DevSpellError as e:
            error_message = str(e)
            logger.error(f"Application Error in {func.__name__}: {error_message}")
            st.error(f"Application Error: {error_message}")
            return None
        except Exception as e:
            error_message = str(e)
            logger.error(f"Unexpected Error in {func.__name__}: {error_message}")
            st.error("An unexpected error occurred. Please try again.")
            return None
    return wrapper