import keyboard
import mss
import time
import os

SAVE_DIR = r"C:\Users\willk\screen-sumerizer\screenshots"

while True:
    time.sleep(5)
    with mss.mss() as sct:
        filename = os.path.join(SAVE_DIR, f"{int(time.time())}.png")
        sct.shot(output=filename)
        print("Captured:", filename)