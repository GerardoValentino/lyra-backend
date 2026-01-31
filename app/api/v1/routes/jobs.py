from fastapi import (
    APIRouter,
    HTTPException, 
    status
)

from app.api.v1.jobs import analysis_jobs

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/song-analysis/{job_id}")
async def get_analysis_status(job_id: str):
    job = analysis_jobs.get(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job no encontrado"
        )

    return job