from utils import *
from gtts import gTTS
import torch
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.models.xtts import XttsArgs

torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig,
    XttsArgs,
])

from TTS.api import TTS
device = "cuda" if torch.cuda.is_available() else "cpu"
print(TTS().list_models())

# Init TTS with the target model name
coquitts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

client = ElevenLabs()

def init11Labs():
    client = ElevenLabs(
        api_key=os.getenv("ell_key"),
    )

def tts(text, method="gtts", log_var=None):
    if method == "gtts":
        output = gTTS(text=text, lang="en")
        output.save("temp/output.mp3")
        log("Saved temp/output.mp3", log_var)
        return "temp/output.mp3"
    elif method == "elevenlabs":
        audio = client.text_to_speech.convert(
        text=text,
        voice_id="gU0LNdkMOQCOrPrwtbee", # EDIT VOICE ID 042
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
        )
        return audio
    elif method == "coqui":
        coquitts.tts_to_file(
                text=text,
                speaker_wav="./voices/fry.wav",
                language="en",
                file_path="temp/output.wav",
                split_sentences=True,
                # 🔥 More expression
                temperature=1.0,      # 0.7–1.1: higher = more emotional/chaotic
                top_p=0.95,           # higher = more variety
                length_penalty=0.8,   # <1 = a bit more drawn-out / dramatic
                # ⚡ Faster render
                speed=1.5#,           # >1 = faster speaking rate
                #sample_rate=16000     # lower = faster generation, smaller file
            )
    else:
        log("Error: Unknown TTS method", log_var)
        return None