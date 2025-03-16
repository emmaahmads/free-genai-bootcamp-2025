# YouTube Transcript Retrieval Agent

A FastAPI application that uses a ReACT agent to retrieve transcripts from YouTube videos in Malay language for language learning purposes.

## Business Goal

This application helps users get transcriptions of YouTube videos that are:
1. In the Malay language
2. Appropriate for language learning settings

If a video doesn't have an embedded transcript or doesn't meet the criteria, the agent will suggest alternative videos with similar content that do have transcriptions.

## Technical Stack

- FastAPI - Web framework for building the API
- Ollama (Mistral 7B) - LLM for the agent's reasoning
- Instructor - For structured JSON output from the LLM
- SQLite3 - For database storage
- YouTube Data API - For interacting with YouTube

## Project Structure

```
agent-content/
├── agent-prompt-test.md     # The ReACT agent prompt
├── agent.py            # Agent implementation
├── main.py             # FastAPI application
├── requirements.txt    # Dependencies
├── tech-specs.md       # Technical specifications
└── tools/              # Agent tools
    ├── get_content.py  # Tool to analyze video content
    ├── get_transcript.py  # Tool to retrieve video transcripts
    └── search_videos.py  # Tool to search for alternative videos
```

## Setup and Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure you have Ollama installed and the Mistral 7B model pulled:
   ```
   ollama pull mistral:7b
   ```

3. Run the application:
   ```
   python main.py
   ```

## API Endpoints

### POST /api/agent

Retrieves a transcript from a YouTube video or suggests alternatives.

#### Request Body

```json
{
  "message_request": "https://www.youtube.com/watch?v=example123"
}
```

#### Response

```json
{
  "transcript": "The full transcript text if available",
  "alternatives": [
    {
      "url": "https://youtube.com/watch?v=id1",
      "title": "Video title 1"
    },
    {
      "url": "https://youtube.com/watch?v=id2",
      "title": "Video title 2"
    }
  ]
}
```

## Notes

- This implementation includes simulated responses for the YouTube API calls
- In a production environment, you would need to use actual YouTube API credentials
- The agent verifies that videos are in Malay and appropriate for language learning before retrieving transcripts
