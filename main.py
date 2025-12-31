from dotenv import load_dotenv
from openrouter import OpenRouter
import requests
import base64
import os
import os.path
import keyboard
import mss
import time

load_dotenv()

SAVE_DIR = r"C:\Users\willk\screen-sumerizer\screenshots"


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def aiResponse(image_data):
    return requests.post(
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

def capture(monitor=1):
    with mss.mss() as sct:
        filename = os.path.join(SAVE_DIR, f"{int(time.time())}.png")
        sct.shot(mon = monitor,output=filename)
        print("Captured:", filename)
        return filename


# print(f"Response Text: {response.text}")

print("which monitor to capture?")
userMonitor = int(input())

while True:
    time.sleep(10) # wait 5 seconds
    image_name = capture(userMonitor) # capture the screen
    print("Processing image:", f"C:\\Users\\willk\\screen-sumerizer\\screenshots\\{image_name}") 
    image_data = encode_image(f"{image_name}") # encode the image for b64
    response = aiResponse(image_data) # input the image to the AI
    result = response.json() # defines as json?

    print(f"Status Code: {response.status_code}")
    print(result["choices"][0]["message"]["content"])
