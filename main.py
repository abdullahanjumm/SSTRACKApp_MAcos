from tkinter import Tk
import os
import pickle
import platform
import sys
import time

# Conditional imports for Windows-specific modules
if platform.system() == "Windows":
    import win32event
    import win32api
    import win32gui
    import winerror
    import win32process

from login import LoginApp
from customized import GUIApp

WINDOW_TITLE = "SStrack"
MUTEX_NAME = "myapp_InstanceMutex"

def bring_window_to_foreground():
    if platform.system() == "Windows":
        def enum_windows_callback(hwnd, pid):
            if win32gui.IsWindowVisible(hwnd) and win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
                win32gui.SetForegroundWindow(hwnd)
                print("Already running")
                return False  # Stop enumeration once the window is found
            return True

        win32gui.EnumWindows(enum_windows_callback, os.getpid())
        time.sleep(0.1)  # Add a small delay to allow mutex release

def main():
    # Dynamically resolve the base directory
    BASE_DIR = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

    if platform.system() == "Windows":
        # Only create and check for the mutex on Windows
        mutex = win32event.CreateMutex(None, False, MUTEX_NAME)
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            bring_window_to_foreground()
            return  # Exit the main function without attempting to release the mutex

    # Start the main application
    data_path = os.path.join(BASE_DIR, "data.pkl")
    if os.path.exists(data_path):
        with open(data_path, "rb") as f:
            stored_data = pickle.load(f)
        root = Tk()
        app = GUIApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    else:
        root = Tk()
        login_app = LoginApp(root)
        root.mainloop()

    if platform.system() == "Windows":
        # Release the mutex if this instance created it
        win32event.ReleaseMutex(mutex)
        win32api.CloseHandle(mutex)

if __name__ == "__main__":
    main()
