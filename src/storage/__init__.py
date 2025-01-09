from .factory import get_storage_provider
from .base import StorageProvider
from .local_storage import LocalStorage
from .s3_storage import S3Storage
from .azure_storage import AzureStorage

# Import core storage functions
from pathlib import Path
import json
import os
from .database import init_db, get_all_projects, save_project, update_project, delete_project

def init_storage():
    Path("data").mkdir(exist_ok=True)
    Path("uploads").mkdir(exist_ok=True)
    init_db()
    
    # Initialize with empty arrays if files don't exist
    if not os.path.exists("data/projects.json"):
        with open("data/projects.json", "w") as f:
            json.dump([], f)
    
    if not os.path.exists("data/issues.json"):
        with open("data/issues.json", "w") as f:
            json.dump([], f)

def load_data():
    """Load projects and issues from storage."""
    projects = get_all_projects()
    
    # For now, keep issues in JSON file
    if not os.path.exists("data/issues.json"):
        with open("data/issues.json", "w") as f:
            json.dump([], f)
    
    try:
        with open("data/issues.json", "r") as f:
            issues = json.load(f)
    except json.JSONDecodeError:
        issues = []
        with open("data/issues.json", "w") as f:
            json.dump(issues, f)
    
    return projects, issues

def save_data(projects, issues):
    with open("data/projects.json", "w") as f:
        json.dump(projects, f, default=str)  # Use str as fallback serializer
    with open("data/issues.json", "w") as f:
        json.dump(issues, f, default=str)  # Use str as fallback serializer