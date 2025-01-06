# Project Activity Tracker

A Streamlit application for tracking project activities and managing technical issues.

## Features

### Project Management
- Create and view projects with detailed information
- Upload and store architecture diagrams
- Track weekly delivery plans
- Manage team information (developers and leads)
- Record technical details:
  - Formatting tools
  - Linting tools
  - CICD pipeline configuration
  - Non-functional requirements

### Issue Tracking
- Create and manage project-specific issues
- Track issue status (Pending/Completed)
- Filter issues by project and status
- Update issue status with one click

## Project Structure

```
.
├── app.py                 # Main application entry point
├── src/
│   ├── config.py         # Application configuration
│   ├── storage.py        # Data storage operations
│   ├── models/
│   │   ├── project.py    # Project data model
│   │   └── issue.py      # Issue data model
│   └── views/
│       ├── project_view.py # Project UI components
│       └── issue_view.py  # Issue UI components
├── data/                  # JSON data storage
└── uploads/              # Uploaded files storage
```

## Setup

1. Install Python dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python3 -m streamlit run app.py
   ```

## Usage

1. **Project Tracker**
   - View existing projects in an expandable list
   - Add new projects with detailed information
   - Upload architecture diagrams
   - Define weekly delivery plans

2. **Issues Tracker**
   - View and filter issues by project and status
   - Add new issues for specific projects
   - Toggle issue status between Pending and Completed

## Data Storage

- Projects and issues are stored in JSON files under the `data/` directory
- Architecture diagrams are stored in the `uploads/` directory
- Data is automatically saved when adding or updating records