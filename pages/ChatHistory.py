import streamlit as st
from utils.firestore_db import get_db
from datetime import datetime

def chat_history_page():
    st.title("Chat History")
    
    if "user" not in st.session_state:
        st.error("Please login first")
        return
        
    # Get user ID from session state
    user_id = st.session_state["user"].uid
    db = get_db()
    
    # Retrieve chat history
    chat_history = db.retrieve_chat_history(user_id)
    
    if chat_history:
        for chat in chat_history:
            with st.expander(f"Chat from {chat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                st.write("**Your Input:**")
                st.write(chat['user_message'])
                st.write("**AI Response:**")
                st.write(chat['llm_response'])
    else:
        st.info("No chat history available yet. Try creating a new project!")

if __name__ == "__main__":
    chat_history_page()