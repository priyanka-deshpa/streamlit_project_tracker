import streamlit as st

def init_page_config():
    st.set_page_config(
        page_title="Project Activity Tracker",
        page_icon="📊",
        layout="wide"
    )
    
    # Load custom CSS
    with open('src/static/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Add custom CSS classes to elements
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)