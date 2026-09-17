"""
Job Description Endpoints
Assigned to: Backend Team
"""

from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze")
async def analyze_job_description(request_data: dict):
    """
    TODO: Implement job description parsing:
    - Extract required vs preferred skills
    - Extract minimum years of experience
    - Detect education/degree requirements
    """
    return {"message": "Job description analysis endpoint - to be implemented by Backend Team"}
