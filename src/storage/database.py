import sqlite3
from datetime import datetime
from pathlib import Path

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    db_path = Path("data/project_tracker.db")
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        developers TEXT NOT NULL,
        leads TEXT NOT NULL,
        scope TEXT NOT NULL,
        ado_link TEXT NOT NULL,
        formatting_tools TEXT NOT NULL,
        linting_tools TEXT NOT NULL,
        cicd_pipeline TEXT NOT NULL,
        nfr TEXT NOT NULL,
        arch_diagram_path TEXT,
        infra_diagram_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create delivery_plans table with foreign key to projects
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS delivery_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        week_number TEXT NOT NULL,
        plan_details TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection."""
    conn = sqlite3.connect('data/project_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

def save_project(project_data):
    """Save project data to the database."""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute('BEGIN')
        
        # Insert project details
        cursor.execute('''
        INSERT INTO projects (
            name, developers, leads, scope, ado_link,
            formatting_tools, linting_tools, cicd_pipeline,
            nfr, arch_diagram_path, infra_diagram_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_data['name'],
            ','.join(project_data['developers']),
            ','.join(project_data['leads']),
            project_data['scope'],
            project_data['ado_link'],
            project_data['formatting_tools'],
            project_data['linting_tools'],
            project_data['cicd_pipeline'],
            project_data['nfr'],
            project_data.get('arch_diagram_path'),
            project_data.get('infra_diagram_path')
        ))
        
        project_id = cursor.lastrowid
        
        # Insert delivery plans
        for week, plan in project_data['delivery_plan'].items():
            cursor.execute('''
            INSERT INTO delivery_plans (project_id, week_number, plan_details)
            VALUES (?, ?, ?)
            ''', (project_id, week, plan))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_project(project_name, project_data):
    """Update existing project in the database."""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('BEGIN')
        
        # Get project id
        cursor.execute('SELECT id FROM projects WHERE name = ?', (project_name,))
        project_id = cursor.fetchone()['id']
        
        # Update project details
        cursor.execute('''
        UPDATE projects SET
            name = ?, developers = ?, leads = ?, scope = ?, ado_link = ?,
            formatting_tools = ?, linting_tools = ?, cicd_pipeline = ?,
            nfr = ?, arch_diagram_path = ?, infra_diagram_path = ?
        WHERE id = ?
        ''', (
            project_data['name'],
            ','.join(project_data['developers']),
            ','.join(project_data['leads']),
            project_data['scope'],
            project_data['ado_link'],
            project_data['formatting_tools'],
            project_data['linting_tools'],
            project_data['cicd_pipeline'],
            project_data['nfr'],
            project_data.get('arch_diagram_path'),
            project_data.get('infra_diagram_path'),
            project_id
        ))
        
        # Delete existing delivery plans
        cursor.execute('DELETE FROM delivery_plans WHERE project_id = ?', (project_id,))
        
        # Insert new delivery plans
        for week, plan in project_data['delivery_plan'].items():
            cursor.execute('''
            INSERT INTO delivery_plans (project_id, week_number, plan_details)
            VALUES (?, ?, ?)
            ''', (project_id, week, plan))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_all_projects():
    """Retrieve all projects from the database."""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Get all projects
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        
        result = []
        for project in projects:
            # Get delivery plans for each project
            cursor.execute('SELECT week_number, plan_details FROM delivery_plans WHERE project_id = ?', (project['id'],))
            delivery_plans = {row['week_number']: row['plan_details'] for row in cursor.fetchall()}
            
            # Convert to dictionary format
            project_dict = dict(project)
            project_dict['developers'] = project_dict['developers'].split(',')
            project_dict['leads'] = project_dict['leads'].split(',')
            project_dict['delivery_plan'] = delivery_plans
            
            # Remove database-specific fields
            project_dict.pop('id', None)
            
            result.append(project_dict)
        
        return result
    finally:
        conn.close()

def delete_project(project_name):
    """Delete a project from the database."""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('BEGIN')
        
        # Get project id
        cursor.execute('SELECT id FROM projects WHERE name = ?', (project_name,))
        project = cursor.fetchone()
        
        if project:
            project_id = project['id']
            
            # Delete delivery plans first (due to foreign key constraint)
            cursor.execute('DELETE FROM delivery_plans WHERE project_id = ?', (project_id,))
            
            # Delete project
            cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
            
            conn.commit()
            return True
        return False
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()