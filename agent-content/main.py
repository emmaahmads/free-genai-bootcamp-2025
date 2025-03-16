from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from agent import YouTubeTranscriptAgent

app = FastAPI(title="YouTube Transcript Retrieval API")

class TranscriptRequest(BaseModel):
    message_request: str  # YouTube URL

class AlternativeVideo(BaseModel):
    url: str
    title: str

class TranscriptResponse(BaseModel):
    transcript: Optional[str] = None
    alternatives: List[AlternativeVideo] = []

@app.post("/api/agent", response_model=TranscriptResponse)
async def get_transcript(request: TranscriptRequest):
    """
    Endpoint to retrieve a transcript from a YouTube video.
    
    If the video is not in Malay or doesn't have a transcript,
    alternative videos will be suggested.
    """
    try:
        agent = YouTubeTranscriptAgent()
        result = await agent.run(request.message_request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/")
async def root():
    return {"message": "YouTube Transcript Retrieval API. Use /api/agent endpoint to get transcripts."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
