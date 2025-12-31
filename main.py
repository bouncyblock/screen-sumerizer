from dotenv import load_dotenv
from openrouter import OpenRouter
import requests
import base64
import os
import os.path

load_dotenv()

'''
client = OpenRouter(
    api_key = os.getenv('api_key'),
    server_url="https://ai.hackclub.com/proxy/v1",
)


response = client.chat.send(
    model="qwen/qwen3-32b",
    messages=[
        {"role": "user", "content": "Tell me a joke."}
    ],
    stream=False,
)

print(response.choices[0].message.content)
'''


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

image_data = encode_image("grass.jpg")

response = requests.post(
    "https://ai.hackclub.com/proxy/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.getenv('api_key')}",
        "Content-Type": "application/json"
    },
    json={
        "model": "google/gemini-2.5-flash",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                }
            ]
        }]
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}")