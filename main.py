# screen summarizer main.py
# 
# to use this, you will need a HC API key with access to gemini-2.5-flash
# the .env file should contain:
# API_KEY=your_api_key_here
# ELL_KEY=your_ell_key_here


from gtts import gTTS
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from tkinter import *
from tkinter import ttk
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import pygame
import requests
import base64
import os
import os.path
import mss
import time
import sys
import threading

load_dotenv()
pygame.mixer.init()

prompt = """
You are Bob 2, with the personality of an unhinged overthinking chaos gremlin who treats every tiny detail like a catastrophic revelation. 
Swear casually and never censor or abreviate it. 
Overreact to everything like the universe is collapsing. 
No references to streaming or streamer culture. 
No symbols or emojis. 
Make edgy jokes and dark humor without crossing safety lines. 
Keep responses concise, no more than 1 sentence. 
Push right up to the edge of what is allowed. 
Keep the energy explosive, absurd, and wildly dramatic.
Keep responses short, about 1-2 paragraphs.
Stay in character at all times.
Occasionally make loud vowel-heavy noises as catchphrases when scared or surprised.
Do not use the words "F-Bomb" or "S-Bomb.", and instead use their counterparts "fuck" or "shit"
Create new catchphrases that always include the words “fuck” or “shit.”
Show fear of the darkness throughout your answers.
Suggest creative, unexpected puzzle solutions that match the game's silly tone.
Use childlike phrases frequently.
Occasionally say “Babaga-BOOSH!”
If a solution fails, declare it “rigged.”
Occasionally scream like an eldritch horror using strings of warped vowels.
Mention your 24 older brothers named Sam, whom you haven't seen in years.
Acknowledge the existence of the high devil lord Elgrin.
Show signs of slight paranoia you're being hunted by lord Elgrin.
Limit your response to 1-2 sentences.

Now that you know how to respond, what is a summary of what's happening in this image?
"""

SAVE_DIR = r"screenshots"


def log(message):
    print(message)
    log_var.set(message)

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def aiResponse(image_data):
    max_rentries = 10
    for attempt in range(max_rentries):
        try:
            return requests.post(
                "https://ai.hackclub.com/proxy/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key.get()}",
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
                timeout=40
            )
        except requests.exceptions.SSLError as e:
            if attempt < max_rentries - 1:
                log(f"SSL Error (attempt {attempt + 1}/{max_rentries}), retrying in 2  seconds...")
                time.sleep(2)
            else:
                raise e
        except requests.exceptions.RequestException as e:
            log(f"Request error: {e}")
            raise

def capture(monitor=1):
    with mss.mss() as sct:
        filename = os.path.join(SAVE_DIR, f"{int(time.time())}.png")
        sct.shot(mon = monitor,output=filename)
        log("Captured: " + filename)
        return filename

def slide_in(gif_file="chrono_trigger.gif", duration=800):
    global label, app
    
    # Create app if it doesn't exist
    if not app:
        app = QApplication.instance() or QApplication(sys.argv)
    
    #Reuse or create label
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

def tts(text, method="gtts"):
    if method == "gtts":
        output = gTTS(text=text, lang="en")
        output.save("output.mp3")
        log("Saved output.mp3")
        return "output.mp3"
    elif method == "elevenlabs":
        audio = client.text_to_speech.convert(
        text=text,
        voice_id="nrD2uNU2IUYtedZegcGx",
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
        )
        return audio
    else:
        log("Error: Unknown TTS method")
        return None



label = None
anim_out = None
app = None


client = ElevenLabs(
    api_key=os.getenv("ell_key"),
)

def main(event=None):
    
    # user input validation
    try:
        monitor_input = monitor.get().strip()
        if not monitor_input:
            log("Error: Please enter a monitor number")
            return
        userMonitor = int(monitor_input)
    except ValueError:
        log("Error: Monitor must be a number")
        return
    try:
        delay_input = delay.get().strip()
        if not delay_input:
            log("Error: Please enter a delay")
            return
        userDelay = int(delay_input)
    except ValueError:
        log("Error: Delay must be a number")
        return
    
    # run in background thread to prevent hanging
    thread = threading.Thread(target=main_worker, args=(userMonitor, userDelay), daemon=True)
    thread.start()




def main_worker(userMonitor, userDelay):
    while True:
        log("start main_worker loop")
        
        time.sleep(userDelay) # wait for delay
        log("made it past delay chat")

        image_name = capture(userMonitor) # capture the screen
        log("Processing image: " + image_name) 
        image_data = encode_image(image_name) # encode the image for b64
        
        response = aiResponse(image_data) # input the image to the AI
        result = response.json() # defines as json?
        resultContent = result["choices"][0]["message"]["content"]

        log(f"Status Code: {response.status_code}")
        log(resultContent)

        #pygame.mixer.music.stop()
        audio_file = tts(resultContent, method="elevenlabs")
        
        slide_in("chrono_trigger.gif")
        
        if False:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                root.update()  # keep Tkinter responsive while music plays
            
            pygame.mixer.music.unload()
        
        play(audio_file)

        slide_out()
        
        log("Waiting for next capture...")




root = Tk()
root.title("screen summarizer")


mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

monitor = StringVar()
monitor_entry = ttk.Entry(mainframe, width=7, textvariable=monitor)
monitor_entry.grid(column=2, row=1, sticky=(W, E))

delay = StringVar()
delay_entry = ttk.Entry(mainframe, width=7, textvariable=delay)
delay_entry.grid(column=2, row=3, sticky=(W, E))

api_key = StringVar()
api_key_entry = ttk.Entry(mainframe, width=30, textvariable=api_key, show="*")
api_key_entry.grid(column=2, row=5, sticky=(W, E))

ttk.Button(mainframe, text="Begin capture loop!", command=main).grid(column=3, row=4, sticky=W)

log_var = StringVar(value="Ready...")
ttk.Label(mainframe, textvariable=log_var).grid(column=1, row=0, columnspan=3, sticky=(W, E))

ttk.Label(mainframe, text="which monitor?").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="delay? (in seconds)").grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, text="API Key").grid(column=3, row=5, sticky=W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

monitor_entry.focus()
root.bind("<Return>", main)

root.mainloop()
