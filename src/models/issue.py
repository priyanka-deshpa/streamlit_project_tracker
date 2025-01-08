from datetime import datetime

def create_issue(project, title, description, status="Pending"):
    return {
        "project": project,
        "title": title,
        "description": description,
        "status": status,
        "created_at": datetime.now().isoformat()
    }