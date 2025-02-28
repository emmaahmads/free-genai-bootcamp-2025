#!/usr/bin/env python3

import requests
import json
import sys
import re

def test_learn_malay(model="deepseek-r1:1.5b", content="Hello, how are you?"):
    url = "http://localhost:9997/v1/learn-malay"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    print(f"Testing learn-malay service with model: {model}")
    print(f"Content: {content}")
    print("Sending request...")
    
    # Use stream=True to handle streaming responses
    response = requests.post(url, headers=headers, json=data, stream=True)
    
    print(f"Response status code: {response.status_code}")
    print("Response headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")
    
    print("\nResponse content:")
    
    # Process the response
    try:
        # Check if the response is JSON
        if 'application/json' in response.headers.get('content-type', ''):
            json_data = response.json()
            print("\nResponse content (JSON):")
            print(f"Translation: {json_data.get('translation', 'N/A')}")
            print(f"Explanation: {json_data.get('explanation', 'N/A')}")
            print(f"Original: {json_data.get('original', 'N/A')}")
            print(f"Model: {json_data.get('model', 'N/A')}")
        else:
            # For streaming or other response types
            print("\nResponse content:")
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    print(chunk.decode('utf-8', errors='replace'), end='', flush=True)
    except Exception as e:
        print(f"Error processing response: {e}")

if __name__ == "__main__":
    # Test with default model and message
    test_learn_malay()
    
    # Test with a different model and message
    test_learn_malay(model="llama3.2:1b", content="Good morning, nice to meet you.")
