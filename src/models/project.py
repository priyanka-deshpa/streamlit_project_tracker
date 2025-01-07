from datetime import datetime
import os

def create_project(
    project_name, developers, leads, scope, ado_link,
    formatting_tools, linting_tools, cicd_pipeline,
    delivery_plan, nfr, arch_diagram=None, infra_diagram=None,
    storage_provider=None
):
    new_project = {
        "name": project_name,
        "developers": [dev.strip() for dev in developers.split(",") if dev.strip()],
        "leads": [lead.strip() for lead in leads.split(",") if lead.strip()],
        "scope": scope,
        "ado_link": ado_link,
        "formatting_tools": formatting_tools,
        "linting_tools": linting_tools,
        "cicd_pipeline": cicd_pipeline,
        "delivery_plan": delivery_plan,
        "nfr": nfr,
        "created_at": datetime.now().isoformat()
    }
    
    if storage_provider and (arch_diagram or infra_diagram):
        project_prefix = project_name.lower().replace(' ', '_')
        
        if arch_diagram:
            file_ext = arch_diagram.type.split('/')[-1]
            file_name = f"{project_prefix}_arch.{file_ext}"
            new_project["arch_diagram_path"] = storage_provider.upload_file(arch_diagram, file_name)
        
        if infra_diagram:
            file_ext = infra_diagram.type.split('/')[-1]
            file_name = f"{project_prefix}_infra.{file_ext}"
            new_project["infra_diagram_path"] = storage_provider.upload_file(infra_diagram, file_name)
    
    return new_project