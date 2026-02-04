import requests
import json

import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("api_key")

# url = "https://ai.hackclub.com/proxy/v1/replicate/models/resemble-ai/chatterbox-pro/predictions"
url = "https://ai.hackclub.com/proxy/v1/replicate/models/minimax/speech-02-turbo/predictions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "wait"
}

# payload = {
#     "input": {
#         "pitch": "medium",
#         "voice": "Josh", # josh?
#         "prompt": "This is a tactic! A goddamn psychological attack!",
#         "temperature": 0.3,
#         "exaggeration": 1
#     }
# }

payload = {
    "input": {
        "text": "This is a tactic! A goddamn psychological attack!",
        "emotion": "angry",
        "voice_id": "English_Debator",
        "language_boost": "English",
        "english_normalization": True,
#        "pitch": -1
    }
}



# Send request
response = requests.post(url, headers=headers, data=json.dumps(payload))
response.raise_for_status()

result = response.json()
print("Prediction result:", result)

# Extract output URL
output_url = result.get("output")
print("Output URL:", output_url)

# Download audio file
if output_url:
    audio_data = requests.get(output_url).content
    with open("output.mp3", "wb") as f:
        f.write(audio_data)
    print("Saved output.mp3")
else:
    print("No output URL found in response.")
