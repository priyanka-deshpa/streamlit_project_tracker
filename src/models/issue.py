from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Comment(BaseModel):
    text: str
    created_at: datetime = Field(default_factory=datetime.now)
    author: str

class Issue(BaseModel):
    project: str
    title: str
    description: str
    status: str = "Pending"
    created_at: datetime = Field(default_factory=datetime.now)
    comments: List[Comment] = Field(default_factory=list)

def create_issue(project: str, title: str, description: str, author: str) -> dict:
    issue = Issue(
        project=project,
        title=title,
        description=description,
        author=author
    )
    return issue.model_dump()