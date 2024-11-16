import streamlit as st
from utils.github_integration import get_github_token, get_github_client
from utils.firestore_db import get_db
from streamlit_extras.switch_page_button import switch_page

# Must be first Streamlit command
st.set_page_config(page_title="GitHub Authentication", page_icon="🔮")

def handle_callback():
   """Handle GitHub OAuth callback."""
   
   # Verify user is logged in
   if "user" not in st.session_state:
       st.error("Please log in first")
       switch_page("Home")
       return

   # Get and validate query parameters
   try:
       code = st.query_params.get("code")
       state = st.query_params.get("state")
       
       if not code or not state:
           st.error("Missing required OAuth parameters")
           st.button("Return to Home", on_click=lambda: switch_page("Home"))
           return

       # Debug info (remove in production)
       st.write("Debug Information:")
       st.write("- Session State Keys:", list(st.session_state.keys()))
       st.write("- Received State:", state)
       st.write("- Stored State:", st.session_state.get('github_oauth_state'))

       # Validate state
       stored_state = st.session_state.get('github_oauth_state')
       if not stored_state or state != stored_state:
           st.error("State validation failed. Please try again.")
           st.button("Return to Home", on_click=lambda: switch_page("Home"))
           return

       # Exchange code for token
       token = get_github_token(code, state)
       if not token:
           st.error("Failed to retrieve GitHub token")
           st.button("Try Again", on_click=lambda: switch_page("Home"))
           return

       # Initialize GitHub client and get user info
       github_client = get_github_client(token)
       if not github_client:
           st.error("Failed to initialize GitHub client")
           return

       github_user = github_client.get_user()
       
       # Update session state
       st.session_state.github_token = token
       st.session_state.github_username = github_user.login
       
       # Update user profile in Firestore
       try:
           db = get_db()
           db.update_user(st.session_state.user.uid, {
               "github_username": github_user.login,
               "github_token": token,
               "github_connected": True
           })
       except Exception as e:
           st.warning(f"Failed to update user profile: {str(e)}")
           # Continue anyway since GitHub connection was successful

       # Clean up OAuth state
       if 'github_oauth_state' in st.session_state:
           del st.session_state.github_oauth_state

       # Show success message
       st.success(f"Successfully connected GitHub account: {github_user.login}")
       
       # Add some useful information
       st.write("You can now:")
       st.write("- Create new repositories")
       st.write("- Access your existing repositories")
       st.write("- Generate project structures")
       
       if st.button("Continue to App", type="primary"):
           switch_page("Home")

   except Exception as e:
       st.error(f"An error occurred during GitHub authentication: {str(e)}")
       st.button("Return to Home", on_click=lambda: switch_page("Home"))

def main():
   st.title("Connecting to GitHub")
   
   # Show a loading spinner while processing
   with st.spinner("Processing GitHub authentication..."):
       handle_callback()

if __name__ == "__main__":
   main()