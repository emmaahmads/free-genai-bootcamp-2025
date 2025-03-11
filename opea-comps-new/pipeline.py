import requests
import json

NGINX_URL = "http://opea-nginx-server"
WHISPER_URL = f"{NGINX_URL}/asr"
VLLM_URL = f"{NGINX_URL}/vllm"
TTS_URL = f"{NGINX_URL}/tts"

def transcribe_audio(audio_file_path):
    """ Sends audio to Whisper ASR and gets transcribed text. """
    with open(audio_file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(WHISPER_URL, files=files)

    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        print(f"ASR Error: {response.text}")
        return None

def generate_response(text):
    """ Sends transcribed text to vLLM for processing. """
    payload = {"prompt": text}
    headers = {"Content-Type": "application/json"}
    response = requests.post(VLLM_URL, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        return response.json().get("generated_text", "")
    else:
        print(f"vLLM Error: {response.text}")
        return None

def synthesize_speech(text):
    """ Sends generated text to TTS for speech synthesis. """
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    response = requests.post(TTS_URL, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        return response.content  # Assuming TTS returns audio data
    else:
        print(f"TTS Error: {response.text}")
        return None

def main(audio_file_path):
    print("Starting ASR → vLLM → TTS pipeline...")

    # Step 1: Transcribe audio
    transcribed_text = transcribe_audio(audio_file_path)
    if not transcribed_text:
        print("Failed at ASR step.")
        return

    print(f"ASR Output: {transcribed_text}")

    # Step 2: Generate response with vLLM
    generated_text = generate_response(transcribed_text)
    if not generated_text:
        print("Failed at vLLM step.")
        return

    print(f"vLLM Output: {generated_text}")

    # Step 3: Convert response to speech using TTS
    speech_output = synthesize_speech(generated_text)
    if not speech_output:
        print("Failed at TTS step.")
        return

    # Save the audio file
    output_audio_path = "output.wav"
    with open(output_audio_path, "wb") as f:
        f.write(speech_output)

    print(f"Speech synthesis complete. Output saved to {output_audio_path}")

if __name__ == "__main__":
    audio_file = "input.wav"  # Replace with the actual file path
    main(audio_file)
