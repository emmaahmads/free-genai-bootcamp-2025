import re
import aiohttp
from typing import Dict, Any, Tuple
from openai import OpenAI
import instructor

client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON,
)

async def get_content(url: str) -> str:
    """
    Analyzes the content of a YouTube video to determine if it's in Malay
    and appropriate for language learning.
    
    Args:
        url: The URL of the YouTube video
        
    Returns:
        A string describing whether the video is in Malay and appropriate
    """
    # Extract video ID from URL
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if not video_id_match:
        return "Error: Invalid YouTube URL format"
    
    video_id = video_id_match.group(1)
    
    # Fetch video metadata using YouTube Data API
    try:
        async with aiohttp.ClientSession() as session:
            # In a real implementation, you would use the YouTube Data API with an API key
            # For this example, we'll simulate the API response
            # async with session.get(f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet&key={API_KEY}") as response:
            #     data = await response.json()
            
            # Simulate API response for demonstration
            data = await _simulate_youtube_api_response(video_id)
            
            # Extract video title and description
            if "items" in data and len(data["items"]) > 0:
                title = data["items"][0]["snippet"]["title"]
                description = data["items"][0]["snippet"]["description"]
                
                # Use LLM to analyze if content is in Malay and appropriate for language learning
                is_malay, is_appropriate = await _analyze_content(title, description)
                
                if is_malay and is_appropriate:
                    return "The video is in Malay and the content is appropriate for language learning."
                elif not is_malay:
                    return "The video is not in Malay language."
                else:
                    return "The video is in Malay but the content is not appropriate for language learning."
            else:
                return "Error: Could not retrieve video metadata"
    except Exception as e:
        return f"Error analyzing video content: {str(e)}"

async def _simulate_youtube_api_response(video_id: str) -> Dict[str, Any]:
    """
    Simulates a response from the YouTube Data API.
    In a real implementation, this would be replaced with actual API calls.
    
    Args:
        video_id: The YouTube video ID
        
    Returns:
        A dictionary mimicking the YouTube API response
    """
    # This is a simplified mock response
    # In a real implementation, you would get this data from the YouTube API
    return {
        "items": [
            {
                "id": video_id,
                "snippet": {
                    "title": "Belajar Bahasa Melayu - Perbualan Asas",
                    "description": "Video pembelajaran bahasa Melayu untuk pemula. Mempelajari frasa-frasa asas dan perbualan harian dalam bahasa Melayu.",
                    "channelTitle": "Malay Language Learning",
                    "publishedAt": "2023-01-15T12:00:00Z"
                }
            }
        ]
    }

async def _analyze_content(title: str, description: str) -> Tuple[bool, bool]:
    """
    Uses an LLM to analyze if the content is in Malay and appropriate for language learning.
    
    Args:
        title: The video title
        description: The video description
        
    Returns:
        A tuple of (is_malay, is_appropriate)
    """
    prompt = f"""
    Analyze the following YouTube video title and description:
    
    Title: {title}
    Description: {description}
    
    Task 1: Determine if this content is in the Malay language.
    Task 2: Determine if this content is appropriate for language learning settings.
    
    Return your analysis as a JSON with two boolean fields: is_malay and is_appropriate.
    """
    
    response = client.chat.completions.create(
        model="mistral:7b",
        messages=[{"role": "user", "content": prompt}],
        response_model={
            "is_malay": bool,
            "is_appropriate": bool
        }
    )
    
    return response.is_malay, response.is_appropriate