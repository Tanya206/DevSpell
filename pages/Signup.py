# Signup.py

import streamlit as st
from utils.auth import signup_user
from streamlit_extras.switch_page_button import switch_page
from utils.firestore_db import get_db
from utils.github_integration import create_github_oauth_url

def app():
    st.title("Sign Up")

    signup_email = st.text_input("Email")
    signup_password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        try:
            db = get_db()
            user = signup_user(signup_email, signup_password, db)  # Pass `db` to `signup_user`
            if user:
                # Save user in session state
                st.session_state["user"] = user
                st.success("Account created successfully!")
                switch_page("Login")
        except Exception as e:
            st.error(f"Sign up failed: {str(e)}")

    if st.button("Already have an account? Login here"):
        switch_page("app")

    st.subheader("GitHub Integration")
    st.write("Link your GitHub account to save projects to your repositories")
    
    if "github_username" not in st.session_state:
        if st.button("Link GitHub Account"):
            auth_url = create_github_oauth_url()
            st.markdown(f"[Authorize GitHub]({auth_url})")
    else:
        st.success(f"GitHub account linked: {st.session_state.github_username}")
        if st.button("Unlink GitHub Account"):
            del st.session_state.github_username
            del st.session_state.github_token
            st.rerun()


if __name__ == "__main__":
    app()
