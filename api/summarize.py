from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.youtube import extract_video_id
from services.transcript_service import get_youtube_transcript
from services.ai_service import get_openrouter_summary

router = APIRouter()

class SummaryRequest(BaseModel):
    url: str
    language: str = "en"

@router.post("/api/summarize")
async def summarize(request: SummaryRequest):
    try:
        # Extract video ID
        video_id = extract_video_id(request.url)

        # Get transcript
        transcript_data = get_youtube_transcript(video_id, request.language)

        # Generate summary using OpenRouter
        summary = get_openrouter_summary(transcript_data["transcript"], request.language)

        return {
            "success": True,
            "summary": summary,
            "source": transcript_data["source"],
            "videoId": video_id,
            "language": transcript_data.get("language", request.language)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
