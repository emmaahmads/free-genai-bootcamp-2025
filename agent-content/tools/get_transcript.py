import re
import aiohttp
from typing import Optional, Dict, Any

async def get_transcript(url: str) -> str:
    """
    Retrieves the transcript from a YouTube video if available.
    
    Args:
        url: The URL of the YouTube video
        
    Returns:
        The transcript text if available, otherwise an error message
    """
    # Extract video ID from URL
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if not video_id_match:
        return "Error: Invalid YouTube URL format"
    
    video_id = video_id_match.group(1)
    
    # In a real implementation, you would use the YouTube Data API or a library like youtube-transcript-api
    # For this example, we'll simulate the API response
    transcript = await _get_youtube_transcript(video_id)
    
    if transcript:
        return transcript
    else:
        return "No transcript available for this video."

async def _get_youtube_transcript(video_id: str) -> Optional[str]:
    """
    Simulates retrieving a transcript from YouTube.
    In a real implementation, this would use the YouTube API or a transcript library.
    
    Args:
        video_id: The YouTube video ID
        
    Returns:
        The transcript text if available, otherwise None
    """
    # This is a simplified mock implementation
    # In a real implementation, you would use youtube-transcript-api or similar
    
    # For demonstration purposes, we'll return None for some video IDs to simulate videos without transcripts
    if video_id == "example123":
        return None
    
    # For other video IDs, return a mock transcript
    transcript_segments = [
        {"text": "Selamat datang ke kelas bahasa Melayu.", "start": 0.0, "duration": 3.5},
        {"text": "Hari ini kita akan belajar perbualan asas.", "start": 3.5, "duration": 4.0},
        {"text": "Mari kita mula dengan ucapan selamat pagi.", "start": 7.5, "duration": 3.0},
        {"text": "Selamat pagi. Apa khabar?", "start": 10.5, "duration": 2.5},
        {"text": "Khabar baik, terima kasih.", "start": 13.0, "duration": 2.0},
        {"text": "Siapa nama anda?", "start": 15.0, "duration": 1.5},
        {"text": "Nama saya Ali. Nama anda siapa?", "start": 16.5, "duration": 3.0},
        {"text": "Nama saya Maria.", "start": 19.5, "duration": 2.0},
        {"text": "Senang bertemu dengan anda.", "start": 21.5, "duration": 2.5},
        {"text": "Sama-sama. Di mana anda tinggal?", "start": 24.0, "duration": 3.0},
        {"text": "Saya tinggal di Kuala Lumpur.", "start": 27.0, "duration": 2.5},
        {"text": "Oh, saya juga tinggal di sana!", "start": 29.5, "duration": 2.5},
        {"text": "Baiklah, itu sahaja untuk hari ini.", "start": 32.0, "duration": 3.0},
        {"text": "Terima kasih kerana menonton.", "start": 35.0, "duration": 2.5},
        {"text": "Jumpa lagi!", "start": 37.5, "duration": 1.5}
    ]
    
    # Combine all text segments into a single transcript
    full_transcript = "\n".join([segment["text"] for segment in transcript_segments])
    
    return full_transcript
