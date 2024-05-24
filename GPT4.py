import os
import requests
import base64

# Get environment variables
GPT4V_KEY = os.getenv("GPT4V_KEY")
IMAGE_PATH = './example.png'

# Check if variables are loaded correctly
if not GPT4V_KEY or not IMAGE_PATH:
    raise ValueError("API key or image path is missing in the environment variables")

# Encode the image to base64
encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

# Set headers for the request
headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

# Prepare the payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are an AI assistant that helps people find information."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encoded_image}"
          }
        },
        {
          "type": "text",
          "text": "Describe this screenshot."
        }
      ]
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800
}

# Set the endpoint for the API request
GPT4V_ENDPOINT = "https://yuantsy-westus.openai.azure.com/openai/deployments/Chat-preview-west-us/chat/completions?api-version=2024-02-15-preview"

# Send the request and handle the response
try:
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    # Handle the response as needed (e.g., print or process)
    print(response.json())
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")
