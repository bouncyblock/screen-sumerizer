from utils import *
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play



# Init TTS with the target model name
client = ElevenLabs()

def init11Labs():
    client = ElevenLabs(
        api_key=os.getenv("ell_key"),
    )

def tts(text, method="gtts", extra = None):
    if method == "gtts":
        output = gTTS(text=text, lang="en")
        output.save("temp/output.mp3")
        # log("Saved temp/output.mp3", log_var)
        return "temp/output.mp3"
    elif method == "elevenlabs":
        audio = client.text_to_speech.convert(
        text=text,
        # voice_id="gU0LNdkMOQCOrPrwtbee", # EDIT VOICE ID 042
        voice_id=extra,
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
        )
        return audio
    else:
       # og("Error: Unknown TTS method", log_var)
        return None