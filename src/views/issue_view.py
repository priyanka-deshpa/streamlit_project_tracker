import streamlit as st
from src.models.issue import create_issue
from src.storage import save_data, load_data

def render_issue_list(issues, projects):
    if not issues:
        st.info("No issues recorded yet.")
        return
        
    status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
    project_filter = st.selectbox("Filter by Project", ["All"] + [p["name"] for p in projects])
    
    filtered_issues = issues
    if status_filter != "All":
        filtered_issues = [i for i in filtered_issues if i["status"] == status_filter]
    if project_filter != "All":
        filtered_issues = [i for i in filtered_issues if i["project"] == project_filter]
    
    for issue in filtered_issues:
        with st.expander(f"Issue: {issue['title']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Project:** {issue['project']}")
                st.write(f"**Description:** {issue['description']}")
                st.write(f"**Created:** {issue['created_at']}")
            with col2:
                st.write(f"**Status:** {issue['status']}")
                if st.button(f"Mark as {'Pending' if issue['status'] == 'Completed' else 'Completed'}", key=f"toggle_{issue['created_at']}"):
                    issue["status"] = "Pending" if issue["status"] == "Completed" else "Completed"
                    save_data(projects, issues)
                    st.experimental_rerun()

def render_issue_form():
    projects, issues = load_data()
    
    with st.form("new_issue_form"):
        project = st.selectbox("Select Project", [p["name"] for p in projects])
        title = st.text_input("Issue Title")
        description = st.text_area("Issue Description")
        
        submitted = st.form_submit_button("Add Issue")
        
        if submitted and title and description:
            new_issue = create_issue(project, title, description)
            issues.append(new_issue)
            save_data(projects, issues)
            st.success("Issue added successfully!")
            st.experimental_rerun()