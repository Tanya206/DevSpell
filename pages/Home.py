import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils.github_integration import link_github_account
from utils.firestore_db import get_db
import uuid
from urllib.parse import urlencode

def home_page():
    # Check if user is logged in
    if "user" not in st.session_state:
        st.warning("Please log in first")
        if st.button("Go to Signup"):  # Add a button to direct users
            switch_page("signup")
        return

    st.title("DevSpell 🔮")
    st.write(f"Welcome {st.session_state.user.email} to your project development hub!")

    # Rest of your code remains the same...
    # GitHub Account Section
    st.subheader("GitHub Integration")
    link_github_account()

    # Project Actions   
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Create New Project", use_container_width=True):
            switch_page("NewProject")

    with col2:
        if st.button("📜 View Chat History", use_container_width=True):
            switch_page("ChatHistory")

    # Recent Projects
    st.subheader("Recent Projects")
    db = get_db()
    recent_projects = db.get_user_projects(st.session_state.user.uid, limit=5)
    
    if recent_projects:
        for project in recent_projects:
            with st.expander(f"📁 {project.get('name', 'Untitled Project')}"):
                st.write(f"Type: {project.get('project_type', 'N/A')}")
                st.write(f"Status: {project.get('status', 'N/A')}")
                if project.get('github_url'):
                    st.markdown(f"[View on GitHub]({project['github_url']})")
    else:
        st.info("No projects yet. Click 'Create New Project' to get started!")

if __name__ == "__main__":
    home_page()