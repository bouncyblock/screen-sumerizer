from gtts import gTTS

text = "Hello, this is a test of gTTS."

tts = gTTS(text=text, lang="en")
tts.save("output.mp3")

print("Saved output.mp3")
