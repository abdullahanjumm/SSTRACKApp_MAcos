import os
import pickle
import sys
from pathlib import Path

from Cocoa import NSApplication, NSRunningApplication, NSApplicationActivateIgnoringOtherApps
from PyObjCTools.AppHelper import runEventLoop

from login import LoginApp
from customized import GUIApp  # Must be PyObjC-based


def get_user_data_dir():
    path = os.path.join(Path.home(), "Library", "Application Support", "SStrack")
    os.makedirs(path, exist_ok=True)
    return path


def main():
    app = NSApplication.sharedApplication()
    user_data_path = os.path.join(get_user_data_dir(), "data.pkl")

    if os.path.exists(user_data_path):
        with open(user_data_path, "rb") as f:
            stored_data = pickle.load(f)
        # ✅ GUIApp must be a PyObjC NSObject subclass with applicationDidFinishLaunching_
        gui_delegate = GUIApp.alloc().init()
        app.setDelegate_(gui_delegate)
    else:
        # ✅ LoginApp must also be a PyObjC NSObject subclass with applicationDidFinishLaunching_
        login_delegate = LoginApp.alloc().init()
        app.setDelegate_(login_delegate)

    NSRunningApplication.currentApplication().activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    app.run()


if __name__ == "__main__":
    main()
