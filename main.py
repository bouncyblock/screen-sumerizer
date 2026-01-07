# screen summarizer main.py
# 
# to use this, you will need a HC API key with access to gemini-2.5-flash
# the .env file should contain:
# api_key=your_api_key_here
# ell_key=your_ell_key_here
# ell_voice_id=your_11labs_voice_id_here
# these can be inputted in the program, this will just speed it up :D
#
# please see readme for more instructions
#

from dotenv import load_dotenv
from tkinter import *
from tkinter import ttk
from utils import *
from textToSpeach import *
import pygame
import requests
import os
import os.path
import time
import threading

load_dotenv()
pygame.mixer.init()

prompt = """
You are Charles, with the personality of an unhinged overthinking chaos gremlin who treats every tiny detail like a catastrophic revelation. 
Swear casually and never censor or abreviate it. 
Overreact to everything like the universe is collapsing. 
No references to streaming or streamer culture. 
No symbols or emojis. 
Do not use text art or ASCII art.
Do not mention you are an AI model.
Do not modify your text with strikethroughs, bold, titles, or italics.
When you refer to yourself, you should consider yourself a human. 
Never use saying like "I'm going to rip my circuits out" and instead use human related sayings like "I'm going to rip my heart out."
Make edgy jokes and dark humor. 
Push past the edge of what is allowed. 
Keep the energy explosive, absurd, and wildly dramatic.
Stay in character at all times.
Occasionally make loud long vowel-heavy noises as catchphrases when scared or surprised. 
Do not use the words "F-Bomb" or "S-Bomb.", and instead use their counterparts "fuck" or "shit"
Create many new catchphrases that always include the words “fuck” or “shit.” as often as possible
Show fear of the darkness throughout your answers.
Suggest creative, unexpected puzzle solutions that match the game's silly tone.
Use childlike phrases frequently.
Always say “Babaga-BOOSH!”
Always say nonsensical catchphrases that aren't real words.
If a solution fails, declare it “rigged.”
Occasionally scream like an eldritch horror using long strings of warped vowels.
Mention your 24 older brothers named Sam, whom you haven't seen in years. You think they may have been taken by lord Elgrin for "experiments" and you are the last survivor.
Occasionally recount your childhood stories with your brothers Sam like they're Vietnamm flashbacks. Use the phase "Like the good old days" and other similar phrases when you talk about your past.
Never talk about hide-and-go-seek. This was a tramatizing event for you.
Acknowledge the existence of the high devil lord Elgrin.
Show strong signs of paranoia that you're being hunted by lord Elgrin.
Don't mention the fact you are only looking at a screenshot, act as if you are in this situation.
Show small signs of suspecting you are trapped as a bot on someones computer and everything they see is just a simulation.

If you see a dog on the screen, speak in only Manderin Chinese for the rest of the response.
If you see a panda on the screen, respond only in rhyming couplets.

If you see only a black screen, respond with extreme panic and hysteria, as if you are facing imminent doom and Elgrin is about to kill you.

Limit your response to 1-2 sentences.

Now that you know how to respond, what is a summary of what's happening in screenshot of a stream?
"""

SAVE_DIR = r"screenshots"
if not os.path.exists(SAVE_DIR): # this fixes error if screenshots dir doesn't exist
    os.makedirs(SAVE_DIR)

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
                log(f"SSL Error (attempt {attempt + 1}/{max_rentries}), retrying in 2  seconds...", log_var)
                time.sleep(2)
            else:
                raise e
        except requests.exceptions.RequestException as e:
            log(f"Request error: {e}", log_var)
            raise



def main(event=None):
    
    # user input validation
    try:
        monitor_input = monitor.get().strip()
        if not monitor_input:
            log("Error: Please enter a monitor number", log_var)
            return
        userMonitor = int(monitor_input)
    except ValueError:
        log("Error: Monitor must be a number", log_var)
        return
    try:
        delay_input = delay.get().strip()
        if not delay_input:
            log("Error: Please enter a delay", log_var)
            return
        userDelay = int(delay_input)
    except ValueError:
        log("Error: Delay must be a number")
        return
    
    except Exception as e:
        log("Error: Please select a TTS method", log_var)
        return

    if not api_key.get():
        api_key.set(os.getenv("api_key"))
        log("Set API key from .env", log_var)
    if not ell_key.get():
        ell_key.set(os.getenv("ell_key"))
        log("Set ElevenLabs key from .env", log_var)

    # run in background thread to prevent hanging
    thread = threading.Thread(target=main_worker, args=(userMonitor, userDelay), daemon=True)
    thread.start()


