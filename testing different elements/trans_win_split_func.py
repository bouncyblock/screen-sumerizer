import sys
import time
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

# fuck off garbage collection
label = None
anim_out = None
app = None

def slide_in(gif_file="chrono_trigger.gif", duration=800):
    global label, app
    
    # Create app if it doesn't exist
    if not app:
        app = QApplication.instance() or QApplication(sys.argv)
    
    # Reuse or create label
    if label is None:
        label = QLabel()
        label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        label.setAttribute(Qt.WA_TranslucentBackground)
    
    # --- Load GIF ---
    movie = QMovie(gif_file)
    label.setMovie(movie)
    movie.start()
    
    # --- Screen + GIF geometry ---
    screen = app.primaryScreen().geometry()
    screen_w, screen_h = screen.width(), screen.height()
    
    movie.jumpToFrame(0)
    gif_w = movie.currentImage().width()
    gif_h = movie.currentImage().height()
    
    start_x = (screen_w - gif_w) // 2
    start_y = screen_h
    end_y = screen_h - gif_h - 50
    
    start_rect = QRect(start_x, start_y, gif_w, gif_h)
    end_rect = QRect(start_x, end_y, gif_w, gif_h)
    
    label.setGeometry(start_rect)
    label.show()
    
    # --- Slide in animation ---
    anim_in = QPropertyAnimation(label, b"geometry")
    anim_in.setDuration(duration)
    anim_in.setStartValue(start_rect)
    anim_in.setEndValue(end_rect)
    anim_in.start()
    
    label.start_x = start_x
    label.gif_h = gif_h
    label.end_rect = end_rect
    
    # Process events during animation
    start_time = time.time()
    while time.time() - start_time < duration / 1000.0:
        app.processEvents()
        time.sleep(0.01)

def slide_out(duration=800):

    global label, anim_out, app
    
    if not label or not app:
        return
    
    end_rect2 = QRect(label.start_x, -label.gif_h, label.end_rect.width(), label.end_rect.height())
    
    anim_out = QPropertyAnimation(label, b"geometry")
    anim_out.setDuration(duration)
    anim_out.setStartValue(label.end_rect)
    anim_out.setEndValue(end_rect2)
    anim_out.finished.connect(lambda: label.hide())
    anim_out.start()
    
    # Process events during animation
    start_time = time.time()
    while time.time() - start_time < duration / 1000.0:
        app.processEvents()
        time.sleep(0.01)

def get_app():
    global app
    return app


'''
slide_in("chrono_trigger.gif")
time.sleep(3)  
slide_out()
app = get_app()
if app:
    app.exec_()
'''

while True:
    slide_in("chrono_trigger.gif")
    time.sleep(2)  # Keep GIF visible for 2 seconds
    slide_out()
    time.sleep(1)  # Wait 1 second before next loop
app = get_app()
if app:
    app.exec_()