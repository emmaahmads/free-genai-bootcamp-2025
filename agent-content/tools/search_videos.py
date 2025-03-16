import re
import aiohttp
from typing import List, Dict, Any

async def search_videos(query: str, transcript_required: bool = True) -> str:
    """
    Searches for alternative YouTube videos with similar content that have transcriptions.
    
    Args:
        query: The search query
        transcript_required: Whether to only return videos with transcripts
        
    Returns:
        A string containing a list of alternative videos
    """
    # In a real implementation, you would use the YouTube Data API
    # For this example, we'll simulate the API response
    search_results = await _simulate_youtube_search(query, transcript_required)
    
    if not search_results:
        return "No alternative videos found."
    
    # Format the results
    result_str = "Found {} alternative videos with transcripts:\n".format(len(search_results))
    for i, video in enumerate(search_results, 1):
        result_str += f"{i}. {video['url']} - \"{video['title']}\"\n"
    
    return result_str

async def _simulate_youtube_search(query: str, transcript_required: bool) -> List[Dict[str, str]]:
    """
    Simulates a YouTube search.
    In a real implementation, this would use the YouTube API.
    
    Args:
        query: The search query
        transcript_required: Whether to only return videos with transcripts
        
    Returns:
        A list of dictionaries containing video information
    """
    # This is a simplified mock implementation
    # In a real implementation, you would use the YouTube Data API
    
    # Generate some mock search results based on the query
    # For demonstration purposes, we'll return different results based on the query
    
    # Extract keywords from the query
    keywords = query.lower().split()
    
    # Base mock results
    mock_results = [
        {
            "id": "alt1",
            "title": "Malay Learning: Basic Conversations",
            "url": "https://www.youtube.com/watch?v=alt1",
            "has_transcript": True
        },
        {
            "id": "alt2",
            "title": "Basic Malay Phrases for Beginners",
            "url": "https://www.youtube.com/watch?v=alt2",
            "has_transcript": True
        },
        {
            "id": "alt3",
            "title": "Malay Conversation Practice",
            "url": "https://www.youtube.com/watch?v=alt3",
            "has_transcript": True
        },
        {
            "id": "alt4",
            "title": "Learn Malay: Everyday Vocabulary",
            "url": "https://www.youtube.com/watch?v=alt4",
            "has_transcript": False
        },
        {
            "id": "alt5",
            "title": "Malay for Tourists: Essential Phrases",
            "url": "https://www.youtube.com/watch?v=alt5",
            "has_transcript": True
        }
    ]
    
    # Filter results based on transcript requirement
    if transcript_required:
        mock_results = [video for video in mock_results if video["has_transcript"]]
    
    # Return only the relevant fields
    return [{"url": video["url"], "title": video["title"]} for video in mock_results[:3]]
