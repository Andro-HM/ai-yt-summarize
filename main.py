from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.summarize import router as summarize_router

app = FastAPI(
    title="YouTube Summarizer API",
    description="API for summarizing YouTube videos using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summarize_router)

@app.get("/")
def root():
    return {
        "message": "YouTube Summarizer API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/summarize": "Summarize a YouTube video"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
