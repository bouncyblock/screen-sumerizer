import ctypes
from ctypes import wintypes
import win32gui
import win32ui
import win32con
import win32process
import psutil

# this is so complicated for so little gain, its better to just use the other method and have another monitor (or emulated monitor) because of discord not updating its window unless its window has priority
# i also dont know how most of this works, this is pieced together from stack overflow
# for anyone who wants to try and add this to main, check compatibility with electron apps

dwm = ctypes.WinDLL("dwmapi")
DwmGetWindowAttribute = dwm.DwmGetWindowAttribute
DWMWA_EXTENDED_FRAME_BOUNDS = 9

def find_pid_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            return proc.info['pid']
    return None

def find_window_by_pid(pid):
    result = []

    def callback(hwnd, _):
        # Only consider visible windows with titles
        if win32gui.IsWindowVisible(hwnd):
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                result.append(hwnd)
        return True

    win32gui.EnumWindows(callback, None)
    return result

def find_window_by_title(title_substring):
    result = []
    
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if title_substring.lower() in window_title.lower():
                result.append(hwnd)
        return True
    
    win32gui.EnumWindows(callback, None)
    return result

def get_window_rect(hwnd):
    rect = wintypes.RECT()
    DwmGetWindowAttribute(hwnd, DWMWA_EXTENDED_FRAME_BOUNDS,
                          ctypes.byref(rect),
                          ctypes.sizeof(rect))
    return rect.left, rect.top, rect.right, rect.bottom

def capture_window(hwnd, output="capture.png"):
    left, top, right, bottom = get_window_rect(hwnd)
    width = right - left
    height = bottom - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)

    # BitBlt copies the actual window surface, even if covered
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    saveBitMap.SaveBitmapFile(saveDC, output)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)


pid = find_pid_by_name("discord.exe")
print("PID:", pid)

# Search for Discord window by title
hwnds = find_window_by_title("discord")
if hwnds:
    print(f"Found Discord window: {hwnds[0]}")
else:
    print("Discord window not found")


hwnd = hwnds[0]  # main window
capture_window(hwnd, "discord.png")
