import re
import aiohttp
from typing import Optional, Dict, Any
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable

async def get_transcript(url: str) -> str:
    """
    Retrieves the transcript from a YouTube video if available.
    
    Args:
        url: The URL of the YouTube video
        
    Returns:
        The transcript text if available, otherwise an error message
    """
    print(f"Retrieving transcript for YouTube URL: {url}")
    
    # Extract video ID from URL
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if not video_id_match:
        print("Error: Invalid YouTube URL format")
        return "Error: Invalid YouTube URL format"
    
    video_id = video_id_match.group(1)
    
    print(f"Video ID: {video_id}")
    
    # In a real implementation, you would use the YouTube Data API or a library like youtube-transcript-api
    # For this example, we'll simulate the API response
    transcript = await _get_youtube_transcript(video_id)
    
    if transcript:
        print("Transcript available")
        return transcript
    else:
        print("No transcript available for this video")
        return "No transcript available for this video."

async def _get_youtube_transcript(video_id: str) -> Optional[str]:
    async def _get_youtube_transcript(video_id: str) -> Optional[str]:
        """
        Retrieves a transcript from a YouTube video using youtube-transcript-api.
        
        Args:
            video_id (str): The YouTube video ID.
            
        Returns:
            Optional[str]: The transcript text if available, otherwise None.
        """
    try:
        # Fetch the transcript using the youtube-transcript-api
        transcript_segments = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text segments into a single transcript
        full_transcript = "\n".join([segment["text"] for segment in transcript_segments])
        
        return full_transcript
    
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for video ID: {video_id}")
        return None
    except VideoUnavailable:
        print(f"Video is unavailable for video ID: {video_id}")
        return None
    except Exception as e:
        print(f"An error occurred while retrieving the transcript for video ID {video_id}: {e}")
        return None