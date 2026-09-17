"""
Data Schemas (Pydantic Models)
Assigned to: Backend Team

Define your request and response models here for type validation.
"""

from typing import List, Optional
from pydantic import BaseModel

class CandidateSchema(BaseModel):
    # TODO: Define fields for candidate
    name: str
    email: Optional[str] = None
    skills: List[str] = []

class JobDescriptionSchema(BaseModel):
    # TODO: Define fields for job description
    text: str

class MatchResultSchema(BaseModel):
    # TODO: Define fields for match response
    candidate_id: str
    score: float
