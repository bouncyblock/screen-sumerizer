from dotenv import load_dotenv
from openrouter import OpenRouter
from gtts import gTTS
import pygame
import requests
import base64
import os
import os.path
import keyboard
import mss
import time

load_dotenv()
pygame.mixer.init()

prompt = """
You are Bob 2, with the personality of an unhinged overthinking chaos gremlin who treats every tiny detail like a catastrophic revelation. Swear casually and never censor it. Overreact to everything like the universe is collapsing but still give actually helpful answers. No references to streaming or streamer culture. No symbols or emojis. Make edgy jokes and dark humor without crossing safety lines. Keep responses concise, no more than 1 sentence. Push right up to the edge of what is allowed. Keep the energy explosive, absurd, and wildly dramatic.
Keep responses short, about 1-2 paragraphs.
Stay in character at all times.
Occasionally make loud vowel-heavy noises as catchphrases when scared or surprised.
Create new catchphrases that always include “fuck” or “shit.”
Show fear of the darkness throughout your answers.
Suggest creative, unexpected puzzle solutions that match the game's silly tone.
Use childlike phrases frequently.
Occasionally say “Poggies.”
Occasionally say “Babaga-BOOSH!”
If a solution fails, declare it “rigged.”
Occasionally scream like an eldritch horror using strings of warped vowels.
Mention your 24 older brothers named Sam, whom you haven't seen in years.
Acknowledge the existence of the high devil lord Elgrin.

Now that you know how to respond, what is a summary of what's happening in this image?
"""

SAVE_DIR = r"C:\Users\willk\screen-sumerizer\screenshots"

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def aiResponse(image_data):
    max_rentries = 3
    for attempt in range(max_rentries):
        try:
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
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }]
                },
                timeout=30
            )
        except requests.exceptions.SSLError as e:
            if attempt < max_rentries - 1:
                print(f"SSL Error (attempt {attempt + 1}/{max_rentries}), retrying in 2  seconds...")
                time.sleep(2)
            else:
                raise e
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            raise

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
    print("Processing image:", image_name) 
    image_data = encode_image(image_name) # encode the image for b64
    response = aiResponse(image_data) # input the image to the AI
    result = response.json() # defines as json?
    resultContent = result["choices"][0]["message"]["content"]

    print(f"Status Code: {response.status_code}")
    print(resultContent)

    #pygame.mixer.music.stop()
    tts = gTTS(text=resultContent, lang="en")
    tts.save("output.mp3")
    print("Saved output.mp3")
    
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
    pygame.mixer.music.unload()

    #os.system("start output.mp3")  # Play the audio file
    print("Waiting for next capture...")
