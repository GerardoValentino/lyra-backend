from app.api.v1.jobs import analysis_jobs
from app.schemas import SongAnalyticsRequest
from .llm_service import analyze_song_lyrics
from app.socket import sio

async def run_song_analysis(
    job_id: str,
    request_data: SongAnalyticsRequest,
    api_key: str
):
    try:
        result = await analyze_song_lyrics(
            message=request_data.message,
            lyrics=request_data.song_lyrics,
            api_key=api_key
        )

        analysis_jobs[job_id] = {
            "status": "done",
            "result": result
        }

        await sio.emit(
            "analysis_done",
            {
                "job_id": job_id,
                "result": result
            },
            room=job_id
        )

    except Exception as e:
        analysis_jobs[job_id] = {
            "status": "failed",
            "error": str(e)
        }

        await sio.emit(
            "analysis_failed",
            {
                "job_id": job_id,
                "error": str(e)
            },
            room=job_id
        )