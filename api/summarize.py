from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.youtube import extract_video_id
from services.transcript_service import get_youtube_transcript
from services.ai_service import get_gemini_summary

router = APIRouter()

class SummaryRequest(BaseModel):
    url: str
    language: str = "en"
    mode: str = "video"
    aiModel: str = "gemini"

@router.post("/api/summarize")
async def summarize(request: SummaryRequest):
    try:
        # Extract video ID
        video_id = extract_video_id(request.url)

        # Get transcript
        transcript_data = get_youtube_transcript(video_id)

        # Generate summary
        summary = get_gemini_summary(transcript_data["transcript"], request.language)

        return {
            "summary": summary,
            "source": transcript_data["source"],
            "videoId": video_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
