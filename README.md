# Project Activity Tracker

A Streamlit application for tracking project activities and managing technical issues with a modern, responsive UI.

## Features

### Project Management
- Create and view projects with detailed information
- Search projects by name
- Upload and store architecture diagrams with multiple storage options (Local/S3/Azure)
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
├── app.py                    # Main application entry point
├── src/
│   ├── config.py            # Application configuration and UI setup
│   ├── static/
│   │   └── style.css        # Custom CSS styles
│   ├── storage/
│   │   ├── __init__.py      # Storage initialization
│   │   ├── base.py          # Base storage provider interface
│   │   ├── factory.py       # Storage provider factory
│   │   ├── local_storage.py # Local file storage
│   │   ├── s3_storage.py    # AWS S3 storage
│   │   └── azure_storage.py # Azure Blob storage
│   ├── models/
│   │   ├── project.py       # Project data model
│   │   └── issue.py         # Issue data model
│   └── views/
│       ├── admin_view.py    # Admin dashboard UI
│       ├── project_view.py  # Project management UI
│       └── issue_view.py    # Issue tracking UI
├── data/                    # JSON data storage
└── uploads/                # Local file storage
```

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure storage provider (optional):
   - Create `.env` file
   - Update with your storage credentials

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Storage Providers

The application supports multiple storage providers for diagram uploads:

- **Local Storage**: Default, stores files in `uploads/` directory
- **AWS S3**: Configure via environment variables:
  - `AWS_BUCKET_NAME`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
- **Azure Blob**: Configure via environment variables:
  - `AZURE_CONNECTION_STRING`
  - `AZURE_CONTAINER_NAME`

## Data Storage

- Projects and issues are stored in JSON files under the `data/` directory
- Architecture diagrams are stored based on the configured storage provider
- Data is automatically saved when adding or updating records

