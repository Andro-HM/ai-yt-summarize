from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
from utils.youtube import extract_video_id
from services.transcript_service import get_youtube_transcript
from services.ai_service import summarize_with_chunks, chunk_text, get_gemini_summary

router = APIRouter()

class SummaryRequest(BaseModel):
    url: str
    language: str = "en"
    mode: str = "video"
    aiModel: str = "gemini"

async def stream_summary(request: SummaryRequest):
    try:
        # Extract video ID
        video_id = extract_video_id(request.url)
        yield json.dumps({"type": "progress", "stage": "analyzing", "message": "Extracting video ID..."}) + "\n"
        await asyncio.sleep(0.1)

        # Get transcript
        yield json.dumps({"type": "progress", "stage": "analyzing", "message": "Fetching transcript..."}) + "\n"
        transcript_data = get_youtube_transcript(video_id)

        # Chunk text
        chunks = chunk_text(transcript_data["transcript"])
        total_chunks = len(chunks)

        # Process chunks with streaming
        from services.ai_service import get_openrouter_summary_stream, get_openrouter_summary

        yield json.dumps({
            "type": "progress",
            "stage": "processing",
            "message": f"Generating summary with streaming..."
        }) + "\n"

        # For simplicity, stream only the final summary (not intermediate chunks)
        if request.aiModel == "openrouter":
            # Stream the text generation word by word
            yield json.dumps({"type": "stream_start"}) + "\n"

            for text_chunk in get_openrouter_summary_stream(transcript_data["transcript"], request.language):
                # Send each word/phrase as it's generated
                yield json.dumps({"type": "stream_chunk", "content": text_chunk}) + "\n"

            yield json.dumps({"type": "stream_end"}) + "\n"
        else:
            # Gemini doesn't stream (for now)
            summary = get_gemini_summary(transcript_data["transcript"], request.language)
            yield json.dumps({
                "type": "complete",
                "summary": summary,
                "source": transcript_data["source"],
                "videoId": video_id,
                "status": "completed"
            }) + "\n"
            return

        # Complete
        yield json.dumps({
            "type": "complete",
            "source": transcript_data["source"],
            "videoId": video_id,
            "status": "completed"
        }) + "\n"

    except Exception as e:
        yield json.dumps({"type": "error", "error": str(e)}) + "\n"

@router.post("/api/summarize")
async def summarize(request: SummaryRequest):
    return StreamingResponse(stream_summary(request), media_type="text/event-stream")
