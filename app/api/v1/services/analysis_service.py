from fastapi import BackgroundTasks
import uuid
from app.schemas import SongAnalyticsRequest
from app.api.v1.jobs import analysis_jobs
from .analysis_tasks import run_song_analysis

def create_song_analysis_job(
    request_data: SongAnalyticsRequest,
    api_key: str,
    background_tasks: BackgroundTasks
) -> dict:
    job_id = str(uuid.uuid4())

    analysis_jobs[job_id] = {
        "status": "processing"
    }

    background_tasks.add_task(
        run_song_analysis,
        job_id,
        request_data,
        api_key
    )

    return {
        "job_id": job_id,
        "status": "processing"
    }

