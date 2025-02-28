#!/usr/bin/env python3

import requests
import json
import sys

def test_learn_malay(model="deepseek-r1:1.5b", content="Hello, how are you? Can you speak Malay?"):
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
    
    print("\nRaw response content (first 1000 bytes):")
    # Print the raw response content
    raw_content = b""
    for chunk in response.iter_content(chunk_size=None):
        raw_content += chunk
        if len(raw_content) > 1000:
            break
    
    print(f"Raw content (hex): {raw_content.hex()}")
    print(f"Raw content (utf-8): {raw_content.decode('utf-8', errors='replace')}")
    print("\n")

if __name__ == "__main__":
    # Test with default model and message
    test_learn_malay()