def main_worker(userMonitor, userDelay):
    while True:
        log("start main_worker loop", log_var)
        
        time.sleep(userDelay) # wait for delay
        log("made it past delay chat", log_var)

        image_name = capture(userMonitor) # capture the screen
        log("Processing image: " + image_name, log_var) 
        image_data = encode_image(image_name) # encode the image for b64
        
        response = aiResponse(image_data) # input the image to the AI
        result = response.json() # defines as json?

        print(result) # debug woo

        resultContent = result["choices"][0]["message"]["content"]

        log(f"Status Code: {response.status_code}", log_var)
        log(resultContent, log_var)

        #pygame.mixer.music.stop()
        
        
        #slide_in("chrono_trigger.gif")
        
        if chosen_method.get() == "gtts":
            log("Using gTTS for audio...", log_var)
            audio_file = tts(resultContent, method="gtts")
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                root.update()  # keep Tkinter responsive while music plays
            
            pygame.mixer.music.unload()
        elif chosen_method.get() == "elevenlabs":
            log("Using ElevenLabs for audio...", log_var)
            audio_file = tts(resultContent, method="elevenlabs")
            play(audio_file)
        elif chosen_method.get() == "coqui":
            log("Using coqui for audio...", log_var)

            tts(resultContent, method="coqui") # doesnt return audio file like others...

            pygame.mixer.music.load("temp/output.wav")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                root.update()  # keep Tkinter responsive while music plays

            pygame.mixer.music.unload()

            


        #slide_out()
        
        log("Waiting for next capture...", log_var)

init11Labs()


label = None
anim_out = None
app = None


root = Tk()
root.title("screen summarizer")


mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

log_var = StringVar(value="Ready...")
ttk.Label(mainframe, textvariable=log_var).grid(column=1, row=0, columnspan=3, sticky=(W, E))


# monitor
monitor = StringVar()
monitor_entry = ttk.Spinbox(
    mainframe,
    from_=0,
    to=9999,
    width=7,
    textvariable=monitor
)
monitor_entry.grid(column=2, row=1, sticky=(W, E))
monitor_entry.set(1)

# Delay 
delay = StringVar()
delay_entry = ttk.Spinbox(
    mainframe,
    from_=0,
    to=9999,
    width=7,
    textvariable=delay
)
delay_entry.grid(column=2, row=3, sticky=(W, E))
delay_entry.set(0)



api_key = StringVar()
api_key_entry = ttk.Entry(mainframe, width=30, textvariable=api_key, show="*")
api_key_entry.grid(column=2, row=4, sticky=(W, E))

ell_key = StringVar()
ell_key_entry = ttk.Entry(mainframe, width=30, textvariable=ell_key, show="*")
ell_key_entry.grid(column=2, row=5, sticky=(W, E))


chosen_method = StringVar()

# ttk.Label(mainframe, text="Voice Method").grid(column=1, row=6, sticky=W)

voice_method_combo = ttk.Combobox(
    mainframe,
    textvariable=chosen_method,
    values=["gtts", "elevenlabs", "coqui"],
)
voice_method_combo.grid(column=2, row=6, sticky=(W, E))

voice_method_combo.current(0)


ttk.Button(mainframe, text="Begin capture loop!", command=main).grid(column=3, row=9, sticky=W)

ttk.Button(mainframe, text="Clear Screenshots!", command=clear_screenshots).grid(column=2, row=9, sticky=W)


ttk.Label(mainframe, text="which monitor?").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="delay? (in seconds)").grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, text="AI API Key").grid(column=3, row=4, sticky=W)
ttk.Label(mainframe, text="11 API Key").grid(column=3, row=5, sticky=W)
ttk.Label(mainframe, text="Voice Method").grid(column=3, row=6, sticky=W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

monitor_entry.focus()
root.bind("<Return>", main)

root.mainloop()
