import streamlit as st
from src.storage import load_data, save_data
# from src.models.issue import create_issue

def render_admin_page():
    projects, _ = load_data()
    
    # Header with Search and Add Project buttons in one line
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input("Search Projects", placeholder="🔍 Search projects by name...", key="project_search", label_visibility="collapsed")
    with col2:
        if st.button("➕ Add New Project", use_container_width=True):
            st.session_state.page = 'project_form'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if not projects:
        st.markdown('<div class="info-message">No projects added yet.</div>', unsafe_allow_html=True)
        return

    # Filter projects based on search
    if search_query:
        projects = [p for p in projects if search_query.lower() in p['name'].lower()]

    # Project list with styling
    for project in projects:
        st.markdown('<div class="table-row">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            st.markdown(f"**{project['name']}**")
        with col2:
            st.markdown(f"Team Size: {len(project['developers'])}")
        with col3:
            view_col, delete_col = st.columns(2)
            with view_col:
                if st.button("👁️ View", key=f"view_{project['name']}", use_container_width=True):
                    st.session_state.selected_project = project['name']
                    st.session_state.page = 'project_details'
                    st.rerun()
            with delete_col:
                if st.button("🗑️ Delete", key=f"delete_{project['name']}", use_container_width=True):
                    if st.session_state.get('confirm_delete') == project['name']:
                        projects.remove(project)
                        save_data(projects, [])
                        st.success(f"Project {project['name']} deleted successfully!")
                        st.session_state.pop('confirm_delete', None)
                        st.rerun()
                    else:
                        st.session_state.confirm_delete = project['name']
                        st.warning(f"Click delete again to confirm removing {project['name']}")
        st.markdown('</div>', unsafe_allow_html=True)



