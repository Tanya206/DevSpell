import streamlit as st

def about_page():
    st.title("About DevSpell")
    st.write("""
        DevSpell is a prompt-driven application that automates software project development.
        Using advanced language models, DevSpell generates project blueprints, code, and documentation
        based on user specifications, making development faster and more accessible.
    """)

if __name__ == "__main__":
    about_page()
