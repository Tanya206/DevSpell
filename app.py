import os
from dotenv import load_dotenv
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from utils.auth import init_firebase, login_user, logout_user
from streamlit_extras.switch_page_button import switch_page
from utils.firestore_db import get_db
from pages.Home import home_page
from pages.NewProject import new_project_page
from pages.ChatHistory import chat_history_page
from utils.error_handler import handle_errors
from utils.auth import init_firebase, login_user, logout_user, display_navigation
from utils.github_integration import create_github_oauth_url

# Must be the first Streamlit command
st.set_page_config(page_title="DevSpell", page_icon="🔮", layout="wide")

def initialize_session_state():
    """Initialize session state variables"""
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "github_oauth_state" not in st.session_state:
        st.session_state.github_oauth_state = None
    if "github_token" not in st.session_state:
        st.session_state.github_token = None

@handle_errors
def main():
    # Initialize session state
    initialize_session_state()
    
    # Load environment variables
    load_dotenv()

    # Initialize Firebase
    init_firebase()

    # Set up Firebase SDK if not already initialized
    FIREBASE_CONFIG_PATH = os.getenv('FIREBASE_CONFIG_PATH')
    if not len(firebase_admin._apps):
        cred = credentials.Certificate(FIREBASE_CONFIG_PATH)
        firebase_admin.initialize_app(cred, {
            'projectId': os.getenv('FIREBASE_PROJECT_ID'),
        })

    # Main app flow
    if not st.session_state.user:
        render_login_ui()
    else:
        render_main_app()

def render_main_app():
    """Render the main application interface"""
    display_navigation()
    
    # Handle GitHub connection status
    if "github_token" not in st.session_state and st.session_state.user:
        st.sidebar.markdown("---")
        st.sidebar.subheader("GitHub Integration")
        github_url = create_github_oauth_url()
        st.sidebar.markdown(f'''
            <a href="{github_url}" target="_self">
                <button style="background-color:#2ea44f;color:white;padding:8px 16px;border:none;border-radius:4px;cursor:pointer">
                    Connect GitHub Account
                </button>
            </a>
        ''', unsafe_allow_html=True)

def display_navigation():
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Welcome, {st.session_state.user.email}")
    page = st.sidebar.radio("Go to", ["Home", "New Project", "Chat History", "About", "Contact"])

    if st.sidebar.button("Logout"):
        handle_logout()

    # Route to appropriate page
    if page == "Home":
        home_page()
    elif page == "New Project":
        new_project_page()
    elif page == "Chat History":
        chat_history_page()
    elif page == "About":
        switch_page("About")
    elif page == "Contact":
        switch_page("Contact")

def handle_logout():
    """Handle user logout"""
    logout_user()
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()
    st.rerun()

@handle_errors
def render_login_ui():
    st.title("Welcome to DevSpell 🔮")
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("Login")
        login_email = st.text_input("Email", key="login_email", autocomplete="email")
        login_password = st.text_input("Password", type="password", key="login_password", autocomplete="current-password")
        
        if st.button("Login", key="login_button"):
            try:
                user = login_user(login_email, login_password, get_db())
                if user:
                    st.session_state.user = user
                    st.session_state.authentication_status = True
                    st.success("Login successful!")
                    st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

    with col2:
        st.header("Sign Up")
        if st.button("Don't have an account? Sign up here"):
            switch_page("Signup")

if __name__ == "__main__":
    main()