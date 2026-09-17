from fastapi import APIRouter
from .routes_resumes import router as resumes_router
from .routes_jobs import router as jobs_router
from .routes_match import router as match_router

api_router = APIRouter()
api_router.include_router(resumes_router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(match_router, prefix="/match", tags=["Match"])
