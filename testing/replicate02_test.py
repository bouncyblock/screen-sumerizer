import requests
import json

import os
import dotenv
dotenv.load_dotenv()

API_KEY = os.getenv("api_key")

url = "https://ai.hackclub.com/proxy/v1/replicate/models/minimax/speech-02-turbo/predictions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "wait"
}

payload = {
    "input": {
        "text": (
            "Speech-02-series is a Text-to-Audio and voice cloning technology that offers "
            "voice synthesis, emotional expression, and multilingual capabilities.\n\n"
            "The HD version is optimized for high-fidelity applications like voiceovers and audiobooks. "
            "While the turbo one is designed for real-time applications with low latency.\n\n"
            "When using this model on Replicate, each character represents 1 token."
        ),
        "emotion": "angry",
        "voice_id": "Deep_Voice_Man",
        "language_boost": "English",
        "english_normalization": True
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
