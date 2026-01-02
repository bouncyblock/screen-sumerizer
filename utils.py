import os
import time
import base64
import mss


def log(message, log_var=None):
    print(message)
    if log_var is not None:
        log_var.set(message)

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def capture(monitor=1, SAVE_DIR="screenshots"):
    with mss.mss() as sct:
        filename = os.path.join(SAVE_DIR, f"{int(time.time())}.png")
        sct.shot(mon = monitor,output=filename)
        log("Captured: " + filename)
        return filename

def clear_screenshots(SAVE_DIR="screenshots"):
    for file in os.listdir(SAVE_DIR):
        file_path = os.path.join(SAVE_DIR, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            log(f"Error deleting file {file_path}: {e}")