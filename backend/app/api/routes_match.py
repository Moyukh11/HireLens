"""
Matching & Scoring Endpoints
Assigned to: Backend Team
"""

from fastapi import APIRouter

router = APIRouter()

@router.post("")
async def match_candidates(request_data: dict):
    """
    TODO: Implement matching endpoint:
    - Receive candidate IDs/data and job criteria
    - Call ml_service to compute scores
    - Return ranked list with explainability breakdown
    """
    return {"message": "Candidate matching endpoint - to be implemented by Backend Team"}
