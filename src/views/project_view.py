import streamlit as st
from src.models.project import create_project, Project
from src.storage import save_data, load_data
from src.storage.factory import get_storage_provider
from src.models.issue import create_issue
from src.views.issue_view import render_issue_list

def render_project_list(projects):
    if not projects:
        st.info("No projects added yet.")
        return
        
    for project in projects:
        with st.expander(f"Project: {project['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Project Details")
                st.write(f"**Team:**")
                st.write(f"- Developers: {', '.join(project['developers'])}")
                st.write(f"- Leads: {', '.join(project['leads'])}")
                st.write(f"**High Level Scope:**")
                st.write(project['scope'])
                st.write(f"**ADO Board:** [{project['ado_link']}]({project['ado_link']})")
            
            with col2:
                st.subheader("Technical Details")
                st.write("**Tools & Quality:**")
                st.write(f"- Formatting: {project['formatting_tools']}")
                st.write(f"- Linting: {project['linting_tools']}")
                st.write(f"- CICD: {project['cicd_pipeline']}")
                
                if project.get('arch_diagram_path'):
                    st.write("**Architecture Diagram:**")
                    st.image(project['arch_diagram_path'])
                
                if project.get('infra_diagram_path'):
                    st.write("**Infrastructure Diagram:**")
                    st.image(project['infra_diagram_path'])

