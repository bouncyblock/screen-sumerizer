from obswebsocket import obsws, requests
import dotenv
import os

dotenv.load_dotenv()
obs_password = os.getenv("OBS_PASSWORD")

if obs_password:
    ws = obsws("localhost", 4455, obs_password)
    ws.connect()

    # Update a text source named "AI_Text"
    ws.call(requests.SetInputSettings(
        inputName="AI_Text",
        inputSettings={"text": "I AM SO GOOD AT PROGRAMMING WOOOOOO)"},
        overlay=True
    ))

    ws.disconnect()
else:
    print("OBS_PASSWORD not set in environment variables.")