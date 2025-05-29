import objc
from Cocoa import (
    NSApplication, NSWindow, NSButton, NSTextField, NSSecureTextField,
    NSColor, NSFont, NSRunningApplication, NSApplicationActivateIgnoringOtherApps,
    NSMakeRect, NSImageView, NSImage
)
from Foundation import NSObject
from AppKit import NSAlert, NSMenu, NSMenuItem, NSApp
import requests
import pickle
import os
import sys
import webbrowser
from pathlib import Path
from customized import GUIApp


class LoginApp(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        def setup_main_menu(app_name="SStrack"):
            main_menu = NSMenu.alloc().init()

            app_menu_item = NSMenuItem.alloc().init()
            main_menu.addItem_(app_menu_item)
            NSApp.setMainMenu_(main_menu)

            app_menu = NSMenu.alloc().init()

            quit_title = f"Quit {app_name}"
            quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                quit_title,
                "terminate:",  # macOS built-in selector for quitting
                "q"
            )
            app_menu.addItem_(quit_item)

            app_menu_item.setSubmenu_(app_menu)
            
           # ✅ Call the menu setup function here
        setup_main_menu("SStrack")
        self.show_password = False  # Track if password is shown or hidden

        # Window setup
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100.0, 100.0, 700.0, 400.0),
            15,
            2,
            False
        )
        self.window.setTitle_("LOGIN")
        self.window.setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0)
        )
        self.window.makeKeyAndOrderFront_(None)

        # Center the window
        screen = self.window.screen().frame()
        win_frame = self.window.frame()
        center_x = (screen.size.width - win_frame.size.width) / 2
        center_y = (screen.size.height - win_frame.size.height) / 2
        self.window.setFrameOrigin_((center_x, center_y))

        content_view = self.window.contentView()

        # App Logo
        logo_path = self.resource_path("images/sstracklogo.png")
        if os.path.exists(logo_path):
            logo_image = NSImage.alloc().initByReferencingFile_(logo_path)
            self.logo_view = NSImageView.alloc().initWithFrame_(NSMakeRect(300, 310, 100, 50))
            self.logo_view.setImage_(logo_image)
            self.logo_view.setImageScaling_(2)
            content_view.addSubview_(self.logo_view)

        # Heading Text
        self.heading = NSTextField.alloc().initWithFrame_(NSMakeRect(250, 280, 200, 30))
        self.heading.setStringValue_("Login to SStrack")
        self.heading.setBezeled_(False)
        self.heading.setDrawsBackground_(False)
        self.heading.setEditable_(False)
        self.heading.setSelectable_(False)
        self.heading.setAlignment_(1)
        self.heading.setFont_(NSFont.boldSystemFontOfSize_(18))
        self.heading.setTextColor_(NSColor.whiteColor())
        content_view.addSubview_(self.heading)

        # Email field
        self.email_field = NSTextField.alloc().initWithFrame_(NSMakeRect(200, 230, 300, 24))
        self.email_field.setPlaceholderString_("Enter your email")
        self.email_field.setFont_(NSFont.systemFontOfSize_(14))
        self.email_field.setEditable_(True)
        self.email_field.setSelectable_(True)
        content_view.addSubview_(self.email_field)

        # Password field (secure by default)
        self.password_field = NSSecureTextField.alloc().initWithFrame_(NSMakeRect(200, 185, 300, 24))
        self.password_field.setPlaceholderString_("Enter your password")
        self.password_field.setFont_(NSFont.systemFontOfSize_(14))
        self.password_field.setEditable_(True)
        self.password_field.setSelectable_(True)
        content_view.addSubview_(self.password_field)

        # Show Password Eye Icon Button
        self.toggle_password_button = NSButton.alloc().initWithFrame_(NSMakeRect(470, 165, 30, 24))
        self.toggle_password_button.setTitle_("👁️")
        self.toggle_password_button.setBezelStyle_(1)
        self.toggle_password_button.setBordered_(False)
        self.toggle_password_button.setTarget_(self)
        self.toggle_password_button.setAction_(objc.selector(self.togglePasswordVisibility_, signature=b'v@:'))
        content_view.addSubview_(self.toggle_password_button)

        # Login button
        self.login_button = NSButton.alloc().initWithFrame_(NSMakeRect(200, 135, 300, 32))
        self.login_button.setTitle_("Login")
        self.login_button.setBezelStyle_(1)
        self.login_button.setTarget_(self)
        self.login_button.setAction_(objc.selector(self.performLogin_, signature=b'v@:'))
        content_view.addSubview_(self.login_button)

        # Forget password button
        self.forget_button = NSButton.alloc().initWithFrame_(NSMakeRect(350, 95, 150, 20))
        self.forget_button.setTitle_("Forget Password")
        self.forget_button.setBordered_(False)
        self.forget_button.setTarget_(self)
        self.forget_button.setAction_(objc.selector(self.openForgetPassword_, signature=b'v@:'))
        content_view.addSubview_(self.forget_button)


    def togglePasswordVisibility_(self, sender):
        """Toggles between showing and hiding the password."""
        content_view = self.window.contentView()
        old_password = str(self.password_field.stringValue())
        frame = self.password_field.frame()

        self.password_field.removeFromSuperview()

        if self.show_password:
            self.password_field = NSSecureTextField.alloc().initWithFrame_(frame)
            self.toggle_password_button.setTitle_("👁️")
        else:
            self.password_field = NSTextField.alloc().initWithFrame_(frame)
            self.toggle_password_button.setTitle_("🙈")

        self.password_field.setStringValue_(old_password)
        self.password_field.setFont_(NSFont.systemFontOfSize_(14))
        self.password_field.setEditable_(True)
        self.password_field.setSelectable_(True)
        content_view.addSubview_(self.password_field)
        self.window.makeFirstResponder_(self.password_field)

        self.show_password = not self.show_password

    def get_user_data_dir(self):
        path = os.path.join(Path.home(), "Library", "Application Support", "SStrack")
        os.makedirs(path, exist_ok=True)
        return path

    def resource_path(self, relative_path):
        if getattr(sys, '_MEIPASS', False):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

  
    def openForgetPassword_(self, sender):
        webbrowser.open("https://www.sstrack.io/forget-password", new=2)

    def performLogin_(self, sender):
        print("🚪 login button clicked")
        email = str(self.email_field.stringValue())
        password = str(self.password_field.stringValue())
        api_url = "https://myuniversallanguages.com:9093/api/v1/signin"
        model = {"email": email, "password": password}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(api_url, json=model, headers=headers)
            data = response.json()

            if "message" in data:
                self._show_error(data["message"])
            else:
                data_dir = self.get_user_data_dir()
                data_path = os.path.join(data_dir, "data.pkl")
                credentials_path = os.path.join(data_dir, "new_data.pkl")

                with open(data_path, "wb") as f:
                    pickle.dump(data["token"], f)
                with open(credentials_path, "wb") as f:
                    pickle.dump({"email": email, "password": password}, f)

                print("✅ Login successful! Opening Home screen...")
                print(f"💾 Token saved at: {data_path}")
                print(f"💾 Credentials saved at: {credentials_path}")

                self.window.close()

                delegate = GUIApp.alloc().init()
                NSApplication.sharedApplication().setDelegate_(delegate)
                delegate.applicationDidFinishLaunching_(None)
        except requests.exceptions.RequestException:
            self._show_error("An error occurred while connecting to the server")


    def _show_error(self, message):
        alert = NSAlert.alloc().init()
        alert.setMessageText_("Error")
        alert.setInformativeText_(message)
        alert.runModal()
    
    def applicationShouldTerminate_(self, sender):
        print("✅ Application is quitting via Cmd+Q")
        return 1  # Equivalent to NSApplicationTerminateNow


# Entry point
if __name__ == '__main__':
    app = NSApplication.sharedApplication()
    delegate = LoginApp.alloc().init()
    app.setDelegate_(delegate)
    NSRunningApplication.currentApplication().activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    app.run()