def render_project_form(project_to_edit=None):
    projects, _ = load_data()
    
    # Add Cancel button before the form
    if st.button("← Cancel", key="cancel_project"):
        st.session_state.page = "admin"
        st.rerun()
    
    with st.form("project_form"):
        st.subheader("Project Details")
        
        # Pre-fill form if editing
        project_name = st.text_input(
            "Project Name *", 
            value=project_to_edit["name"] if project_to_edit else "",
            help="Project name (3-100 characters)"
        )
        
        developers = st.text_input(
            "Developers (comma-separated) *", 
            value=",".join(project_to_edit["developers"]) if project_to_edit else "",
            help="List of developers (minimum 2 characters per name)"
        )
        
        leads = st.text_input(
            "Leads (comma-separated) *",
            value=",".join(project_to_edit["leads"]) if project_to_edit else "",
            help="List of project leads (minimum 2 characters per name)"
        )
        
        scope = st.text_area(
            "High Level Scope *", 
            value=project_to_edit["scope"] if project_to_edit else "",
            help="Project scope (50-2000 characters)"
        )
        
        ado_link = st.text_input(
            "ADO Board Link *", 
            value=project_to_edit["ado_link"] if project_to_edit else "",
            help="Valid Azure DevOps board URL (must start with http:// or https://)"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            formatting_tools = st.text_input(
                "Formatting Tools *",
                value=project_to_edit["formatting_tools"] if project_to_edit else "",
                help="Formatting tools (3-200 characters)"
            )
            linting_tools = st.text_input(
                "Linting Tools *",
                value=project_to_edit["linting_tools"] if project_to_edit else "",
                help="Linting tools (3-200 characters)"
            )
        
        with col2:
            cicd_pipeline = st.text_input(
                "CICD Pipeline *",
                value=project_to_edit["cicd_pipeline"] if project_to_edit else "",
                help="CI/CD pipeline configuration (3-200 characters)"
            )
            storage_option = st.selectbox("Storage Provider for Diagrams *", ["local", "s3", "azure"])
        
        col3, col4 = st.columns(2)
        with col3:
            arch_diagram = st.file_uploader("Technical Architecture Diagram (optional)", type=['png', 'jpg', 'jpeg'])
        with col4:
            infra_diagram = st.file_uploader("Infrastructure Diagram (optional)", type=['png', 'jpg', 'jpeg'])
        
        weeks = st.number_input(
            "Number of Weeks for Delivery Plan *",
            min_value=1,
            max_value=52,
            value=len(project_to_edit["delivery_plan"]) if project_to_edit else 4
        )
        
        delivery_plan = {}
        st.write("Weekly Delivery Plan: * (minimum 10 characters per plan)")
        for week in range(1, weeks + 1):
            week_key = f"Week {week}"
            delivery_plan[week_key] = st.text_area(
                f"Week {week} Plan *",
                value=project_to_edit["delivery_plan"].get(week_key, "") if project_to_edit else "",
                help="Minimum 10 characters required"
            )
        
        nfr = st.text_area(
            "Non-Functional Requirements *",
            value=project_to_edit["nfr"] if project_to_edit else "",
            help="Non-functional requirements (50-2000 characters)"
        )
        
        # Add note about required fields
        st.markdown("**Note:** Fields marked with * are required")
        
        col_submit, col_clear = st.columns([1, 4])
        with col_submit:
            submitted = st.form_submit_button("Save Project")
        
        if submitted:
            # Validate required fields
            if not all([project_name, developers, leads, scope, ado_link, 
                       formatting_tools, linting_tools, cicd_pipeline, 
                       all(plan.strip() for plan in delivery_plan.values()), nfr]):
                st.error("Please fill in all required fields marked with *")
                return
            
            try:
                storage_provider = get_storage_provider(storage_option)
                project_data = create_project(
                    project_name, developers, leads, scope, ado_link,
                    formatting_tools, linting_tools, cicd_pipeline,
                    delivery_plan, nfr, arch_diagram, infra_diagram,
                    storage_provider
                )
                
                if project_to_edit:
                    # Update existing project
                    project_idx = next(
                        (i for i, p in enumerate(projects) if p["name"] == project_to_edit["name"]),
                        None
                    )
                    if project_idx is not None:
                        # Preserve existing diagram paths if no new uploads
                        if not arch_diagram:
                            project_data["arch_diagram_path"] = project_to_edit.get("arch_diagram_path")
                        if not infra_diagram:
                            project_data["infra_diagram_path"] = project_to_edit.get("infra_diagram_path")
                        projects[project_idx] = project_data
                else:
                    # Add new project
                    projects.append(project_data)
                
                save_data(projects, [])
                st.success("Project saved successfully!")
                st.session_state.page = "admin"
                st.rerun()
            except ValueError as e:
                st.error(f"Validation error: {str(e)}")
                
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
                
def render_project_details(project):
    st.header(f"Project: {project['name']}")
    
    # Add Edit button
    if st.button("✏️ Edit Project"):
        st.session_state.project_to_edit = project
        st.session_state.page = "edit_project"
        st.rerun()
    
    # Create tabs for different sections
    overview_tab, issues_tab, timeline_tab = st.tabs(["Overview", "Issues", "Timeline"])
    
    with overview_tab:
        # Project Overview
        st.subheader("Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Team**")
            st.write(f"🧑‍💻 **Developers:** {', '.join(project['developers'])}")
            st.write(f"👥 **Leads:** {', '.join(project['leads'])}")
        
        with col2:
            st.write("**Links**")
            st.write(f"📋 [ADO Board]({project['ado_link']})")
        
        # Scope and Requirements
        st.subheader("Scope and Requirements")
        with st.expander("High Level Scope", expanded=True):
            st.write(project['scope'])
        
        with st.expander("Non-Functional Requirements", expanded=True):
            st.write(project['nfr'])
        
        # Technical Setup
        st.subheader("Technical Setup")
        col3, col4 = st.columns(2)
        with col3:
            st.write("**Development Tools**")
            st.write(f"🔧 **Formatting:** {project['formatting_tools']}")
            st.write(f"🔍 **Linting:** {project['linting_tools']}")
        
        with col4:
            st.write("**Infrastructure**")
            st.write(f"⚙️ **CICD Pipeline:** {project['cicd_pipeline']}")
        
        # Diagrams
        st.subheader("Technical Diagrams")
        col5, col6 = st.columns(2)
        with col5:
            if project.get('arch_diagram_path'):
                st.write("**Architecture Diagram**")
                st.image(project['arch_diagram_path'])
        
        with col6:
            if project.get('infra_diagram_path'):
                st.write("**Infrastructure Diagram**")
                st.image(project['infra_diagram_path'])
        
        # Delivery Plan
        st.subheader("Delivery Plan")
        for week, plan in project['delivery_plan'].items():
            with st.expander(week):
                st.write(plan)
    
    with issues_tab:
        #  _, issues = load_data()
        render_issue_list(project['name'])
    
    with timeline_tab:
        st.subheader("Delivery Timeline")
        for week, plan in project['delivery_plan'].items():
            with st.expander(week):
                st.markdown(plan)             