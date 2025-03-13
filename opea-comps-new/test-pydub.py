from pydub import AudioSegment

try:
    audio = AudioSegment.from_file("fixed.wav")
    print("File loaded successfully!")
except Exception as e:
    print(f"Error: {e}")
