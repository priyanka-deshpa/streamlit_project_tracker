import streamlit as st
from src.models.project import create_project
from src.storage import save_data, load_data
from src.storage.factory import get_storage_provider

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

def render_project_form():
    projects, _ = load_data()
    
    with st.form("new_project_form"):
        project_name = st.text_input("Project Name")
        developers = st.text_input("Developers (comma-separated)")
        leads = st.text_input("Leads (comma-separated)")
        scope = st.text_area("High Level Scope")
        ado_link = st.text_input("ADO Board Link")
        
        col1, col2 = st.columns(2)
        with col1:
            formatting_tools = st.text_input("Formatting Tools")
            linting_tools = st.text_input("Linting Tools")
        
        with col2:
            cicd_pipeline = st.text_input("CICD Pipeline")
            storage_option = st.selectbox(
                "Storage Provider for Diagrams",
                ["local", "s3", "azure"]
            )
        
        col3, col4 = st.columns(2)
        with col3:
            arch_diagram = st.file_uploader(
                "Technical Architecture Diagram",
                type=['png', 'jpg', 'jpeg', 'pdf']
            )
        with col4:
            infra_diagram = st.file_uploader(
                "Infrastructure Diagram",
                type=['png', 'jpg', 'jpeg', 'pdf']
            )
        
        weeks = st.number_input("Number of Weeks for Delivery Plan", min_value=1, max_value=52, value=4)
        
        delivery_plan = {}
        st.write("Weekly Delivery Plan:")
        for week in range(1, weeks + 1):
            delivery_plan[f"Week {week}"] = st.text_area(f"Week {week} Plan")
        
        nfr = st.text_area("Non-Functional Requirements")
        
        submitted = st.form_submit_button("Add Project")
        
        if submitted and project_name:
            try:
                storage_provider = get_storage_provider(storage_option)
                new_project = create_project(
                    project_name, developers, leads, scope, ado_link,
                    formatting_tools, linting_tools, cicd_pipeline,
                    delivery_plan, nfr, arch_diagram, infra_diagram,
                    storage_provider
                )
                projects.append(new_project)
                save_data(projects, [])
                st.success("Project added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving project: {str(e)}")