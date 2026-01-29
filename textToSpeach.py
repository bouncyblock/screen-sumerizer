import pygame
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


client = ElevenLabs(
    api_key=os.getenv("ell_key"),
)

    

def ttsGenerate(text, method="gtts", log_var=None, _extra=None):
    match method:
        case "gtts":
            output = gTTS(text=text, lang="en")
            output.save("temp/output.mp3")
            log("Saved temp/output.mp3", log_var)
            return "temp/output.mp3"
        
        case "elevenlabs":
            audio = client.text_to_speech.convert(
            text=text,
            voice_id=str(_extra), # EDIT VOICE ID 042
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128",
            )
            with open("temp/output.mp3", "wb") as f:
                f.write(b"".join(audio))
            log("Saved temp/output.mp3", log_var)
            return "temp/output.mp3"
        
        case "coqui":
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
        case _:
            log("Error: Unknown TTS method", log_var)
            return None
    

def ttsPlay(file_path, method="gtts", log_var=None, extra=None):
    match method:
        case "gtts":
            log("Using gTTS for audio...", log_var)
            
            audio_file = ttsGenerate(file_path, method="gtts")
            
            if audio_file and isinstance(audio_file, str):
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                    #root.update()  # keep Tkinter responsive while music plays
                
                pygame.mixer.music.unload()
            else:
                log("Error generating gTTS audio", log_var)
        
        case "elevenlabs":
            log("Using ElevenLabs for audio...", log_var)
            audio_file = ttsGenerate(file_path, method="elevenlabs", _extra=extra) # voice id
            
            if audio_file and isinstance(audio_file, str):
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
                play(audio_bytes)
            else:
                log("Error generating ElevenLabs audio", log_var)

        case "coqui":
            log("Using coqui for audio...", log_var)

            ttsGenerate(file_path, method="coqui") # doesnt return audio file like others...

            pygame.mixer.music.load("temp/output.wav")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                #root.update()  # keep Tkinter responsive while music plays

            pygame.mixer.music.unload()