from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class IssueAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    repo_url: str
    issue_number: int
    summary: str
    type: str
    priority_score: int
    suggested_labels: str  # Comma-separated string
    potential_impact: str
    full_json: str  # Original JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
