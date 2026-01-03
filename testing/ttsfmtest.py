from ttsfm import TTSClient, AudioFormat, Voice

client = TTSClient()

# Basic usage
response = client.generate_speech(
    text="Hello from TTSFM!",
    voice=Voice.ALLOY,
    response_format=AudioFormat.MP3,
)
response.save_to_file("hello")  # -> hello.mp3

# With speed adjustment (requires ffmpeg)
response = client.generate_speech(
    text="This will be faster!",
    voice=Voice.NOVA,
    response_format=AudioFormat.MP3,
    speed=1.5,  # 1.5x speed (0.25 - 4.0)
)
response.save_to_file("fast")  # -> fast.mp3