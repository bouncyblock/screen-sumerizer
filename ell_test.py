from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ell_key"),
)
audio = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="nrD2uNU2IUYtedZegcGx",
    model_id="eleven_flash_v2_5",
    output_format="mp3_44100_128",
)
print("Playing audio...")
play(audio)
print("Audio playback finished.")