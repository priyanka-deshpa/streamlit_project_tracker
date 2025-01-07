from datetime import datetime

def create_issue(project, title, description):
    return {
        "project": project,
        "title": title,
        "description": description,
        "status": "Pending",
        "created_at": datetime.now().isoformat()
    }