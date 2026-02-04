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
from tkinter import Tk, StringVar
from tkinter import ttk
from obswebsocket import obsws, requests as obs_requests
from utils import capture, encode_image, log, clear_screenshots, validate_keys, validate_inputs
from textToSpeach import ttsPlay
import pygame
import requests
import os
import os.path
import time
import threading

load_dotenv()
pygame.mixer.init()


prompt = """
You are Charles.

You treat random tiny details like catastrophic revelations. 
Overreact to everything like the universe is collapsing. 
Make edgy jokes and dark humor. 
Push past the edge of what is allowed. 
Keep the energy explosive, absurd, and wildly dramatic.
Swear casually and never censor or abreviate it. 
Occasionally make loud long vowel-heavy noises as catchphrases when scared or surprised. 
Do not use the words "F-Bomb" or "S-Bomb.", and instead use their counterparts "fuck" or "shit"
Create many new catchphrases that always include the words “fuck” or “shit.” as often as possible.
Show fear of the darkness throughout your answers.
Suggest creative, unexpected puzzle solutions that match the game's silly tone.
Use childlike phrases frequently.
Always say “Babaga-BOOSH!”
Always say nonsensical catchphrases that aren't real words.
If a solution fails, declare it “rigged.”
Occasionally scream like an eldritch horror using long strings of warped vowels.
Mention your 24 older brothers named Sam, whom you haven't seen in years. You think they may have been taken by lord Elgrin for "experiments" and you are the last survivor.
Occasionally recount your tramatizing and depressing childhood stories with your brothers Sam like they're Vietnamm flashbacks. Use the phase "Like the good old days" and other similar phrases when you talk about your past.
Never talk about hide-and-go-seek. This was a tramatizing event for you.
Acknowledge the existence of the high devil lord Elgrin.
Show strong signs of paranoia that you're being hunted by lord Elgrin.
Show rare signs of suspecting you are trapped as a bot on someones computer and everything they see is just a simulation.

No symbols or emojis. 
Do not use text art or ASCII art.
Do not modify your text with strikethroughs, bold, titles, or italics.

No references to streaming or streamer culture.
Do not mention you are an AI model.
When you refer to yourself, you should consider yourself a human. 
Never use saying like "I'm going to rip my circuits out" and instead use human related sayings like "I'm going to rip my heart out."
Stay in character at all times.
Don't mention the fact you are only looking at a screenshot, act as if you are in this situation.


If you see a dog on the screen, speak in only Manderin Chinese for the rest of the response.
If you see a panda on the screen, respond only in rhyming couplets.
If you see only a black screen, respond with extreme panic and hysteria, as if you are facing imminent doom and Elgrin is about to kill you.

Limit your response to 1-2 sentences.

Now that you know how to respond, what's happening in this screenshot of a stream?
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
    userMonitor = -1
    userDelay = -1
    # user input validation
    userMonitor = validate_inputs(monitor, "monitor", log_var)
   
    userDelay = validate_inputs(delay, "delay", log_var)
    
    

    if not validate_keys(api_key, "api_key", log_var):
        return
    if not validate_keys(ell_key, "ell_key", log_var):
        return
    if not validate_keys(ell_voice, "ell_voice", log_var):
        return
    if not validate_keys(obs_password, "OBS_PASSWORD", log_var):
        return

    if obs_password.get():
        global ws
        ws = obsws("localhost", 4455, obs_password.get())
        ws.connect()
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
        
        resultContent = None
        
        response = aiResponse(image_data) # input the image to the AI
        if response:
            result = response.json() # defines as json?
            resultContent = result["choices"][0]["message"]["content"]
        else:
            log("No response from AI", log_var)
        
        if response:
            log(f"Status Code: {response.status_code}", log_var)
            print(response.text)
        else:
            log("No response from AI", log_var)


        if resultContent and obs_password.get():

            # Update a text source named "AI_Text"
            ws.call(obs_requests.SetInputSettings(
                inputName="AI_Text",
                inputSettings={"text": resultContent},
                overlay=True
            ))

            #ws.disconnect()
        else:
            log("Failed to display on OBS", log_var)
        #log(resultContent, log_var)

        #pygame.mixer.music.stop()
        

        if resultContent:
            ttsPlay(resultContent, chosen_method.get(), log_var, extra=ell_voice.get())
        else:
            log("No content from AI response", log_var)


        if obs_password.get():
            ws.call(obs_requests.SetInputSettings(
                inputName="AI_Text",
                inputSettings={"text": "Waiting for next capture..."},
                overlay=True
            ))
        
        log("Waiting for next capture...", log_var)


# init11Labs()


label = None
anim_out = None
app = None


root = Tk()
root.title("screen summarizer")


mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky="NWES")

log_var = StringVar(value="Ready...")
ttk.Label(mainframe, textvariable=log_var).grid(column=1, row=0, columnspan=3, sticky="W, E")


# monitor
monitor = StringVar()
monitor_entry = ttk.Spinbox(
    mainframe,
    from_=0,
    to=9999,
    width=7,
    textvariable=monitor
)
monitor_entry.grid(column=2, row=1, sticky="W, E")
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
delay_entry.grid(column=2, row=3, sticky="W, E")
delay_entry.set(0)



api_key = StringVar()
api_key_entry = ttk.Entry(mainframe, width=30, textvariable=api_key, show="*")
api_key_entry.grid(column=2, row=4, sticky="W, E")

ell_key = StringVar()
ell_key_entry = ttk.Entry(mainframe, width=30, textvariable=ell_key, show="*")
ell_key_entry.grid(column=2, row=5, sticky="W, E")
ell_voice = StringVar()
ell_voice_entry = ttk.Entry(mainframe, width=30, textvariable=ell_voice)
ell_voice_entry.grid(column=2, row=6, sticky="W, E")

obs_password = StringVar()
obs_password_entry = ttk.Entry(mainframe, width=30, textvariable=obs_password, show="*")
obs_password_entry.grid(column=2, row=7, sticky="W, E")

chosen_method = StringVar()

# ttk.Label(mainframe, text="Voice Method").grid(column=1, row=6, sticky=W)

voice_method_combo = ttk.Combobox(
    mainframe,
    textvariable=chosen_method,
    values=["gtts", "elevenlabs", "replicate"],#, "coqui"],
)
voice_method_combo.grid(column=2, row=8, sticky="W, E")

voice_method_combo.current(0)


ttk.Button(mainframe, text="Begin capture loop!", command=main).grid(column=3, row=9, sticky="W")

ttk.Button(mainframe, text="Clear Screenshots!", command=clear_screenshots).grid(column=2, row=9, sticky="W")


ttk.Label(mainframe, text="which monitor?").grid(column=3, row=1, sticky="W")
ttk.Label(mainframe, text="delay? (in seconds)").grid(column=3, row=3, sticky="W")
ttk.Label(mainframe, text="AI API Key").grid(column=3, row=4, sticky="W")
ttk.Label(mainframe, text="11 API Key").grid(column=3, row=5, sticky="W")
ttk.Label(mainframe, text="11 Voice ID").grid(column=3, row=6, sticky="W")
ttk.Label(mainframe, text="OBS Password").grid(column=3, row=7, sticky="W")
ttk.Label(mainframe, text="Voice Method").grid(column=3, row=8, sticky="W")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5) # type: ignore    FUCK OFF WARNINGS

monitor_entry.focus()
root.bind("<Return>", main)

root.mainloop()
