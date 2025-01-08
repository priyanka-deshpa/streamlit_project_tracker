# import streamlit as st
# from src.storage import load_data, save_data

# def render_admin_page():
#     projects, _ = load_data()
    
#     # Header with search and add button
#     col1, col2, _ = st.columns([2, 1, 1])
#     with col1:
#         search_query = st.text_input("🔍 Search Projects", key="project_search")
#     with col2:
#         st.button("➕ Add New Project", 
#                  use_container_width=True,
#                  on_click=lambda: setattr(st.session_state, 'page', 'project_form'))
    
#     if not projects:
#         st.info("No projects added yet.")
#         return

#     # Filter projects based on search
#     if search_query:
#         filtered_projects = [p for p in projects if search_query.lower() in p['name'].lower()]
#     else:
#         filtered_projects = projects

#     # Project list
#     st.markdown("### Projects")
#     for project in filtered_projects:
#         with st.container():
#             col1, col2, col3 = st.columns([4, 2, 2])
#             with col1:
#                 st.markdown(f"**{project['name']}**")
#             with col2:
#                 st.markdown(f"Team: {len(project['developers'])}")
#             with col3:
#                 view_col, delete_col = st.columns(2)
#                 with view_col:
#                     if st.button("👁️ View", key=f"view_{project['name']}", use_container_width=True):
#                         st.session_state.selected_project = project['name']
#                         st.session_state.page = 'project_details'
#                         st.rerun()
#                 with delete_col:
#                     if st.button("🗑️ Delete", key=f"delete_{project['name']}", use_container_width=True):
#                         if st.session_state.get('confirm_delete') == project['name']:
#                             projects.remove(project)
#                             save_data(projects, [])
#                             st.success(f"Project {project['name']} deleted successfully!")
#                             st.session_state.pop('confirm_delete', None)
#                             st.rerun()
#                         else:
#                             st.session_state.confirm_delete = project['name']
#                             st.warning(f"Click delete again to confirm removing {project['name']}")
#             st.divider()

# def render_project_details(project):
#     st.header(f"Project: {project['name']}")
    
#     tab1, tab2, tab3 = st.tabs(["Project Details", "Issues", "Timeline"])
    
#     with tab1:
#         render_project_info(project)
    
#     with tab2:
#         render_project_issues(project['name'])
    
#     with tab3:
#         render_project_timeline(project)

# def render_project_info(project):
#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("Team Information")
#         st.markdown("**Developers:**")
#         for dev in project['developers']:
#             st.markdown(f"- {dev}")
        
#         st.markdown("**Leads:**")
#         for lead in project['leads']:
#             st.markdown(f"- {lead}")
            
#         st.markdown("**ADO Board:**")
#         st.markdown(f"[Open Board]({project['ado_link']})")
        
#     with col2:
#         st.subheader("Technical Stack")
#         st.markdown(f"**Formatting:** {project['formatting_tools']}")
#         st.markdown(f"**Linting:** {project['linting_tools']}")
#         st.markdown(f"**CICD:** {project['cicd_pipeline']}")

#     st.subheader("Project Scope")
#     st.markdown(project['scope'])
    
#     st.subheader("Non-Functional Requirements")
#     st.markdown(project['nfr'])
    
#     if project.get('arch_diagram_path') or project.get('infra_diagram_path'):
#         col1, col2 = st.columns(2)
#         if project.get('arch_diagram_path'):
#             with col1:
#                 st.subheader("Architecture Diagram")
#                 st.image(project['arch_diagram_path'])
        
#         if project.get('infra_diagram_path'):
#             with col2:
#                 st.subheader("Infrastructure Diagram")
#                 st.image(project['infra_diagram_path'])

# def render_project_issues(project_name):
#     projects, issues = load_data()
#     project_issues = [i for i in issues if i['project'] == project_name]
    
