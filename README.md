# screen summarizer BETA
## What if you could have the AI stream checker that DougDoug used in one of his [recent popular clips?](https://www.youtube.com/shorts/EYF_fvP8o8M)? 
![hackatime badge](https://hackatime-badge.hackclub.com/U09GRHV7Y80/screen-sumerizer)

Well, APPARENTLY YOU ALREADY COULD because halfway through this project I realized that his [github account](https://github.com/DougDougGithub/Babagaboosh/tree/main) is public. BUT I FINISHED MY VERSION ANYWAYS.

This app basically works by looking at one of your monitors (or a virtual monitor using [this repo](https://github.com/VirtualDrivers/Virtual-Display-Driver), which is what I recommend if you don't what summaries of your own screen), sending it to gemini-2.5-flash, sending that output to gTTS (google TTS, aka the Google Translate TTS), then playing it using pygame.

***PLEASE NOTE THAT MOST OF THE CODE IS WRITTEN FOR THE AI.HACKCLUB.COM API KEY PROVIDER. IT HAS NOT BEEN TESTED WITH OTHER TYPES OF API KEYS***
## How can I set it up?

***hey so the releases do not have a beta release conpiled. the only option is running from source!***

### if you're running from source... 

1. make sure you have python 3.11 installed
2. clone the project
3. install the dependencies (pip install -r requirements.txt)
4. run main.py (python3 main.py)


minimal layout required:
```
screen-sumerizer
|- screenshots/    # should auto generate now....
|- voices/         # won't auto generate but not needed for anything but Coqui-TTS
|- main.py
|- character.py    # depricated functions, yet to be removed from main....
|- utils.py
|- .env

```

### secret bonus guide: compile to .exe from source!
for this, I used nuitka because it was the first one that compiled to a working .exe. basically, once you're finished modifying your code, this is the command I used to compile this.

```
python -m nuitka main.py `
    --mode=standalone `
    --enable-plugin=tk-inter `
    --enable-plugin=pyqt5 `
    --include-package=<copy and paste this line for everything in the requirements.txt> `
    --noinclude-data-file=*.env
```
this will generate 2 folders, main.build and main.dist. the files you likely want are in main.dist.

optionally, you can compress it into one .exe with this command instead, but if the top command doesn't work for you this won't either.
```
python -m nuitka main.py `
    --mode=onefile `
    --enable-plugin=tk-inter `
    --enable-plugin=pyqt5 `
    --include-package=<copy and paste this line for everything in the requirements.txt> `
    --noinclude-data-file=*.env
```
## how do I use this?

### GUI:

// add image here

alright, here we go.

the top text is a debug log, but its only one line. Just because nothing changes immediately after pressing begin capture loop does not mean its broken. it depends on your set delay.


first input line is which display do you want to be capturing. you can find number identifications in any display settings you bios has. THIS NUMBER IS 1 INDEXED. IF YOU PUT 0 IN, YOU DONT HAVE 0 MONITORS (or if you do then I don't know why you're using this program)


second input line is delay between screenshots. this number will be ADDED onto however much time it takes to finish the tts


the api key. the program will auto input the api key if you have a .env and you press start capture link otherwise you need a:
- Hack Club API key
- 11Labs API key      // hey so if you're using this, the voice selector hasen't been added as a prompt... ctrl-f the code for 042 and change that voice ID to the one you want!

and even with a correct api key, it can still fail.
some formatting notes:
- don't have api_key= or anything like that
- don't have quotes around the api key
- only have the api key


for Voice Method, you have a couple of options. 
gTTS is free, but uses the google translator voice and cannot be changed
11Labs can use 20k credits per month, then it won't work without a subscription (this voice is the best)
Coqui-TTS will use the voice YOU PUT in voices/ and is free because it runs on your hardware. if you have an NVIDIA GPU then you'll have short generation times, but anything else its like 2m for a normal response.

i personally like 11labs the best because Coqui sounds buggy imo but its expensive :C


the button "Clear Screenshots" does what it says. the screenshots the program gets are saved in screenshots/ and aren't deleted so this will do that.


the button "start capture loop" starts the program! only press it when you're ready, the error handling is questionable at best on the compiled version. if it broke because you pressed the button too many times, maybe a quick restart wouldn't hurt you.



(if you compiled from source run main.py)

### CLI:
the CLI is no longer supported, sorry. you can still find it in the files (testing/main-cli.py) but it lacks proper dirrectory control, TTS other than gTTS, and a lot more. 

to use it, make sure you have a screenshots folder in the same dir and a .env with the following format:



## expected output
some ai yelling at you in the <chosen voice method> voice every _delay_ seconds!

## faq

Q: 

![alt text](image-2.png)

A:

your api key is invalid!

Q:

![alt text](image-3.png)

A:

your monitor is out of range!

Q: File screenshot not found

A: you don't have a screenshots folder in the project dir!

Q: why is summarizer misspelt everywhere 

it was late ok


## secret bonus recommendation

if you were to unironically use this software, I'd recommend you set it up on a virtual monitor using [this repo](https://github.com/VirtualDrivers/Virtual-Display-Driver), find out what it was numbered in windows settings, and use it as where you store the thing you want summarized. It keeps it off your main screen, and still renders everything correctly (ahem electron apps). please note this has the same effect as plugging a second monitor into you pc. (if you're having problems with resolution/size of external monitor, change the resolution in windows advanced display settings. it should give you resolution options)

but ohhhh I can't see the other monitor- use obs to capture the other monitor! its still being rendered in the background. (which does mean your mouse will move off screen into it)

***not my work*** but a really cool project that works really well with this one.


another thing, if you aren't happy with the default personality, change "prompt" in main.py (provided you're using the source code edition). this current personality is based HEAVILY on dougdougs ai ([that project](https://github.com/DougDougGithub/Babagaboosh/tree/main)) which i only discovered halfway though but ultimately decided to use it because my ai prompt was NOT working well.

## planned features
- conversation rather than redefining the entire ai every time
- cross platform compatability (don't have a mac so idk about this one...)
- better UI and UX
    - right now you HAVE to set up Coqui no matter what
    - same for 11Labs
    - the ui is outdated and should have defaults in case of missing one
    - error handling

## ai use disclaimer
i did use some code generation and some copying from stack overflow for the example flies (not used for the main program, just me testing) and some bugfixing (look coqui has some stupid dependancies). there is probably a small ai code in the main.py from "inline suggestions".


i did not use ai for the readme or commits.


oh and...
you use ai to generate the answers to whats on your screen. this means you are FEEDING AI a picture of your screen.

## and with that, i'm off.
did the main work all in one night with no sleep from midnight to 8am, with some changes at 1pm. i've never felt so burnt out. on the bright side, i have this great screenshot (it was paused for one hour at one point):
<img width="1917" height="1033" alt="Screenshot 2025-12-31 084333" src="https://github.com/user-attachments/assets/63ea9bde-463f-448a-b905-52f1410fc532" />

the rest of the work was done in the following week and added
- 11labs
- Coqui
- a funny prompt
- file reorg
- requirements.txt

and i removed chrono because it didn't work and i hate pyqqt or whatever its called.

now im done :D