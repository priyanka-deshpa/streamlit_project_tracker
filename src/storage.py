import json
import os
from pathlib import Path

def init_storage():
    Path("data").mkdir(exist_ok=True)
    Path("uploads").mkdir(exist_ok=True)
    
    if not os.path.exists("data/projects.json"):
        with open("data/projects.json", "w") as f:
            json.dump([], f)
    
    if not os.path.exists("data/issues.json"):
        with open("data/issues.json", "w") as f:
            json.dump([], f)

def load_data():
    with open("data/projects.json", "r") as f:
        projects = json.load(f)
    with open("data/issues.json", "r") as f:
        issues = json.load(f)
    return projects, issues

def save_data(projects, issues):
    with open("data/projects.json", "w") as f:
        json.dump(projects, f)
    with open("data/issues.json", "w") as f:
        json.dump(issues, f)