#     # Search and Add buttons
#     col1, col2, _ = st.columns([2, 1, 1])
#     with col1:
#         search_query = st.text_input("🔍 Search Issues", key="issue_search")
#     with col2:
#         if st.button("➕ Add New Issue", use_container_width=True):
#             st.session_state.add_issue = True

#     # Add New Issue Form
#     if st.session_state.get('add_issue'):
#         with st.form("new_issue_form"):
#             st.subheader("Add New Issue")
#             title = st.text_input("Issue Title")
#             description = st.text_area("Issue Description")
#             status = st.selectbox("Status", ["Pending", "Completed"])
            
#             submitted = st.form_submit_button("Save Issue")
#             if submitted and title and description:
#                 new_issue = create_issue(project_name, title, description, status)
#                 issues.append(new_issue)
#                 save_data(projects, issues)
#                 st.session_state.add_issue = False
#                 st.success("Issue added successfully!")
#                 st.rerun()

#     # Filter issues based on search
#     if search_query:
#         project_issues = [i for i in project_issues 
#                          if search_query.lower() in i['title'].lower() or 
#                             search_query.lower() in i['description'].lower()]

#     # Display issues in table format
#     if project_issues:
#         for issue in project_issues:
#             with st.container():
#                 col1, col2, col3 = st.columns([3, 2, 2])
#                 with col1:
#                     st.markdown(f"**{issue['title']}**")
#                 with col2:
#                     st.markdown(f"Status: {issue['status']}")
#                 with col3:
#                     view_col, delete_col = st.columns(2)
#                     with view_col:
#                         if st.button("👁️ View", key=f"view_issue_{issue['title']}", use_container_width=True):
#                             st.session_state.selected_issue = issue
#                             st.session_state.show_issue = True
#                     with delete_col:
#                         if st.button("🗑️ Delete", key=f"delete_issue_{issue['title']}", use_container_width=True):
#                             issues.remove(issue)
#                             save_data(projects, issues)
#                             st.success("Issue deleted successfully!")
#                             st.rerun()
#                 st.divider()

#             # Show Issue Details
#             if st.session_state.get('show_issue') and st.session_state.get('selected_issue') == issue:
#                 with st.container():
#                     st.subheader("Issue Details")
#                     st.markdown(f"**Title:** {issue['title']}")
#                     st.markdown(f"**Status:** {issue['status']}")
#                     st.markdown(f"**Created:** {issue['created_at']}")
#                     st.markdown("**Description:**")
#                     st.markdown(issue['description'])
#                     if st.button("Close Details"):
#                         st.session_state.show_issue = False
#                         st.rerun()
#     else:
#         st.info("No issues found for this project.")

# def render_project_timeline(project):
#     st.subheader("Weekly Delivery Plan")
#     for week, plan in project['delivery_plan'].items():
#         with st.expander(week):
#             st.markdown(plan)
import streamlit as st
from src.storage import load_data, save_data
from src.models.issue import create_issue

def render_admin_page():
    projects, _ = load_data()
    
    # Header with Search and Add Project buttons
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input("", placeholder="🔍 Search projects by name...", key="project_search")
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
            # if st.button("👁️ View", key=f"view_{project['name']}", use_container_width=True):
            #     st.session_state.selected_project = project['name']
            #     st.session_state.page = 'project_details'
            #     st.rerun()
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

