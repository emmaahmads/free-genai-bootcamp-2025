# OPEA Megaservice

## Project Overview

OPEA (Open Platform Enterprise AI) is a modular, microservice-based AI system designed to integrate multiple AI capabilities into a cohesive platform. This implementation focuses on speech-to-text, language processing, and text-to-speech services working together to create a conversational AI experience in Malay language.

## Architecture
![OPEA Megaservice](../listening-comp/opea-audio.jpg)

The system follows a microservice architecture with the following components:

### Core Services

1. **Whisper Service** (ASR - Automatic Speech Recognition)
   - Converts audio input to text
   - Runs on port 7066
   - Uses OpenAI's Whisper model for speech recognition

2. **Ollama Server** (LLM - Large Language Model)
   - Processes text input and generates responses
   - Runs on port 11434
   - Default model: Mistral 7B Instruct

3. **SpeechT5 Service** (TTS - Text-to-Speech)
   - Converts text responses to speech
   - Runs on port 7055
   - Optimized for Malay language output

### Orchestration

- **Service Orchestrator**: Manages the flow of data between microservices
- **SuaraApp**: Main application that coordinates the entire pipeline

## Current Status

The megaservice app called SuaraApp is in functional state and the project is to have the following features implemented:

- Audio input processing via Whisper
- Text processing via Ollama LLM
- Text-to-speech conversion via SpeechT5
- NGINX reverse proxy for service communication (optional)
- Docker containerization for all services

### Work in Progress

- Streaming responses from LLM to TTS
- Fine-tuning models for better Malay language support
- Performance optimization for production deployment

## Getting Started

### Prerequisites

- Docker and Docker Compose
- At least 8GB RAM for running all services
- Internet connection for initial model downloads

### Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/emmaahmads/free-genai-bootcamp-2025.git
   cd free-genai-bootcamp-2025/opea-comps-new
   ```

2. Create a `.env` file with the following variables (or use the existing one):
   ```
   HF_TOKEN=your_huggingface_token
   TAG=latest
   ```

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. The services will be available at:
   - Main API: http://localhost:8080
   - Whisper ASR: http://localhost:7066
   - Ollama LLM: http://localhost:11434
   - SpeechT5 TTS: http://localhost:7055

## Usage

The system accepts audio input and returns audio output. You can interact with it using:

```bash
curl -X POST http://localhost:8888/v1/suara \
  -H "Content-Type: application/json" \
  -d '{
    "audio": "base64_encoded_audio",
    "max_tokens": 128,
    "temperature": 0.01,
    "voice": "default"
  }'
```

## Development

To modify or extend the system:

1. Update service configurations in `docker-compose.yml`
2. Modify the orchestration logic in `suaraapp.py`
