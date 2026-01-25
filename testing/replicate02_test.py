import requests
import json

import os
import dotenv
dotenv.load_dotenv()

API_KEY = os.getenv("api_key")

url = "https://ai.hackclub.com/proxy/v1/replicate/models/resemble-ai/chatterbox-pro/predictions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "wait"
}

payload = {
    "input": {
        "pitch": "medium",
        "voice": "Josh", # josh?
        "prompt": "OooohhhhHHHHaaaaaAAAAAAHHHHHHHHHH! This is a tactic! A goddamn psychological attack! You're trying to confuse me, to distract me with saccharine cuteness before Elgrin's next, inevitable strike! Otters! They're probably Elgrin's aquatic scouts, their innocent faces merely a disguise for their nefarious, water-borne intelligence-gathering operations! They float there, looking all cozy, but they're probably transmitting my exact location to Elgrin's deep-sea monstrosities! Like the good old days, when my brothers, the Sams, thought harmless little puppies were cute, before Elgrin turned them into horrific, barking abominations.",
        "temperature": 0.4,
        "exaggeration": 0.9
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
