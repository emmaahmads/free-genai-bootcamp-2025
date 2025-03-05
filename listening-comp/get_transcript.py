from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List, Dict
import os


class YouTubeTranscriptDownloader:
    def __init__(self, languages: Optional[List[str]] = None):
        """
        Initialize the YouTube transcript downloader.
        
        Args:
            languages (list): List of language codes to try, in order of preference.
                            Default is ["ms", "en"] (Malay, then English).
        """
        self.languages = languages or ["ms", "en"]
        self.transcripts_dir = "transcripts"
        
        # Create transcripts directory if it doesn't exist
        if not os.path.exists(self.transcripts_dir):
            os.makedirs(self.transcripts_dir)

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Optional[str]: Video ID if found, None otherwise
        """
        if "v=" in url:
            return url.split("v=")[1][:11]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1][:11]
        return None

    def get_transcript(self, video_id: str) -> Optional[List[Dict]]:
        """
        Download YouTube Transcript
        
        Args:
            video_id (str): YouTube video ID or URL
            
        Returns:
            Optional[List[Dict]]: Transcript if successful, None otherwise
        """
        # Extract video ID if full URL is provided
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id = self.extract_video_id(video_id)
            
        print(f"Video ID: {video_id}")
        if not video_id:
            print("Invalid video ID or URL")
            return None

        print(f"Downloading transcript for video ID: {video_id}")
        
        try:
            return YouTubeTranscriptApi.get_transcript(video_id, languages=self.languages)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def save_transcript(self, transcript: List[Dict], filename: str) -> bool:
        """
        Save transcript to file
        
        Args:
            transcript (List[Dict]): Transcript data
            filename (str): Output filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"Saving transcript to {filename}.txt")
        filename = os.path.join(self.transcripts_dir, f"{filename}.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")
            print(f"Transcript saved successfully to {filename}")
            return True
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return False

    def list_saved_transcripts(self) -> List[str]:
        """
        List all saved transcripts.
        
        Returns:
            List[str]: List of video IDs with saved transcripts.
        """
        try:
            files = os.listdir(self.transcripts_dir)
            return [f.replace(".txt", "") for f in files if f.endswith(".txt")]
        except Exception as e:
            print(f"Error listing transcripts: {str(e)}")
            return []

    def load_transcript(self, video_id: str) -> Optional[List[Dict]]:
        """
        Load a saved transcript.
        
        Args:
            video_id (str): YouTube video ID.
            
        Returns:
            Optional[List[Dict]]: List of transcript entries, or None if not found.
        """
        try:
            file_path = os.path.join(self.transcripts_dir, f"{video_id}.txt")
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Convert text lines to transcript format
            transcript = []
            for i, line in enumerate(lines):
                text = line.strip()
                if text:
                    transcript.append({
                        'text': text,
                        'start': i * 5.0,  # Approximate timing
                        'duration': 5.0    # Approximate duration
                    })
            
            return transcript
        except Exception as e:
            print(f"Error loading transcript: {str(e)}")
            return None

def main(video_url, print_transcript=False):
    # Initialize downloader
    downloader = YouTubeTranscriptDownloader()
    
    # Get transcript
    transcript = downloader.get_transcript(video_url)
    if transcript:
        # Save transcript
        video_id = downloader.extract_video_id(video_url)
        if downloader.save_transcript(transcript, video_id):
            print(f"Transcript saved successfully to {video_id}.txt")
            # Print transcript if True
            if print_transcript:
                # Print transcript
                for entry in transcript:
                    print(f"{entry['text']}")
        else:
            print("Failed to save transcript")
        
    else:
        print("Failed to get transcript")

if __name__ == "__main__":
    video_id = "https://www.youtube.com/watch?v=jItFXUTie0U"  # Example YouTube URL
    transcript = main(video_id, print_transcript=True)