def render_project_details(project):
    st.header(f"Project: {project['name']}")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Project Details", "Issues", "Timeline"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Team Information")
            st.markdown("**Developers:**")
            for dev in project['developers']:
                st.markdown(f"- {dev}")
            st.markdown("**Leads:**")
            for lead in project['leads']:
                st.markdown(f"- {lead}")
            st.markdown(f"**ADO Board:** [{project['ado_link']}]({project['ado_link']})")
        
        with col2:
            st.subheader("Technical Stack")
            st.markdown(f"**Formatting:** {project['formatting_tools']}")
            st.markdown(f"**Linting:** {project['linting_tools']}")
            st.markdown(f"**CICD:** {project['cicd_pipeline']}")
        
        st.subheader("Project Scope")
        st.markdown(project['scope'])
        
        st.subheader("Non-Functional Requirements")
        st.markdown(project['nfr'])
        
        if project.get('arch_diagram_path') or project.get('infra_diagram_path'):
            st.subheader("Diagrams")
            col1, col2 = st.columns(2)
            if project.get('arch_diagram_path'):
                with col1:
                    st.markdown("**Architecture Diagram**")
                    st.image(project['arch_diagram_path'])
            if project.get('infra_diagram_path'):
                with col2:
                    st.markdown("**Infrastructure Diagram**")
                    st.image(project['infra_diagram_path'])
    
    with tab2:
        render_project_issues(project['name'])
    
    with tab3:
        st.subheader("Delivery Timeline")
        for week, plan in project['delivery_plan'].items():
            with st.expander(week):
                st.markdown(plan)

def render_project_issues(project_name):
    projects, issues = load_data()
    project_issues = [i for i in issues if i['project'] == project_name]
    
    # Search and Add buttons
    col1, col2= st.columns([4, 1])
    with col1:
        search_query = st.text_input("", placeholder="🔍 Search Issues....", key="issue_search")
    with col2:
        if st.button("➕ Add New Issue", use_container_width=True):
            st.session_state.add_issue = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)        

    # Filter issues based on search
    if search_query:
        project_issues = [i for i in project_issues if search_query.lower() in i['title'].lower()]

    # Add New Issue Form
    if st.session_state.get('add_issue'):
        with st.form("new_issue_form"):
            st.subheader("Add New Issue")
            title = st.text_input("Issue Title")
            description = st.text_area("Issue Description")
            status = st.selectbox("Status", ["Pending", "Completed"])
            
            submitted = st.form_submit_button("Save Issue")
            if submitted and title and description:
                new_issue = create_issue(project_name, title, description, status)
                issues.append(new_issue)
                save_data(projects, issues)
                st.session_state.add_issue = False
                st.markdown('<div class="success-message">Issue added successfully!</div>', 
                          unsafe_allow_html=True)
                st.rerun()

    # Display issues in table format
    if project_issues:
        for issue in project_issues:
            st.markdown('<div class="table-row">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**{issue['title']}**")
            with col2:
                status_class = "status-completed" if issue['status'] == "Completed" else "status-pending"
                st.markdown(f'<span class="{status_class}">Status: {issue["status"]}</span>', 
                          unsafe_allow_html=True)
            with col3:
                view_col, delete_col = st.columns(2)
                with view_col:
                    if st.button("👁️ View", key=f"view_issue_{issue['title']}", 
                               use_container_width=True):
                        st.session_state.selected_issue = issue
                        st.session_state.show_issue = True
                with delete_col:
                    if st.button("🗑️ Delete", key=f"delete_issue_{issue['title']}", 
                               use_container_width=True):
                        issues.remove(issue)
                        save_data(projects, issues)
                        st.markdown('<div class="success-message">Issue deleted successfully!</div>', 
                                  unsafe_allow_html=True)
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            # Show Issue Details
            if st.session_state.get('show_issue') and st.session_state.get('selected_issue') == issue:
                with st.container():
                    st.markdown('<div class="element-container">', unsafe_allow_html=True)
                    st.subheader("Issue Details")
                    st.markdown(f"**Title:** {issue['title']}")
                    st.markdown(f'<span class="{status_class}">Status: {issue["status"]}</span>', 
                              unsafe_allow_html=True)
                    st.markdown(f"**Created:** {issue['created_at']}")
                    st.markdown("**Description:**")
                    st.markdown(issue['description'])
                    if st.button("Close Details"):
                        st.session_state.show_issue = False
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-message">No issues found for this project.</div>', 
                   unsafe_allow_html=True)