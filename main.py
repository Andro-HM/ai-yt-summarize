from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from utils.youtube import extract_video_id
from services.transcript_service import get_youtube_transcript
from services.ai_service import get_gemini_summary
from api.summarize import router as summarize_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summarize_router)

@app.get("/")
def root():
    return {"message": "YouTube Summarizer API"}

@app.get("/test")
def test():
    video_id = extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"video_id": video_id}

@app.get("/test-transcript")
def test_transcript():
    result = get_youtube_transcript("dQw4w9WgXcQ")
    return {
        "source": result["source"],
        "title": result["title"],
        "transcript_length": len(result["transcript"])
    }

@app.get("/test-ai")
def test_ai():
    sample_text = "Python is a high-level programming language. It was created by Guido van Rossum in 1991."
    summary = get_gemini_summary(sample_text, "en")
    return {"summary": summary}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
