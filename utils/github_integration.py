from github import Github
import os
from dotenv import load_dotenv
import streamlit as st
from urllib.parse import urlencode
import requests
import uuid
from utils.firestore_db import get_db

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_ORG_TOKEN = os.getenv("GITHUB_ORG_TOKEN")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")

def create_github_oauth_url():
    """Create GitHub OAuth URL with a secure state parameter."""
    # Initialize state if it doesn't exist
    if 'github_oauth_state' not in st.session_state:
        st.session_state.github_oauth_state = str(uuid.uuid4())
    
    # Debug log (remove in production)
    print(f"Creating OAuth URL with state: {st.session_state.github_oauth_state}")
    
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "repo user",
        "state": st.session_state.github_oauth_state
    }
    return f"https://github.com/login/oauth/authorize?{urlencode(params)}"

def get_github_token(code, state):
    """Exchange code for access token and verify state."""
    stored_state = st.session_state.get('github_oauth_state')
    
    # Debug logs (remove in production)
    print(f"Stored state: {stored_state}")
    print(f"Received state: {state}")
    
    if not stored_state or state != stored_state:
        print("State mismatch!")  # Debug log
        return None
    
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI
        },
        headers={"Accept": "application/json"}
    )
    
    if response.ok:
        return response.json().get("access_token")
    return None

def get_github_client(token=None):
    """Return a GitHub client, authenticated with a user token or organization token."""
    try:
        if token:
            g = Github(token)
            # Verify connection
            g.get_user().login
            return g
        return Github(GITHUB_ORG_TOKEN)
    except Exception as e:
        st.error(f"GitHub authentication failed: {str(e)}")
        if "github_token" in st.session_state:
            del st.session_state.github_token
        return None

def link_github_account():
    """UI for linking GitHub account with button to initiate OAuth process."""
    if "github_username" not in st.session_state:
        github_url = create_github_oauth_url()
        st.markdown(f'''
            <a href="{github_url}" target="_self">
                <button style="background-color:#2ea44f;color:white;padding:8px 16px;border:none;border-radius:4px;cursor:pointer">
                    Link GitHub Account
                </button>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.success(f"GitHub account linked: {st.session_state.github_username}")
        if st.button("Unlink GitHub Account"):
            del st.session_state.github_username
            del st.session_state.github_token
            db = get_db()
            db.update_user(st.session_state.user_id, {
                "github_username": None,
                "github_token": None
            })
            st.rerun()
