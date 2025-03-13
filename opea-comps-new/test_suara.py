import requests
import base64
import os
import sys

def test_suara_app(audio_file_path, output_file_path="response.wav"):
    """
    Test the Suara app by sending an audio file and saving the response.
    
    Args:
        audio_file_path: Path to the audio file to send
        output_file_path: Path to save the response audio
    """
    # Check if the audio file exists
    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file {audio_file_path} not found.")
        return False
    
    try:
        # Read and encode the audio file
        with open(audio_file_path, 'rb') as f:
            audio_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Prepare the request payload
        payload = {
            "audio": audio_base64,
            "max_tokens": 128,
            "temperature": 0.01,
            "top_p": 0.95,
            "frequency_penalty": 0.0,
            "voice": "default"
        }
        
        # Define the endpoint URL
        url = "http://localhost:8888/v1/suara"
        
        print(f"Sending request to {url}...")
        print(f"Audio file size: {os.path.getsize(audio_file_path)} bytes")
        
        # Send the request
        response = requests.post(
            url, 
            json=payload,
            # Disable OpenTelemetry tracing for this request
            headers={"traceparent": "00-00000000000000000000000000000000-0000000000000000-00"}
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the response to a file
            with open(output_file_path, 'wb') as f:
                f.write(response.content)
            print(f"Success! Response saved to {output_file_path}")
            print(f"Response size: {len(response.content)} bytes")
            return True
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Use command line argument for audio file path or default to output.wav
    audio_file = sys.argv[1] if len(sys.argv) > 1 else "output.wav"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "response.wav"
    
    print(f"Testing Suara app with audio file: {audio_file}")
    test_suara_app(audio_file, output_file)