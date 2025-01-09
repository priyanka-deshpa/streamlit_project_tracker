import streamlit as st
from src.config import init_page_config
from src.storage import init_storage
from src.views.project_view import render_project_form, render_project_details
from src.views.issue_view import render_issue_list, render_issue_form
from src.views.admin_view import render_admin_page
from src.storage import load_data

# Initialize
init_storage()
init_page_config()

def main():
    st.title("Project Activity Tracker")
    
    # Initialize session state if needed
    if "page" not in st.session_state:
        st.session_state.page = "admin"
    
    # Determine current page
    current_page = st.session_state.page
    
    if current_page == "project_form":
        render_project_form()
    elif current_page == "edit_project":
        render_project_form(st.session_state.project_to_edit)
    elif current_page == "issues":
        projects, issues = load_data()
        if st.button("Back to Admin"):
            st.session_state.page = "admin"
            st.rerun()
        # tab1, tab2 = st.tabs(["View Issues", "Add New Issue"])
        # with tab1:
        #     render_issue_list(issues, projects)
        # with tab2:
        #     render_issue_form()
    elif current_page == "edit_issue":
        render_issue_form(st.session_state.issue_to_edit)
    elif current_page == "project_details":
        if st.button("Back to Admin"):
            st.session_state.page = "admin"
            st.rerun()
        projects, _ = load_data()
        project = next((p for p in projects if p['name'] == st.session_state.selected_project), None)
        if project:
            render_project_details(project)
    else:  # Default to admin page
        render_admin_page()

if __name__ == "__main__":
    main()