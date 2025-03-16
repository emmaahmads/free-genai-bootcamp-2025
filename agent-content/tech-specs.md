# Tech Specs

## Business Goal
We want to create a program that will get the transcription of a youtube video from a URL. The video must be verified to be in Malay and is appropriate for a language learning setting. If the video does not have an embedded transcript, we want to give suggestions for alternative videos that are of similar contents and have the transcription. We want to use an agent to handle this task. 

## Technical Requirements

- FastAPI
- Ollama via the Ollama Python SDK
    - Mistral 7B
- Instructor (for structured json output)
- SQLite3 (for database)
- Youtube Data API

## API Endpoints

### GetTranscript POST /api/agent 

### Behaviour

This endpoint goes to our agent which is uses the reAct framework
so that it can go to Youtube, check the content of the Youtube link and retireve the transcript and return the transcript in a text file. If either the content is not suitable, or the video does not have a transcript, the agent will search for alternative videos that are of similar contents and have the transcription. 

Tools avaliable:
- tools/get_transcript.py
- tools/get_content.py
- tools/search_videos.py

### JSON Request Parameters
- `message_request` (str): A string that contains the URL of the youtube video

### JSON Response
- `transcript` (str): The transcript of the video
- `alternatives` (list): A list of alternative videos that have the transcript