import streamlit as st
from src.config import init_page_config
from src.storage import init_storage
from src.views.project_view import render_project_list, render_project_form
from src.views.issue_view import render_issue_list, render_issue_form
from src.storage import load_data

# Initialize
init_storage()
init_page_config()

def main():
    st.title("Project Activity Tracker")
    
    menu = ["Project Tracker", "Issues Tracker"]
    choice = st.sidebar.selectbox("Navigation", menu)
    
    if choice == "Project Tracker":
        st.header("Project Tracker")
        projects, _ = load_data()
        
        tab1, tab2 = st.tabs(["View Projects", "Add New Project"])
        with tab1:
            render_project_list(projects)
        with tab2:
            render_project_form()
    else:
        st.header("Issues Tracker")
        projects, issues = load_data()
        
        tab1, tab2 = st.tabs(["View Issues", "Add New Issue"])
        with tab1:
            render_issue_list(issues, projects)
        with tab2:
            render_issue_form()

if __name__ == "__main__":
    main()