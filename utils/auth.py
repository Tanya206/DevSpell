import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv
from pages.ChatHistory import chat_history_page
from pages.Home import home_page
from pages.NewProject import new_project_page
from utils.error_handler import handle_errors, DevSpellError
from utils.firestore_db import get_db
import uuid
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from firebase_admin import auth as firebase_auth

load_dotenv()

# Firebase initialization
@handle_errors
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv('FIREBASE_CONFIG_PATH'))
        firebase_admin.initialize_app(cred)

@handle_errors
def login_user(email, password, firestore_db):
    if not email or not password:
        raise DevSpellError("Email and password are required")

    try:
        # Firebase Authentication sign-in
        user = firebase_auth.get_user_by_email(email)  # Get user details by email
        if not user:
            raise DevSpellError("Invalid email or password")

        # Here we simulate Firebase Authentication. In production, use Firebase client-side SDK or a custom backend login.
        # You may need Firebase Auth service on client-side for real password validation.

        # Assuming successful password verification, store user in session
        st.session_state["user"] = user
        st.success("Login successful!")
        return user
    except firebase_auth.UserNotFoundError:
        raise DevSpellError("User not found")
    except firebase_auth.InvalidPasswordError:
        raise DevSpellError("Invalid password")
    except Exception as e:
        raise DevSpellError(f"Login failed: {str(e)}")

@handle_errors
def signup_user(email, password, firestore_db):
    if not email or not password:
        raise DevSpellError("Email and password are required")
    if len(password) < 6:
        raise DevSpellError("Password must be at least 6 characters long")

    try:
        # Check if the user already exists in Firestore
        existing_user = firestore_db.get_user_by_email(email)
        if existing_user:
            raise DevSpellError("Email already exists")

        # Create new user in Firebase Authentication
        user_record = auth.create_user(email=email, password=password)

        # User profile data to store in Firestore
        user_data = {
            'email': email,
            'name': '',  # Add name field if available in the UI
            'uid': user_record.uid,
            'created_at': datetime.now(),
            'last_login': datetime.now()
        }

        # Save user profile in Firestore
        firestore_db.save_user_profile(user_record.uid, user_data)

        # Return a user object to set in session state
        user = type('User', (), {
            'email': email,
            'uid': user_record.uid
        })

        return user
    except Exception as e:
        raise DevSpellError(f"Sign up failed: {str(e)}")

@handle_errors
def logout_user():
    # Clear the user from session state
    if "user" in st.session_state:
        del st.session_state["user"]
    switch_page("Login")

def display_navigation():
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Welcome, {st.session_state.user.email}")
    page = st.sidebar.radio("Go to", ["Home", "New Project", "Chat History"])
    
    if st.sidebar.button("Logout"):
        logout_user()
    
    if page == "Home":
        home_page()
    elif page == "New Project":
        new_project_page()
    elif page == "Chat History":
        chat_history_page()