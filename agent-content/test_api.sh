#!/bin/bash

# Test the YouTube Transcript Retrieval API
# This script sends a request to the /api/agent endpoint

# Set the API endpoint URL
API_URL="http://localhost:8000/api/agent"

# Example YouTube URL to test
YOUTUBE_URL="https://www.youtube.com/watch?v=WjsjzuCU8Ns"

# Create a JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "message_request": "$YOUTUBE_URL"
}
EOF
)

# Print the request details
echo "Sending request to: $API_URL"
echo "Payload:"
echo "$JSON_PAYLOAD"
echo ""
echo "Response:"

# Send the request using curl
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD" \
  | python -m json.tool

# Note: The python -m json.tool part formats the JSON response
# If you prefer using jq (if installed): | jq '.'