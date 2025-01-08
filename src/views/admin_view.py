# import streamlit as st
# import pandas as pd
# from src.storage import load_data, save_data

# def delete_project(project_name):
#     projects, issues = load_data()
#     projects = [p for p in projects if p['name'] != project_name]
#     issues = [i for i in issues if i['project'] != project_name]
#     save_data(projects, issues)

# def render_project_details(project_details):
#     st.markdown("### Project Details")
#     st.write(f"**Project Name:** {project_details['name']}")
#     st.write(f"**Team Leads:** {', '.join(project_details['leads'])}")
#     st.write(f"**Developers:** {', '.join(project_details['developers'])}")
#     st.write(f"**Scope:** {project_details['scope']}")
#     st.write(f"**ADO Link:** [{project_details['ado_link']}]({project_details['ado_link']})")
#     st.write(f"**Formatting Tools:** {project_details['formatting_tools']}")
#     st.write(f"**Linting Tools:** {project_details['linting_tools']}")
#     st.write(f"**CICD Pipeline:** {project_details['cicd_pipeline']}")
    
#     if 'arch_diagram_path' in project_details:
#         st.write("**Architecture Diagram:**")
#         st.image(project_details['arch_diagram_path'])
    
#     if 'infra_diagram_path' in project_details:
#         st.write("**Infrastructure Diagram:**")
#         st.image(project_details['infra_diagram_path'])

# def render_admin_page():
#     # Header with buttons
#     col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
#     with col1:
#         pass
#     with col2:
#         if st.button("Add New Project", type="primary"):
#             st.session_state.page = "project_form"
#             st.rerun()
#     with col3:
#         if st.button("Issue Tracker", type="secondary"):
#             st.session_state.page = "issues"
#             st.rerun()
#     with col4:
#         if st.button("Delete Selected", type="secondary"):
#             if 'selected_project' in st.session_state:
#                 delete_project(st.session_state.selected_project)
#                 st.success(f"Project {st.session_state.selected_project} deleted!")
#                 del st.session_state.selected_project
#                 st.rerun()

#     # Load projects
#     projects, _ = load_data()
    
#     if not projects:
#         st.info("No projects available. Click 'Add New Project' to create one.")
#         return

#     # Convert projects to DataFrame
#     project_data = []
#     for project in projects:
#         project_data.append({
#             'Project Name': project['name'],
#             'Team Leads': ', '.join(project['leads']),
#             'Team Size': len(project['developers']),
#             'ADO Link': f"[Link]({project['ado_link']})"
#         })
    
#     df = pd.DataFrame(project_data)
    
#     # Display projects table
#     st.markdown("### Project Overview")
    
#     # Create clickable project names using markdown
#     for index, row in df.iterrows():
#         cols = st.columns([3, 2, 1, 2])
#         with cols[0]:
#             if st.button(row['Project Name'], key=f"project_{index}"):
#                 st.session_state.page = "project_details"
#                 st.session_state.selected_project = row['Project Name']
#                 st.rerun()
#         with cols[1]:
#             st.write(row['Team Leads'])
#         with cols[2]:
#             st.write(row['Team Size'])
#         with cols[3]:
#             st.markdown(row['ADO Link'])
import streamlit as st
from src.storage import load_data, save_data

def render_admin_page():
    projects, _ = load_data()
    
    # Header buttons
    col1, col2 = st.columns([2, 2])
    with col1:
        st.button("➕ Add New Project", 
                 use_container_width=True,
                 on_click=lambda: setattr(st.session_state, 'page', 'project_form'))
    with col2:
        st.button("📊 Issues Dashboard", 
                 use_container_width=True,
                 on_click=lambda: setattr(st.session_state, 'page', 'issues'))
    
    if not projects:
        st.info("No projects added yet.")
        return

    # Project list with better styling
    st.markdown("### Projects Overview:")
    for project in projects:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 2, 2])
            with col1:
                st.markdown(f"**{project['name']}**")
            with col2:
                st.markdown(f"Team Size: {len(project['developers'])}")
            with col3:
                st.markdown(f"Leads: {', '.join(project['leads'])}")
            with col4:
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
            st.divider()

def render_project_details(project):
    st.header(f"Project: {project['name']}")
    
    # Project Overview
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Team Information")
            st.markdown("**Developers:**")
            for dev in project['developers']:
                st.markdown(f"- {dev}")
            
            st.markdown("**Leads:**")
            for lead in project['leads']:
                st.markdown(f"- {lead}")
                
            st.markdown("**ADO Board:**")
            st.markdown(f"[Open Board]({project['ado_link']})")
            
        with col2:
            st.subheader("Technical Stack")
            st.markdown(f"**Formatting:** {project['formatting_tools']}")
            st.markdown(f"**Linting:** {project['linting_tools']}")
            st.markdown(f"**CICD:** {project['cicd_pipeline']}")
    
    # Project Details
    st.subheader("Project Scope")
    st.markdown(project['scope'])
    
    st.subheader("Delivery Plan")
    for week, plan in project['delivery_plan'].items():
        with st.expander(week):
            st.markdown(plan)
    
    st.subheader("Non-Functional Requirements")
    st.markdown(project['nfr'])
    
    # Diagrams
    if project.get('arch_diagram_path') or project.get('infra_diagram_path'):
        col1, col2 = st.columns(2)
        if project.get('arch_diagram_path'):
            with col1:
                st.subheader("Architecture Diagram")
                st.image(project['arch_diagram_path'])
        
        if project.get('infra_diagram_path'):
            with col2:
                st.subheader("Infrastructure Diagram")
                st.image(project['infra_diagram_path'])