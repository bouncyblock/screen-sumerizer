# screen summerizer
## What if you could have the AI stream checker tha DougDoug used in one of his [recent popular clips?](https://www.youtube.com/shorts/EYF_fvP8o8M)? 
Well, APPARENTLY YOU ALREADY COULD because halfway through this project I relized that his [github account](https://github.com/DougDougGithub/Babagaboosh/tree/main) is public. BUT I FINISHED MY VERSION ANYWAYS.

This app basically works by looking at one of your monitors (or a virtual monitor using [this repo](https://github.com/VirtualDrivers/Virtual-Display-Driver), which is what I recommend if you don't what summeries of your own screen), sending it to gemini-2.5-flash, sending that output to gTTS (google TTS, aka the Google Translate TTS), then playing it using pygame.

## How can I set it up?

### if you're normal...


### if you're compiling from source...
Good news! All you need is Python 3.11, a COUPLE dependencies:
```
dotenv
openrouter
gtts import
PyQt5
tkinter
pygame
requests
base64
os
keyboard
mss
time
sys
threading
```
Also make sure you have a screenshots folder (even if empty), and for your .env file, well...
```api_key="my gemini-2.5-flash api key here"```

If for some reason you can't run it after that, please let me know (will.kuntze@gmail.com)! Or open an issue if you want?

## how do I use this?

### GUI:
![picture of application](image.png)
alright, here we go.
the top text is a debug log, but its only one line. Just because nothing changes imedietly after pressing begin capture loop does not mean its broken. it depends on your delay
first input line is which display do you want to be capturing. you can find number identifications in any display settings you bios has. THIS NUMBER IS 1 INDEXED. IF YOU PUT 0 IN, YOU DONT HAVE 0 MONITORS (or if you do then I don't know why you're using this program)
second input line is delay between screenshots. this number will be ADDED onto however much time it takes to finish the tts
the button starts the program! only press it when you're ready, the error handling is questionable at best on the compiled version. if it broke because you pressed the button too many times, maybe a quick restart wouldn't hurt you.

### CLI:
wow! I can't beleive you're using source just to use cli! there's only one option for the CLI verison though, monitor number, and you'll be prompted for that.
otherwise just run the python file (main-cli.py). it has SLIGHTLY less features than the GUI version.