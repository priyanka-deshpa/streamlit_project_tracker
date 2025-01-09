from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, HttpUrl, field_validator, constr
from src.storage.database import save_project, update_project

class DeliveryPlan(BaseModel):
    """Model for weekly delivery plan validation"""
    week_number: constr(pattern=r'^Week \d+$')
    plan_details: constr(min_length=10, max_length=1000)

class Project(BaseModel):
    """Project model with enhanced validation"""
    name: constr(min_length=3, max_length=100) = Field(..., description="Project name (3-100 characters)")
    developers: List[constr(min_length=2, max_length=50)] = Field(..., description="List of developers")
    leads: List[constr(min_length=2, max_length=50)] = Field(..., description="List of project leads")
    scope: constr(min_length=50, max_length=2000) = Field(..., description="Project scope (50-2000 characters)")
    ado_link: HttpUrl = Field(..., description="Azure DevOps board link")
    formatting_tools: constr(min_length=3, max_length=200) = Field(..., description="Formatting tools used")
    linting_tools: constr(min_length=3, max_length=200) = Field(..., description="Linting tools used")
    cicd_pipeline: constr(min_length=3, max_length=1000) = Field(..., description="CI/CD pipeline configuration")
    delivery_plan: Dict[str, str] = Field(..., description="Weekly delivery plan")
    nfr: constr(min_length=50, max_length=2000) = Field(..., description="Non-functional requirements")
    created_at: datetime = Field(default_factory=datetime.now)
    arch_diagram_path: Optional[str] = Field(None, description="Path to architecture diagram")
    infra_diagram_path: Optional[str] = Field(None, description="Path to infrastructure diagram")

    @field_validator('developers', 'leads')
    def validate_team_members(cls, v):
        if not v:
            raise ValueError("At least one team member is required")
        return v

    @field_validator('delivery_plan')
    def validate_delivery_plan(cls, v):
        if not v:
            raise ValueError("Delivery plan is required")
        
        for week, plan in v.items():
            if not week.startswith('Week '):
                raise ValueError(f"Invalid week format: {week}")
            if not plan or len(plan.strip()) < 10:
                raise ValueError(f"Plan for {week} must be at least 10 characters")
        return v

    @field_validator('ado_link')
    def validate_ado_link(cls, v):
        if not str(v).startswith(('http://', 'https://')):
            raise ValueError("ADO link must be a valid HTTP(S) URL")
        return str(v)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        error_msg_templates = {
            'value_error.missing': 'This field is required',
            'value_error.url.scheme': 'ADO link must be a valid HTTP(S) URL',
            'value_error.any_str.min_length': 'Minimum length: {limit_value}',
            'value_error.any_str.max_length': 'Maximum length: {limit_value}'
        }

def create_project(
    project_name: str,
    developers: str,
    leads: str,
    scope: str,
    ado_link: str,
    formatting_tools: str,
    linting_tools: str,
    cicd_pipeline: str,
    delivery_plan: Dict[str, str],
    nfr: str,
    arch_diagram=None,
    infra_diagram=None,
    storage_provider=None
) -> dict:
    try:
        # Create project data dictionary
        project_data = {
            "name": project_name,
            "developers": [dev.strip() for dev in developers.split(",") if dev.strip()],
            "leads": [lead.strip() for lead in leads.split(",") if lead.strip()],
            "scope": scope,
            "ado_link": ado_link,
            "formatting_tools": formatting_tools,
            "linting_tools": linting_tools,
            "cicd_pipeline": cicd_pipeline,
            "delivery_plan": delivery_plan,
            "nfr": nfr
        }

        # Handle file uploads if provided
        if storage_provider and (arch_diagram or infra_diagram):
            project_prefix = project_name.lower().replace(' ', '_')
            
            if arch_diagram:
                file_ext = arch_diagram.type.split('/')[-1]
                file_name = f"{project_prefix}_arch.{file_ext}"
                project_data["arch_diagram_path"] = storage_provider.upload_file(arch_diagram, file_name)
            
            if infra_diagram:
                file_ext = infra_diagram.type.split('/')[-1]
                file_name = f"{project_prefix}_infra.{file_ext}"
                project_data["infra_diagram_path"] = storage_provider.upload_file(infra_diagram, file_name)

        # Validate project data using Pydantic model
        project = Project(**project_data)
        
        # Save to database
        if save_project(project.dict()):
            return project.dict()
        raise ValueError("Failed to save project to database")

    except Exception as e:
        raise ValueError(f"Project validation failed: {str(e)}")