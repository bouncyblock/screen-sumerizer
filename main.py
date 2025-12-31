from dotenv import load_dotenv
from openrouter import OpenRouter
from gtts import gTTS
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import pygame
import requests
import base64
import os
import os.path
import keyboard
import mss
import time
import sys


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

def slide_in(gif_file="chrono_trigger.gif", duration=800):
    global label, app
    
    # Create app if it doesn't exist
    if not app:
        app = QApplication.instance() or QApplication(sys.argv)
    
    # Reuse or create label
    if label is None:
        label = QLabel()
        label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        label.setAttribute(Qt.WA_TranslucentBackground)
    
    # --- Load GIF ---
    movie = QMovie(gif_file)
    label.setMovie(movie)
    movie.start()
    
    # --- Screen + GIF geometry ---
    screen = app.primaryScreen().geometry()
    screen_w, screen_h = screen.width(), screen.height()
    
    movie.jumpToFrame(0)
    gif_w = movie.currentImage().width()
    gif_h = movie.currentImage().height()
    
    start_x = (screen_w - gif_w) // 2
    start_y = screen_h
    end_y = screen_h - gif_h - 50
    
    start_rect = QRect(start_x, start_y, gif_w, gif_h)
    end_rect = QRect(start_x, end_y, gif_w, gif_h)
    
    label.setGeometry(start_rect)
    label.show()
    
    # --- Slide in animation ---
    anim_in = QPropertyAnimation(label, b"geometry")
    anim_in.setDuration(duration)
    anim_in.setStartValue(start_rect)
    anim_in.setEndValue(end_rect)
    anim_in.start()
    
    label.start_x = start_x
    label.gif_h = gif_h
    label.end_rect = end_rect
    
    # Process events during animation
    start_time = time.time()
    while time.time() - start_time < duration / 1000.0:
        app.processEvents()
        time.sleep(0.01)

def slide_out(duration=800):

    global label, anim_out, app
    
    if not label or not app:
        return
    
    end_rect2 = QRect(label.start_x, -label.gif_h, label.end_rect.width(), label.end_rect.height())
    
    anim_out = QPropertyAnimation(label, b"geometry")
    anim_out.setDuration(duration)
    anim_out.setStartValue(label.end_rect)
    anim_out.setEndValue(end_rect2)
    anim_out.finished.connect(lambda: label.hide())
    anim_out.start()
    
    # Process events during animation
    start_time = time.time()
    while time.time() - start_time < duration / 1000.0:
        app.processEvents()
        time.sleep(0.01)

def get_app():
    global app
    return app
# print(f"Response Text: {response.text}")


# fuck off garbage collection
label = None
anim_out = None
app = None


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
    slide_in("chrono_trigger.gif")
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
    pygame.mixer.music.unload()
    slide_out()
    #os.system("start output.mp3")  # Play the audio file
    print("Waiting for next capture...")
