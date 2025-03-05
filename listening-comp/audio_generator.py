import os
import json
import time
import logging
import subprocess
from elevenlabs.client import ElevenLabs
from typing import Dict, List, Optional
from elevenlabs import play

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class AudioGenerator:
    """
    Class to generate audio from text using ElevenLabs.
    """

    def __init__(self, output_directory: str = "audio_files"):
        """
        Initialize the AudioGenerator.

        Args:
            output_directory (str): Directory to save audio files.
        """
        self.output_directory = output_directory

        # Create output directory if it doesn't exist
        os.makedirs(self.output_directory, exist_ok=True)

        # Set ElevenLabs API key from environment variable
        api_key = os.getenv("ELEVENLABS_API_KEY")

        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=api_key)

    def generate_audio(self, text: str) -> Optional[str]:
        """
        Generate audio from text.

        Args:
            text (str): Text to convert to audio.

        Returns:
            Optional[str]: Path to the generated audio file, or None if generation failed.
        """
        filename = f"audio_{hash(text) % 10000}_{int(time.time())}.mp3"
        output_path = os.path.join(self.output_directory, filename)

        try:
            audio_content = self.client.text_to_speech.convert(
                  text=text,
                  voice_id="Xb7hH8MSUJpSbSDYk0k2",
                  model_id="eleven_multilingual_v2",
                  output_format="mp3_44100_128",
            )

            play(audio_content)

            with open(output_path, "wb") as audio_file:
                for chunk in audio_content:
                    if chunk:
                        audio_file.write(chunk)
            return output_path

        except Exception as error:
            logging.error(f"Error generating audio with ElevenLabs: {str(error)}")
            return None

    def generate_audio_with_voice(self, text: str, voice_id: str) -> Optional[str]:
        """
        Generate audio from text using a specific voice.

        Args:
            text (str): Text to convert to audio.
            voice_id (str): Voice ID to use (e.g., 'male1', 'female1').

        Returns:
            Optional[str]: Path to the generated audio file, or None if generation failed.
        """
        filename = f"audio_{hash(text) % 10000}_{voice_id}_{int(time.time())}.mp3"
        output_path = os.path.join(self.output_directory, filename)

        try:
            audio_content = self.client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
            )

            play(audio_content)

            with open(output_path, "wb") as audio_file:
                for chunk in audio_content:
                    if chunk:
                        audio_file.write(chunk)
            return output_path

        except Exception as error:
            logging.error(f"Error generating audio with ElevenLabs: {str(error)}")
            return None

    def generate_audio_from_transcript(self, transcript: List[Dict]) -> Optional[str]:
        """
        Generate audio from a YouTube transcript.

        Args:
            transcript (List[Dict]): List of transcript entries.

        Returns:
            Optional[str]: Path to the generated audio file, or None if generation failed.
        """
        text_content = " ".join(entry["text"] for entry in transcript)
        return self.generate_audio(text_content)

    def generate_audio_from_transcript_with_voice(self, transcript: List[Dict], voice_id: str) -> Optional[str]:
        """
        Generate audio from a YouTube transcript using a specific voice.

        Args:
            transcript (List[Dict]): List of transcript entries.
            voice_id (str): Voice ID to use (e.g., 'male1', 'female1').

        Returns:
            Optional[str]: Path to the generated audio file, or None if generation failed.
        """
        text_content = " ".join(entry["text"] for entry in transcript)
        return self.generate_audio_with_voice(text_content, voice_id)

    def concatenate_audio_files(self, audio_file_paths: List[str]) -> Optional[str]:
        """
        Concatenate multiple audio files into one.

        Args:
            audio_file_paths (List[str]): List of audio file paths.

        Returns:
            Optional[str]: Path to the concatenated audio file, or None if concatenation failed.
        """
        if not audio_file_paths:
            logging.error("No audio files to concatenate")
            return None

        if len(audio_file_paths) == 1:
            return audio_file_paths[0]

        output_filename = f"concatenated_{int(time.time())}.mp3"
        output_path = os.path.join(self.output_directory, output_filename)

        try:
            file_list = "|".join(audio_file_paths)
            command = f"ffmpeg -i \"concat:{file_list}\" -c copy {output_path}"

            subprocess.run(command, shell=True, check=True)
            return output_path

        except subprocess.CalledProcessError as error:
            logging.error(f"Error concatenating audio files: {str(error)}")
            return None
        except Exception as error:
            logging.error(f"Unexpected error concatenating audio files: {str(error)}")
            return None
