"""
Resume Endpoints
Assigned to: Backend Team
"""

from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    TODO: Implement resume upload and extraction:
    - Read file bytes (PDF / DOCX / TXT)
    - Pass to parser_service
    - Store parsed data in database
    """
    return {"message": f"Received {len(files)} file(s) - parsing to be implemented by Backend Team"}
