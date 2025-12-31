import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer

app = QApplication(sys.argv)

# --- Window setup ---
label = QLabel()
label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
label.setAttribute(Qt.WA_TranslucentBackground)

# --- Load GIF ---
movie = QMovie("chrono_trigger.gif")
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

# Keep animation references to prevent garbage collection
anim_in = None
anim_out = None

# --- Slide in animation ---
anim_in = QPropertyAnimation(label, b"geometry")
anim_in.setDuration(800)
anim_in.setStartValue(start_rect)
anim_in.setEndValue(end_rect)
anim_in.start()

def slide_out():
    global anim_out
    end_rect2 = QRect(start_x, -gif_h, gif_w, gif_h)

    anim_out = QPropertyAnimation(label, b"geometry")
    anim_out.setDuration(800)
    anim_out.setStartValue(end_rect)
    anim_out.setEndValue(end_rect2)
    anim_out.finished.connect(lambda: (label.close(), app.quit()))
    anim_out.start()

# After sliding in, wait 2 seconds, then slide out
QTimer.singleShot(2000, slide_out)

sys.exit(app.exec_())
