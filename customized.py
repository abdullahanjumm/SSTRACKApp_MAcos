from tkinter import *
from tkinter import Toplevel
from tkinter import messagebox
import datetime
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont
import objc
from Cocoa import (
    NSApplication, NSWindow, NSView, NSImageView, NSImage,
    NSButton, NSTextField, NSColor, NSFont,
    NSRunningApplication, NSApplicationActivateIgnoringOtherApps,
    NSMakeRect, NSTitledWindowMask, NSClosableWindowMask,
    NSResizableWindowMask, NSBackingStoreBuffered,
)
# ✅ CORRECT
from AppKit import NSMutableAttributedString, NSForegroundColorAttributeName, NSPopUpButton, NSButtonCell, NSBezierPath, NSAttributedString, NSDictionary, NSForegroundColorAttributeName
from Quartz import CAShapeLayer, CGPathCreateMutable, CGPathAddRoundedRect, CGRectMake
from Foundation import NSObject
import pickle
import base64
import json
import tkinter as tk
import requests
import time
import os
import threading
import io
import platform
# from pynput import mouse, keyboard
import sys
import subprocess
import webbrowser
import requests
import pytz
import ctypes
# import win32com.client
from dateutil.parser import parse
from datetime import timedelta
# import PySimpleGUIQt as sg
import re
import datetime as dt
from dateutil import parser  # Handy for parsing ISO 8601 strings
# import messagebox from tkinter module  
import tkinter.messagebox
import uuid  # Import the UUID module for generating a unique ID
import socketio
from ActivityMonitor import ActivityMonitor
from pystray import Icon, Menu, MenuItem
import shutil
from plyer import notification
from Quartz import CAShapeLayer, CGPathCreateMutable, CGPathAddRoundedRect, CGRectMake
from AppKit import NSImage, NSSize
from tkinter import font
# Import platform-specific libraries
if platform.system() == "Windows":
    import pygetwindow as gw
elif platform.system() == "Linux":
    import ewmh
from pathlib import Path
from Cocoa import NSWindow, NSView, NSImageView, NSImage, NSTextField, NSButton
from Cocoa import NSColor, NSFont, NSMakeRect
class GUIApp(NSObject):
    def applicationDidFinishLaunching_(self, notification):
            # Initialize tracking-related variables
        self.is_timer_running = False
        self.screenshot_count = 0
        self.total = 0
        self.exact_time = None
        self.playTime = None
        self.break_button_enabled = True
        self.breakActive = False
        self.popActive = False
        self.calledImmediate = False
        self.total_intervals = 0
        self.active_intervals = 0
        self.trackingStart_list = []
        self.sio = socketio.Client()
        self.token = None
        self.employeeSetting_lock = threading.Lock()
        self.fetch_data_lock = threading.Lock()
        self.user_Data()
        self.last_time = time.time()
        self.description = None
        self.activity_flag = False
        self.sleep_mode = False
        self.active_intervals = 0
        self.total_intervals = 0
        self.activityinterval = 12
        self.autoPauseTrackingAfter = 20
        self.disabled = False
        self.autoPauseenabled = False
        self.frequency = 2
        self.ssperhr = 30
        self.updated = False
        self.download = False
        self.current_v = "1.1.25"
        self.dailytime = "0h 0m"
        self.hours = "00"
        self.minutes = "00"
        self.BreakTime='0h 0m'
        self.check_for_update_lock = threading.Lock()  # Initialize the lock
        self.percentage = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        self.overall_report = ""  
        self.weeklyTimeLimit = "No limit"
        self.allowAddingOfflineTime = 0
        self.trackingStart_list = []
        self.trackingStop_list=[]
        self.breakData = []
        self.breakData_list = [] 
        self.calledImmediate = False
        self.autoLaunch = False
        self.launch_monitor = False
        self.breakActive = False
        self.breakCount = 0
        self.breakUsed = {}
        self.breakConvertedData = []
        self.popActive=False
        self.breakFound = False
        self.last_notification_time = 0  
        self.notification_timeout = 3  
        self.user_id = None
        self.projects = ["no project"]
        

        self.setupUI()

    def resource_path(self, relative_path):
        import sys, os
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    def setupUI(self):
        self.is_timer_running = False
        self.total = 0
        self.exact_time = None
        self.playTime = None
        self.break_button_enabled = True
        self.breakActive = False
        self.popActive = False
        self.total_intervals = 0
        self.active_intervals = 0
        self.trackingStart_list = []

        # Create the main window
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 700, 340),
            15,  # Titled, closable, resizable
            2,   # Buffered
            False
        )
        self.window.setTitle_("SStrack - Home")
        self.window.setBackgroundColor_(NSColor.whiteColor())
        self.window.makeKeyAndOrderFront_(None)

        content_view = self.window.contentView()

        # Header view (blue background)
        self.header_view = NSView.alloc().initWithFrame_(NSMakeRect(0, 260, 700, 80))
        self.header_view.setWantsLayer_(True)
        self.header_view.layer().setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0).CGColor()
        )
        content_view.addSubview_(self.header_view)

        # Logo
        logo_path = self.resource_path("images/sstracklogo.png")
        if os.path.exists(logo_path):
            logo_image = NSImage.alloc().initByReferencingFile_(logo_path)
            logo_view = NSImageView.alloc().initWithFrame_(NSMakeRect(40, 10, 130, 60))
            logo_view.setImage_(logo_image)
            logo_view.setImageScaling_(2)  # scale proportionally
            self.header_view.addSubview_(logo_view)

  
        
        # ✅ Test Button (styled like settings button)
        test_icon_path = self.resource_path("images/Settings_Icon.png")  # Same or another icon
        if os.path.exists(test_icon_path):
            test_image = NSImage.alloc().initByReferencingFile_(test_icon_path)
            test_image.setTemplate_(False)
            resized_test_image = GUIApp.resize_nsimage(test_image, 26, 26)
        
            self.test_button = NSButton.alloc().initWithFrame_(NSMakeRect(598, 291, 18, 18))  # ⬅️ small button frame
            self.test_button.setBezelStyle_(0)
            self.test_button.setBordered_(False)
            self.test_button.setImage_(resized_test_image)
            self.test_button.setTarget_(self)
            self.test_button.setAction_("openSettings:")  # ✅ Make sure your handler ends with a colon
            content_view.addSubview_(self.test_button)
        

        
        # Logout button
        logout_icon_path = self.resource_path("images/log_out_white.png")
        if os.path.exists(logout_icon_path):
            logout_image = NSImage.alloc().initByReferencingFile_(logout_icon_path)
            logout_image.setTemplate_(False)
            resized_logout_image = GUIApp.resize_nsimage(logout_image, 26, 26)
            self.logout_button = NSButton.alloc().initWithFrame_(NSMakeRect(648, 32, 18, 18))
            self.logout_button.setBezelStyle_(0)
            self.logout_button.setBordered_(False)
            self.logout_button.setImage_(resized_logout_image)
            self.logout_button.setTarget_(self)
            self.logout_button.setAction_("logout:")
            self.header_view.addSubview_(self.logout_button)




        # Username label (example)
        # ✅ Checkmark Icon
        check_icon_path = self.resource_path("images/verified.png")
        if os.path.exists(check_icon_path):
            check_image = NSImage.alloc().initByReferencingFile_(check_icon_path)
            self.check_icon = NSImageView.alloc().initWithFrame_(NSMakeRect(230, 170, 30, 30))
            self.check_icon.setImage_(check_image)
            self.check_icon.setImageScaling_(2)  # Scale proportionally
            content_view.addSubview_(self.check_icon)


        # ✅ Username Label
        self.username_label = NSTextField.alloc().initWithFrame_(NSMakeRect(273, 170, 300, 30))

        # ✅ Set it dynamically from self.name
        if hasattr(self, "name") and self.name:
            self.username_label.setStringValue_(self.name)
        else:
            self.username_label.setStringValue_("User Name")  # fallback

        self.username_label.setFont_(NSFont.boldSystemFontOfSize_(22))
        self.username_label.setBezeled_(False)
        self.username_label.setDrawsBackground_(False)
        self.username_label.setEditable_(False)
        self.username_label.setSelectable_(False)
        self.username_label.setTextColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0)
        )
        content_view.addSubview_(self.username_label)

        # ✅ Description / Project Entry (grey placeholder + underline)
# ✅ Add this line before creating project_field
        self.placeholder = "enter your project description"

        # ✅ Now create project_field normally
        self.project_field = NSTextField.alloc().initWithFrame_(NSMakeRect(230, 130, 300, 28))
        self.project_field.setPlaceholderString_(self.placeholder)  # <- Use the variable now
        self.project_field.setFont_(NSFont.systemFontOfSize_(14))
        self.project_field.setTextColor_(NSColor.grayColor())
        self.project_field.setBezeled_(False)
        self.project_field.setDrawsBackground_(False)
        self.project_field.setEditable_(True)
        self.project_field.setSelectable_(True)
        self.project_field.setBordered_(False)
        content_view.addSubview_(self.project_field)

        self.project_field.setTarget_(self)
        self.project_field.setAction_("getDescriptionValue:")
        # self.project_field.setSendsActionOnEndEditing_(True)

        # ✅ Add blue underline below the project field
        underline = NSView.alloc().initWithFrame_(NSMakeRect(230, 128, 300, 2))
        underline.setWantsLayer_(True)
        underline.layer().setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0).CGColor())
        content_view.addSubview_(underline)
        
        
        # ✅ Company Button (Right of Username and Project Field)
        self.company_button = NSButton.alloc().initWithFrame_(NSMakeRect(550, 210, 120, 32))  # (x, y, width, height)
        self.company_button.setBezelStyle_(0)  # No standard macOS button style
        self.company_button.setBordered_(False)
        self.company_button.setWantsLayer_(True)
        self.company_button.layer().setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0).CGColor()  # Same dark blue color
        )

        # ✅ Set Button Text from self.company
        company_name = self.company if hasattr(self, "company") and self.company else "Company"

        title_attr = NSMutableAttributedString.alloc().initWithString_(company_name)
        title_attr.addAttribute_value_range_(
            NSForegroundColorAttributeName,
            NSColor.whiteColor(),
            (0, len(company_name))  # ⚡ Use dynamic length
        )
        self.company_button.setAttributedTitle_(title_attr)

        # ✅ Set Button Action
        self.company_button.setTarget_(self)
        self.company_button.setAction_("printCompanyName:")

        content_view.addSubview_(self.company_button)




        # --- Dropdown below the button ---
        # --- Dropdown below the button ---
        self.project_dropdown = NSPopUpButton.alloc().initWithFrame_pullsDown_(NSMakeRect(550, 130, 120, 32), False)

        # ✅ Dynamically add items from self.projects
        if hasattr(self, "projects") and self.projects:
            self.project_dropdown.addItemsWithTitles_(self.projects)
        else:
            self.project_dropdown.addItemsWithTitles_(["no project"])  # fallback if empty

        # Style the dropdown similarly
        self.project_dropdown.setFont_(NSFont.boldSystemFontOfSize_(13))
        self.project_dropdown.setBordered_(False)
        self.project_dropdown.setWantsLayer_(True)
        self.project_dropdown.layer().setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0).CGColor()
        )
        self.project_dropdown.setContentTintColor_(NSColor.whiteColor())  # Set text color to white if supported

        self.project_dropdown.setTarget_(self)
        self.project_dropdown.setAction_("projectSelected:")

        content_view.addSubview_(self.project_dropdown)


        # Style the dropdown similarly
        self.project_dropdown.setFont_(NSFont.boldSystemFontOfSize_(13))
        self.project_dropdown.setBordered_(False)
        self.project_dropdown.setWantsLayer_(True)
        self.project_dropdown.layer().setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0).CGColor()
        )
        self.project_dropdown.setContentTintColor_(NSColor.whiteColor())  # Set text color to white if supported

        self.project_dropdown.setTarget_(self)
        self.project_dropdown.setAction_("projectSelected:")

        content_view.addSubview_(self.project_dropdown)
        
        # Timer Background View (Green with Rounded Top-Left Corner)
        self.timer_view = NSView.alloc().initWithFrame_(NSMakeRect(-30, 10, 240, 250))
        self.timer_view.setWantsLayer_(True)
        self.timer_view.layer().setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.48, 0.796, 0.349, 1.0).CGColor()  # #7ACB59
        )
        content_view.addSubview_(self.timer_view)
        
        # Create path for top-left rounded corner
        path = CGPathCreateMutable()
        rect = CGRectMake(0, 0, 240, 250)  # ⬅️ Fix this line
        CGPathAddRoundedRect(path, None, rect, 40, 40)  # 40-radius on all corners (mask will only reveal top-left)
        rounded_layer = CAShapeLayer.layer()
        rounded_layer.setFrame_(rect)
        rounded_layer.setPath_(path)
        self.timer_view.layer().setMask_(rounded_layer)
        
        # "Today" Label
        today_label = NSTextField.alloc().initWithFrame_(NSMakeRect(50, 200, 100, 30))
        today_label.setStringValue_("Today")
        today_label.setFont_(NSFont.boldSystemFontOfSize_(18))
        today_label.setTextColor_(NSColor.whiteColor())
        today_label.setBezeled_(False)
        today_label.setDrawsBackground_(False)
        today_label.setEditable_(False)
        today_label.setSelectable_(False)
        self.timer_view.addSubview_(today_label)
        
        # Hour Label
        self.hour_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 110, 100, 80))  # Bigger width and height
        self.hour_label.setStringValue_(str(self.hours))  # ← Here you show self.hours dynamically
        self.hour_label.setFont_(NSFont.boldSystemFontOfSize_(50))
        self.hour_label.setBezeled_(False)
        self.hour_label.setDrawsBackground_(False)
        self.hour_label.setEditable_(False)
        self.hour_label.setSelectable_(False)
        self.hour_label.setTextColor_(NSColor.whiteColor())
        self.hour_label.setAlignment_(1)  # Center alignment (optional)
        self.timer_view.addSubview_(self.hour_label)


        # First check if Roboto is really installed, fallback if not
        font = NSFont.fontWithName_size_("Roboto", 50)
        if font is None:
            font = NSFont.boldSystemFontOfSize_(50)  # fallback to system bold font

        self.hour_label.setFont_(font)
        self.hour_label.setBezeled_(False)
        self.hour_label.setDrawsBackground_(False)
        self.hour_label.setEditable_(False)
        self.hour_label.setSelectable_(False)
        self.hour_label.setTextColor_(NSColor.whiteColor())
        self.hour_label.setAlignment_(1)  # Center alignment (optional)
        self.timer_view.addSubview_(self.hour_label)

        
        # Colon Label
        colon_label = NSTextField.alloc().initWithFrame_(NSMakeRect(110, 145, 20, 40))
        colon_label.setStringValue_(":")
        colon_label.setFont_(NSFont.boldSystemFontOfSize_(36))
        colon_label.setBezeled_(False)
        colon_label.setDrawsBackground_(False)
        colon_label.setEditable_(False)
        colon_label.setSelectable_(False)
        colon_label.setTextColor_(NSColor.whiteColor())
        self.timer_view.addSubview_(colon_label)
        
        # --- Minute Label (Updated) ---
        print(f"✅ Debug: Current minutes value is: {self.minutes}")
        self.minute_label = NSTextField.alloc().initWithFrame_(NSMakeRect(120, 110, 100, 80))  # Bigger frame
        self.minute_label.setStringValue_(str(self.minutes))  # ← Show self.minutes dynamically
        self.minute_label.setFont_(NSFont.boldSystemFontOfSize_(50))
        self.minute_label.setBezeled_(False)
        self.minute_label.setDrawsBackground_(False)
        self.minute_label.setEditable_(False)
        self.minute_label.setSelectable_(False)
        self.minute_label.setTextColor_(NSColor.whiteColor())
        self.minute_label.setAlignment_(1)  # Optional: Center alignment
        self.timer_view.addSubview_(self.minute_label)


        # Safely use Roboto font if available, fallback otherwise
        minute_font = NSFont.fontWithName_size_("Roboto", 50)
        if minute_font is None:
            minute_font = NSFont.boldSystemFontOfSize_(50)  # fallback to system bold

        self.minute_label.setFont_(minute_font)

        self.minute_label.setBezeled_(False)
        self.minute_label.setDrawsBackground_(False)
        self.minute_label.setEditable_(False)
        self.minute_label.setSelectable_(False)
        self.minute_label.setTextColor_(NSColor.whiteColor())
        self.minute_label.setAlignment_(1)  # Optional: Center text
        self.timer_view.addSubview_(self.minute_label)

        
        
        
         # --- Bottom blue view (like header) ---
        self.bottom_view = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 700, 110))
        self.bottom_view.setWantsLayer_(True)
        self.bottom_view.layer().setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0).CGColor())
        content_view.addSubview_(self.bottom_view)

    
        # ✅ First load images
        self.play_icon = self.load_icon(self.resource_path("images/playButton.png"), 80, 80)
        self.play_icon_grey = self.load_icon(self.resource_path("images/Play_Icon_Grey.png"), 80, 80)
        self.pause_icon_grey = self.load_icon(self.resource_path("images/Pause_Icon_Grey.png"), 60, 60)
        self.pause_icon = self.load_icon(self.resource_path("images/Pause_Red.png"), 60, 60)


        # ✅ Now safe to create Play Button
        self.play_button = NSButton.alloc().initWithFrame_(NSMakeRect(40, 40, 40, 40))
        self.play_button.setImage_(self.play_icon)
        self.play_button.setBezelStyle_(0)
        self.play_button.setBordered_(False)
        self.play_button.setImageScaling_(2)
        self.play_button.setTarget_(self)
        self.play_button.setAction_("playButtonClicked:")
        self.bottom_view.addSubview_(self.play_button)

        # ✅ Create Pause Button
        self.pause_button = NSButton.alloc().initWithFrame_(NSMakeRect(100, 40, 40, 40))
        self.pause_button.setImage_(self.pause_icon_grey)
        self.pause_button.setBezelStyle_(0)
        self.pause_button.setBordered_(False)
        self.pause_button.setImageScaling_(2)
        self.pause_button.setTarget_(self)
        self.pause_button.setAction_("pauseButtonClicked:")
        self.bottom_view.addSubview_(self.pause_button)



        # --- Break Button ---
        self.break_button = NSButton.alloc().initWithFrame_(NSMakeRect(210, 40, 160, 40))
        self.break_button.setBezelStyle_(0)
        self.break_button.setBordered_(False)
        self.break_button.setWantsLayer_(True)
        self.break_button.layer().setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.91, 0.96, 0.99, 1.0).CGColor()
        )
        self.break_button.layer().setCornerRadius_(6)  # Optional: soft edges
        self.break_button.layer().setBorderWidth_(0)   # No border

        # Set dark blue title
        break_text_attr = NSAttributedString.alloc().initWithString_attributes_(
            "Break",
            NSDictionary.dictionaryWithObject_forKey_(
                NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0),
                NSForegroundColorAttributeName
            )
        )
        self.break_button.setAttributedTitle_(break_text_attr)
        self.break_button.setFont_(NSFont.boldSystemFontOfSize_(18))
        self.bottom_view.addSubview_(self.break_button)
        
        # --- View Break Timeline (Clickable Text Button) ---
        self.view_break_timeline_button = NSButton.alloc().initWithFrame_(NSMakeRect(230, 20, 120, 20))  # Below Break button
        self.view_break_timeline_button.setBezelStyle_(0)
        self.view_break_timeline_button.setBordered_(False)
        self.view_break_timeline_button.setWantsLayer_(True)
        self.view_break_timeline_button.layer().setBackgroundColor_(NSColor.clearColor())

        view_break_attr = NSAttributedString.alloc().initWithString_attributes_(
            "View Break Timeline",
            NSDictionary.dictionaryWithObject_forKey_(
                NSColor.whiteColor(),  # White color text
                NSForegroundColorAttributeName
            )
        )
        self.view_break_timeline_button.setAttributedTitle_(view_break_attr)
        self.view_break_timeline_button.setFont_(NSFont.systemFontOfSize_(10))
        # --- Set click action ---
        self.view_break_timeline_button.setTarget_(self)
        self.view_break_timeline_button.setAction_("openViewBreakTimeline:")

        self.bottom_view.addSubview_(self.view_break_timeline_button)

        # --- View Timeline Button ---
        self.view_timeline_button = NSButton.alloc().initWithFrame_(NSMakeRect(480, 40, 160, 40))
        self.view_timeline_button.setBezelStyle_(0)
        self.view_timeline_button.setBordered_(False)
        self.view_timeline_button.setWantsLayer_(True)
        self.view_timeline_button.layer().setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.91, 0.96, 0.99, 1.0).CGColor()
        )
        self.view_timeline_button.layer().setCornerRadius_(6)  # Optional
        self.view_timeline_button.layer().setBorderWidth_(0)   # No border

        # Set dark blue title
        timeline_text_attr = NSAttributedString.alloc().initWithString_attributes_(
            "VIEW TIMELINE",
            NSDictionary.dictionaryWithObject_forKey_(
                NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0),
                NSForegroundColorAttributeName
            )
        )
        self.view_timeline_button.setAttributedTitle_(timeline_text_attr)
        self.view_timeline_button.setFont_(NSFont.boldSystemFontOfSize_(16))
        self.bottom_view.addSubview_(self.view_timeline_button)
        
        # Start background listeners (mouse and keyboard)
        threading.Thread(target=self.start_listeners, daemon=True).start()

        # Initialize activity monitor
        self.activity_monitor = ActivityMonitor()

        # Instead of BooleanVar, simple bools
        self.launch_monitor_enabled = False
        self.auto_start_enabled = False
        self.selected_project_name = ""
        self.description = ""
        self.projectId = None
       
        # ✅ Add this block during setupUI (preferably at end of setupUI)
        self.updateProject_lock = threading.Lock()
        self.update_daily_time_lock = threading.Lock()
        self.click_pause_button_lock = threading.Lock()
        self.fetch_data_lock = threading.Lock()
        self.employeeSetting_lock = threading.Lock()
        self.handle_sleep_mode_lock = threading.Lock()
        self.play_timer_lock = threading.Lock()
        self.screenshots_add_lock = threading.Lock()
        self.stop_timer_lock = threading.Lock()
        self.screenshots_data_lock = threading.Lock()
        self.check_activity_lock = threading.Lock()
        self.update_time_lock = threading.Lock()
        self.breakExecution_lock = threading.Lock()
        self.startBreakTime_lock = threading.Lock()
        self.stopBreakTime_lock = threading.Lock()
        self.archive_project_lock = threading.Lock()
        self.on_project_select_lock = threading.Lock()
        self.update_User_status_lock = threading.Lock()

   # --- Define the function to open the link ---
   
   
    def openViewBreakTimeline_(self, sender):
        url = "https://www.sstrack.io/"  # Change your link here!
        webbrowser.open(url) 
    @objc.IBAction
    def printCompanyName_(self, sender):
        print("Company Name: i8is.com")
        
    @objc.IBAction
    def projectSelected_(self, sender):
        selected_project = self.project_dropdown.titleOfSelectedItem()
        print(f"Selected project: {selected_project}")    
    @staticmethod
    def resize_nsimage(image, new_width, new_height):
        from AppKit import NSSize
        resized = NSImage.alloc().initWithSize_(NSSize(new_width, new_height))
        resized.lockFocus()
        image.drawInRect_fromRect_operation_fraction_(
            ((0, 0), (new_width, new_height)),
            ((0, 0), image.size()),
            2,
            1.0
        )
        resized.unlockFocus()
        return resized



    @objc.typedSelector(b"v@:@")
    def openSettings_(self, sender):
        print("✅ Test button clicked!")
        
            # Safely close existing popup if already open
        if hasattr(self, "test_popup") and self.test_popup is not None:
            self.test_popup.close()
            self.test_popup = None

        # Create the popup window
        self.test_popup = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(250, 250, 700, 340),  # Same size
            15,  # Titled, Closable
            2,
            False
        )
        self.test_popup.setTitle_("Settings")
        self.test_popup.makeKeyAndOrderFront_(None)

        # Content View
        content = self.test_popup.contentView()
        content.setWantsLayer_(True)
        content.layer().setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0).CGColor())

        # --- Header Logo (small) ---
        settings_icon_path = self.resource_path("images/logoTray.png")
        if os.path.exists(settings_icon_path):
            icon_image = NSImage.alloc().initByReferencingFile_(settings_icon_path)
            resized_icon = GUIApp.resize_nsimage(icon_image, 20, 20)
            icon_view = NSImageView.alloc().initWithFrame_(NSMakeRect(20, 310, 20, 20))
            icon_view.setImage_(resized_icon)
            icon_view.setImageScaling_(2)
            content.addSubview_(icon_view)

        # --- Title Label ---
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(50, 310, 200, 20))
        title_label.setStringValue_("Settings")
        title_label.setFont_(NSFont.systemFontOfSize_(14))
        title_label.setBezeled_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setTextColor_(NSColor.whiteColor())
        content.addSubview_(title_label)

        # --- Close Button ("X") ---
        self.close_button = NSButton.alloc().initWithFrame_(NSMakeRect(660, 310, 20, 20))
        self.close_button.setTitle_("X")
        self.close_button.setFont_(NSFont.boldSystemFontOfSize_(14))
        self.close_button.setBezelStyle_(0)
        self.close_button.setBordered_(False)
        self.close_button.setWantsLayer_(True)

        # ✅ Background Black
        self.close_button.layer().setBackgroundColor_(NSColor.blackColor().CGColor())

        # ✅ Text White
        text_attr = NSMutableAttributedString.alloc().initWithString_("X")
        text_attr.addAttribute_value_range_(
            NSForegroundColorAttributeName,
            NSColor.whiteColor(),
            (0, 1)
        )
        self.close_button.setAttributedTitle_(text_attr)

        self.close_button.setTarget_(self)
        self.close_button.setAction_("closeTestPopup:")
        content.addSubview_(self.close_button)

        # --- Field Labels (White Text) ---
        field_names = [
            ("Launch on Startup", 250),
            ("Auto-start Tracking", 220),
            ("Screenshots:", 180),
            ("Auto-pause:", 150),
            ("Weekly limit:", 120),
            ("Allow Offline Time:", 90),
            ("Activity Level Tracking:", 60),
            ("App & URL Tracking:", 30)
        ]

        for text, y in field_names:
            field = NSTextField.alloc().initWithFrame_(NSMakeRect(30, y, 300, 20))
            field.setStringValue_(text)
            field.setFont_(NSFont.systemFontOfSize_(12))
            field.setBezeled_(False)
            field.setDrawsBackground_(False)
            field.setEditable_(False)
            field.setSelectable_(False)
            field.setTextColor_(NSColor.whiteColor())
            content.addSubview_(field)

    @objc.typedSelector(b"v@:@")
    def closeTestPopup_(self, sender):
        print("Closing Settings popup")
        if hasattr(self, "test_popup") and self.test_popup is not None:
            self.test_popup.orderOut_(None)  # Only hide popup
            self.test_popup = None

    def load_icon(self, path, width, height):
        if os.path.exists(path):
            img = NSImage.alloc().initByReferencingFile_(path)
            resized = GUIApp.resize_nsimage(img, width, height)
            return resized
        else:
            return None



    @objc.typedSelector(b"v@:@")
    def playButtonClicked_(self, sender):
        print("✅ Play button clicked")
        try:
            # ✅ UI changes first (change button icons)
            if hasattr(self, "play_button") and self.play_icon_grey:
                self.play_button.setImage_(self.play_icon_grey)

            if hasattr(self, "pause_button") and self.pause_icon:
                self.pause_button.setImage_(self.pause_icon)

            # ✅ Now call your full click_play_button logic
            self.click_play_button()

        except Exception as e:
            print(f"⚠️ Failed to start tracking: {e}")

    




    @objc.typedSelector(b"v@:@")
    def pauseButtonClicked_(self, sender):
        print("⏸️ Pause button clicked")

        try:
            # ✅ Revert play/pause icons
            if hasattr(self, "play_button") and self.play_icon:
                self.play_button.setImage_(self.play_icon)

            if hasattr(self, "pause_button") and self.pause_icon_grey:
                self.pause_button.setImage_(self.pause_icon_grey)

            # ✅ Lock section
            with self.click_pause_button_lock:
                if self.is_timer_running:
                    self.is_timer_running = False

                    # ✅ Remove tray icon (PyObjC version of `self.icon.stop()`, if applicable)
                    # Add code here if you're using NSStatusBar-based tray icon

                # ✅ Load time_entry_id
                try:
                    with open(GUIApp.get_data_file_path("time_entry_id.pkl"), "rb") as f:
                        timeEntryId = pickle.load(f)
                except (FileNotFoundError, EOFError):
                    print("❌ time_entry_id.pkl not found or empty.")
                    return

                # ✅ Load trackingStop_list
                self.trackingStop_list = []
                stop_list_path = GUIApp.get_data_file_path("trackingStop_list.pkl")
                if os.path.isfile(stop_list_path):
                    try:
                        with open(stop_list_path, "rb") as f:
                            self.trackingStop_list = pickle.load(f)
                    except EOFError:
                        print("⚠️ trackingStop_list.pkl is empty. Starting fresh.")

                # ✅ Append tracking stop data
                current_time = self.exact_time if self.sleep_mode else datetime.datetime.now(pytz.UTC)
                trackingstop = {"endTime": current_time, "timeEntryId": timeEntryId}
                self.trackingStop_list.append(trackingstop)

                # ✅ Save updated stop list
                with open(stop_list_path, "wb") as f:
                    pickle.dump(self.trackingStop_list, f)

                # ✅ Display Notification
                if not self.breakActive:
                    message = self.description or ""
                    if self.selected_project_name and self.selected_project_name != "no project":
                        project_name = self.selected_project_name.upper()
                        message = f"{project_name}\n{message}"

                    os.system('terminal-notifier -title "SSTRACK" -message "Tracking stopped" -appIcon "images/animatedlogo.png"')

                # ✅ Reset intervals and break
                self.total_intervals = 0
                self.active_intervals = 0
                self.breakStartedOn = current_time

                # ✅ Handle popup & break fetching
                if self.popActive:
                    self.popActive = False
                    threading.Thread(target=self.getBreaktimes).start()

                # ✅ Start stop timer
                threading.Thread(target=self.stop_Timer).start()

        except Exception as e:
            print(f"⚠️ An error occurred in pauseButtonClicked_: {e}")




    def start_listeners(self):
        # Start the listeners
        self.fetch_data()
        self.userProject()
        self.checkAutoLaunch()
        self.employeeSetting()
        self.fetch_projects()
        self.connect_to_server()
        self.getBreaktimes()
        self.getRemainingBreakTime()  
    @staticmethod
    def get_app_dir():
        """Get the directory where the executable is running."""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)  # Running as an executable
        return os.path.dirname(os.path.abspath(__file__))  # Running as a script   
    
    @staticmethod
    def get_data_file_path(filename):
        """
        Return the full path to a file stored in the user's Application Support directory for SStrack.
        This ensures the app has write access and avoids sandbox issues.
        """
        support_dir = os.path.join(Path.home(), "Library", "Application Support", "SStrack")
        os.makedirs(support_dir, exist_ok=True)  # Ensure directory exists
        return os.path.join(support_dir, filename)
    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for development and PyInstaller """
        if getattr(sys, 'frozen', False):
            # Running in a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running in a normal Python environment
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)




    def load_custom_font(self, size=52):
        # Path to the font file
        font_path = os.path.join(os.path.dirname(__file__), "font", "Technology.ttf")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        # Load the font with PIL
        pil_font = ImageFont.truetype(font_path, size)

        # Get the font family name from PIL
        font_family = pil_font.getname()[0]

        # Register the font family in tkinter
        font.nametofont("TkDefaultFont").configure(family=font_family)

        return font_family
    

    def open_link(self, event):
        url = f"https://www.sstrack.io/auth={self.token}"
        webbrowser.open(url, new=2)       



    def is_break_time_valid(self, break_time):
        """
        Checks if the break time is greater than 0h 0m.
        """
        if not break_time:
            return False

        # Parse the hours and minutes from the break time string
        try:
            parts = break_time.split()
            hours = int(parts[0][:-1])  # Extract the number before 'h'
            minutes = int(parts[1][:-1]) if len(parts) > 1 else 0  # Extract the number before 'm', if present
            return hours > 0 or minutes > 0  # Return True if either hours or minutes is greater than 0
        except (IndexError, ValueError):
            return False  # Return False if parsing fails


    def subtract_break_count(self, break_time):
        """
        Subtracts self.breakcount (in minutes) from a given break_time string.
        Returns the remaining time as a formatted string "Xh Ym".
        """
        if not break_time:
            return "0h 0m"  # Return zero time if no break_time is provided

        try:
            # Parse the hours and minutes from the break_time string
            parts = break_time.split()
            hours = int(parts[0][:-1]) if 'h' in parts[0] else 0  # Extract hours
            minutes = int(parts[1][:-1]) if len(parts) > 1 and 'm' in parts[1] else 0  # Extract minutes

            # Convert hours and minutes to total minutes
            total_minutes = hours * 60 + minutes

            # Subtract self.breakcount from total minutes
            remaining_minutes = max(0, total_minutes - 1)  # Prevent negative time

            # Convert remaining minutes back to hours and minutes
            remaining_hours = remaining_minutes // 60
            remaining_minutes %= 60
            self.BreakTime = f"{remaining_hours}h {remaining_minutes}m"
            self.update_break_label()

            return f"{remaining_hours}h {remaining_minutes}m"
        except (IndexError, ValueError):
            return "Invalid time format"  # Return error message for invalid input



    def calculate_max_characters(self):
        # Assuming the average width of a character in 'Roboto', size 11 is about 7 pixels
        average_char_width = 7  # This can vary depending on font style
        max_width = 350
        return max_width // average_char_width  # Calculate the max number of characters

    def limit_text_length(self, event):
        current_text = self.descriptions.get()
        if len(current_text) > self.max_characters:
            self.descriptions.delete(self.max_characters, tk.END)  # Truncate the text

    def show_menu(self, event=None):
        # Show the dropdown menu below the button
        try:
            # if hasattr(self, 'selected_project_name') and not self.selected_project_name:  # If project name is None, null, or empty
            #     self.selected_project_name = '+ project'
            self.button["text"] = self.selected_project.get()  # Update button text
            self.fixProject()
            x = self.button.winfo_rootx()
            y = self.button.winfo_rooty() + self.button.winfo_height()
            self.projects_dropdown.post(x, y)
        except Exception as e:
            print(f"Error displaying menu: {e}")


    # Mouse and keyboard event handlers
    def on_move(self, x, y):
        self.on_activity()

    def on_click(self, x, y, button, pressed):
        self.on_activity()

    def on_scroll(self, x, y, dx, dy):
        self.on_activity()

    def on_press(self, key):
        self.on_activity()

    def on_release(self, key):
        pass
  
  
  
    def userProject(self):
        try:
            headers = {"Authorization": "Bearer " + self.token}
            response = requests.get(
                "https://myuniversallanguages.com:9093/api/v1/timeTrack/userProject", headers=headers
            )
            if response.status_code == 200:
                projects_data = response.json()
                project = projects_data.get("data").get("project")
                description = projects_data.get("data").get("prodescription")
                if (
                    description is not None
                    and description != "null"
                    and description != ""
                ):
                    self.description = description
                    self.project_field.setStringValue_(self.description)
    
                projectName = project.get('name')
                if projectName is not None:
                    self.projectId = project.get("_id")
                    self.selected_project_name = projectName
    
                    # Select project in the dropdown
                    if projectName in self.projects:
                        self.project_dropdown.selectItemWithTitle_(projectName)
                    else:
                        self.project_dropdown.selectItemAtIndex_(0)  # "no project"
                else:
                    self.project_dropdown.selectItemAtIndex_(0)  # "no project"
    
                self.fixProject()
    
            else:
                print("Failed to fetch user project.")
        except Exception as e:
            print(f"Error fetching user projects: {e}")
 
 
    
    def fetch_projects(self):
        try:
            headers = {
                "Authorization": "Bearer " + self.token,
                "Content-Type": "application/json",
            }
            response = requests.get(
                "https://myuniversallanguages.com:9093/api/v1/timeTrack/getProjects", headers=headers
            )
            if response.status_code == 200:
                projects_data = response.json()
                project_list = projects_data.get("projects", [])
                                
                # Extract project names and IDs from the fetched project_list
                fetched_projects = {pro.get("name"): pro.get("_id") for pro in project_list}
                
                # Ensure "no project" is at the 0th index
                self.projects = ["no project"] + [name for name in fetched_projects.keys() if name != "no project"]
                
                
                # Update `project_map` to synchronize with the fetched data
                self.project_map = [
                    {"projectname": name, "projectid": proj_id}
                    for name, proj_id in fetched_projects.items()
                ]
                # Add new projects from incoming_projects to project_map and projects
                # for pro_id, pro_name in incoming_projects.items():
                #     if pro_id not in [project["projectid"] for project in self.project_map]:
                #         self.projects.append(pro_name)
                #         self.project_map.append({"projectname": pro_name, "projectid": pro_id})

                # Validate the selected project
                # if self.projectId and self.projectId not in [project["projectid"] for project in self.project_map]:
                #     self.projectName = " "
                #     self.projectIdNew = None
                #     try:
                #         os.remove("projectId.pkl")
                #     except FileNotFoundError:
                #         print("File projectId.pkl not found, skipping removal.")
                #     self.selected_project.set("+ Project")
                    
                    

                # Update the dropdown with the new projects
                self.update_projects_dropdown()  # Update dropdown with new projects
            else:
                print(
                    f"Failed to fetch projects: {response.status_code} - {response.text}"
                )
                self.update_projects_dropdown()  # Update dropdown with new projects

        except Exception as e:
            print(f"Error fetching projects: {e}")
    def update_projects_dropdown(self):
        try:
            # First remove all existing items
            self.project_dropdown.removeAllItems()

            # Add updated projects
            if hasattr(self, "projects") and self.projects:
                self.project_dropdown.addItemsWithTitles_(self.projects)
            else:
                self.project_dropdown.addItemsWithTitles_(["no project"])

            # Optionally set default selected item
            if self.projects and len(self.projects) > 0:
                self.project_dropdown.selectItemAtIndex_(0)

        except Exception as e:
            print(f"An error occurred in update_projects_dropdown: {e}")

    def fixProject(self):
        selected_project_name = self.selected_project.get()
        if len(selected_project_name) > 11:
            selected_project_name = (
                selected_project_name[:8] + "..."
            )  # Truncate and add ellipsis
        # if hasattr(self, 'selected_project_name') and not self.selected_project_name:  # If project name is None, null, or empty
        #         self.selected_project_name = '+ project'
        self.button["text"] = selected_project_name


    def callback(self, *args):
        try:
            print(f"the variable has changed to '{self.selected_project.get()}'")
            # if hasattr(self, 'selected_project_name') and not self.selected_project_name:  # If project name is None, null, or empty
            #         self.selected_project_name = '+ project'
            self.button["text"] = (
                self.selected_project.get()
            )  # Update button text when selection changes
            # self.selected_project_name = self.selected_project.get()
            self.fixProject()
            # self.on_project_select(self.selected_project.get())
            self.button.after(20, lambda: self.on_project_select(self.selected_project.get()))  # Run on_project_select after 20ms

        except Exception as e:
            print(f"Error callback projects: {e}")


    def updateProject(self):
        try:
            with self.updateProject_lock:
                if self.selected_project_name or self.description :
                    data = {
                        "projectId": self.projectId,
                        "projectDescription": self.description,
                    }
                    api_url = "https://myuniversallanguages.com:9093/api/v1"
                    headers = {
                        "Authorization": "Bearer " + self.token,
                    }
                    response = requests.post(
                        f"{api_url}/timetrack/updateProject", headers=headers, data=data
                    )
                    if response.ok:
                        data = response.json()
                        print("project updated", data)
                    else:
                        print("not success")
        except Exception as e:
            print(f"An error occurred updateProject: {e}")
            return None

    def show_custom_notification(project_name, description):
        root = tk.Tk()
        root.title("Notification")
        root.geometry("300x150")
        root.configure(bg="white")

        # Project Name with Blue Background
        project_label = tk.Label(root, text=project_name, bg="blue", fg="white", font=("Arial", 12, "bold"))
        project_label.pack(pady=10, fill="x")

        # Description
        description_label = tk.Label(root, text=description, bg="white", font=("Arial", 10))
        description_label.pack(pady=10)

        # Display for a few seconds
        root.after(5000, root.destroy)  # Close after 5 seconds
        root.mainloop()



    # Callback function to handle project selection
    def on_project_select(self, selected_project):
        try:
            with self.on_project_select_lock:
                selectedProject = self.selected_project.get()
                projectFound = False
                if self.selected_project_name is None: 
                    self.selected_project_name = selected_project
                    
                if self.selected_project_name != selected_project:
                    self.selected_project_name = selected_project
                    try:
                        # Find project ID from self.project_map
                        try:
                            # Find project ID from self.project_map
                            if selected_project != "no project":
                                for project in self.project_map:
                                    if project["projectname"] == selected_project:
                                        self.projectId = project["projectid"]
                                        projectFound = True
                                        break
                                if not projectFound:
                                    # If no match is found, reset projectId
                                    self.projectId = None
                            else:
                                # Handle "no project" case
                                self.projectId = None
                                # self.selected_project.set("no project")  # Ensure UI reflects the default value
                        except Exception as e:
                            print(f"An error occurred: {e}")

                        if self.is_timer_running:
                            print(projectFound)
                            # self.is_timer_running = False
                            self.restartTimer()
                            # # threading.Thread(target=self.updateProject).start()
                            # self.updateProject()
                        else:
                            # Handle case where project is not found, but continue safely
                            print(f"Selected project '{selected_project}' not found in project map.")
                            self.projectId = None  # Reset projectId for safety
                            # self.is_timer_running = False
                            # self.restartTimer()
                        # self.restartTimer()
                        # threading.Thread(target=self.updateProject).start()
                        self.updateProject()
                    except Exception as e:
                        print(f"An error occurred sub on_project_select: {e}")
                        return None
        except Exception as e:
            print(f"An error occurred on_project_select: {e}")
            return None

    def set_placeholder(self):
        print("Setting placeholder")  # Debugging statement
        self.descriptions.delete(0, tk.END)  # Clear the entry widget
        self.descriptions.insert(0, self.placeholder)
        self.descriptions.config(fg="grey")


    def getDescriptionValue_(self, sender):
        try:
            print("hello description value")
            value = str(self.project_field.stringValue())
            if value == self.placeholder:
                value = ""

            if value != self.description:
                self.description = value

                if self.description and self.is_timer_running:
                    self.restartTimer()

                if self.description:
                    self.project_field.setStringValue_(self.description)

                self.updateProject()

                print(value)

            # ✅ Only reset first responder if window is active
            if self.window and self.window.isVisible():
                self.window.makeFirstResponder_(None)

        except Exception as e:
            print(f"An error occurred in getDescriptionValue_: {e}")
            return None

    


    def on_focus_in(self, event):
        print("Focus in event triggered")  # Debugging statement
        if self.descriptions.get() == self.placeholder:
            self.descriptions.delete(0, tk.END)
            self.descriptions.config(fg="#0E4772")

    def on_focus_out(self, event):
        print("Focus out event triggered")  # Debugging statement
        if not self.descriptions.get() or self.descriptions.get() == "":
            self.set_placeholder()

    def view_Timeline(self):
        url = f"https://www.sstrack.io/auth={self.token}"
        webbrowser.open(url, new=2)  # Open in a new tab if possible

    def employeeSetting(self):
        # Replace with the actual API URL
        try:
            with self.employeeSetting_lock:
                headers = {
                    "Content-Type": "application/json",
                }

                response = requests.get(
                    f"https://myuniversallanguages.com:9093/api/v1/superAdmin/Settings/{self.user_id}",
                    headers=headers,
                )
                json_data = response.json()
                if response.ok:
                    # Use get() to handle missing keys gracefully
                    if json_data.get("employeeSettings", {}):
                        self.settings = json_data.get("employeeSettings", {})
                        print(self.settings)
                        self.updateSettings()
                else:
                    print(
                        f"Failed to get data: {response.status_code} - {response.text}"
                    )
                    # Check if the user is not logged in, access is blocked, or the user is archived
                    if (
                        not json_data.get("loggedIn", True) or
                        json_data.get("accessBlock", False) or
                        json_data.get("isArchived", False) or
                        "user not exists" in json_data.get("Message", "").lower()
                    ):
                        print("User access blocked, archived, or not logged in. Logging out...")

                        # List of files to delete
                        files_to_remove = [
                            'screenshots_data.pkl',
                            'trackingStart_list.pkl',
                            'trackingStop_list.pkl',
                            'breakData.pkl',
                            'breakUsed.pkl',
                            'new_data.pkl'
                        ]

                        # Attempt to remove each file
                        for file in files_to_remove:
                            file_path = GUIApp.get_data_file_path(file)
                            try:
                                os.remove(file_path)
                            except FileNotFoundError:
                                print(f"File not found: {file_path}")  # Ignore missing files
                            except Exception as e:
                                print(f"Error deleting {file_path}: {e}")

                        self.logout()
                        return  # Exit function early
                    # if response.text.message = "User not found"

                    return "N/A"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"

    def updateSettings(self):
        try:
            print(f"effective setting {self.settings}")
            self.autoPauseenabled = self.settings.get("autoPauseTrackingAfter", {}).get(
                "pause"
            )
            if self.autoPauseenabled:
                self.autoPauseTrackingAfter = self.settings.get(
                    "autoPauseTrackingAfter", {}
                ).get("frequency")
            else:
                self.autoPauseTrackingAfter = 0
            effectscreenshot = self.settings.get("screenshots")
            self.ssperhr = effectscreenshot.get("frequency")
            self.ssenable = effectscreenshot.get("enabled")
            self.weeklyTimeLimit = self.settings.get("weeklyTimeLimit")
            if self.weeklyTimeLimit == 0:
                self.weeklyTimeLimit = "No limit"
            self.allowAddingOfflineTime = self.settings.get("allowAddingOfflineTime")
            if not self.ssenable:
                self.disabled = True
            else:
                self.disabled = False

            # Extract numeric part using regular expression
            match = re.search(r"\d+", self.ssperhr)
            if match is not None:
                self.ssperhr = int(match.group())
                if self.ssperhr > 0:
                    self.frequency = int(60 / self.ssperhr)
                self.activityinterval = int(self.frequency * 60 / 10)
                print(self.ssperhr)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def user_Data(self):
        try:
            # Use the updated macOS-safe directory
            data_path = os.path.join(Path.home(), "Library", "Application Support", "SStrack", "data.pkl")

            if os.path.isfile(data_path):
                with open(data_path, "rb") as f:
                    stored_data = pickle.load(f)
                    self.token = stored_data
            else:
                print("data.pkl not found in Application Support.")
                return "N/A"

            # Decode the Base64-encoded parts of the token
            header, payload, signature = self.token.split(".")
            decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
            self.user_info = json.loads(decoded_payload)
            self.name = self.user_info.get("name", "N/A")

            # Format name
            if len(self.name) > 15:
                self.name = self.name[:12] + "..."
            else:
                self.name = self.name

            self.company = self.user_info.get("company", "N/A")
            self.user_id = self.user_info.get("_id", "N/A")

        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"



    def open_settingsSS(self):
        # Create a new Toplevel window for settings
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("700x340")  # Set initial window size
        settings_window.configure(bg="#F0F0F0")  # Light background color

        # Add padding and layout styling
        title_font = ("Arial", 10, "bold")
        label_font = ("Arial", 9)

        # Configure the grid layout to make it responsive
        settings_window.columnconfigure(0, weight=1)
        settings_window.columnconfigure(1, weight=1)
        settings_window.columnconfigure(2, weight=1)
        settings_window.columnconfigure(3, weight=1)

        # Team Settings Section
        tk.Label(
            settings_window,
            text="Team settings (set by company manager)",
            font=title_font,
            bg="#F0F0F0",
        ).grid(row=0, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # First column labels and values
        tk.Label(
            settings_window, text="Screenshots:", font=label_font, bg="#F0F0F0"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="30/hr", font=label_font, fg="#4CAF50", bg="#F0F0F0"
        ).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(
            settings_window, text="Auto-pause tracking:", font=label_font, bg="#F0F0F0"
        ).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="40 min", font=label_font, fg="#4CAF50", bg="#F0F0F0"
        ).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(
            settings_window, text="Weekly time limit:", font=label_font, bg="#F0F0F0"
        ).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window,
            text="No limit",
            font=label_font,
            fg="#4CAF50",
            bg="#F0F0F0",
        ).grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Second column labels and values
        tk.Label(
            settings_window,
            text="Allow adding offline time:",
            font=label_font,
            bg="#F0F0F0",
        ).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="No", font=label_font, fg="#F44336", bg="#F0F0F0"
        ).grid(row=1, column=3, padx=10, pady=5, sticky="w")

        tk.Label(
            settings_window,
            text="Activity Level tracking:",
            font=label_font,
            bg="#F0F0F0",
        ).grid(row=2, column=2, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="Yes", font=label_font, fg="#4CAF50", bg="#F0F0F0"
        ).grid(row=2, column=3, padx=10, pady=5, sticky="w")

        tk.Label(
            settings_window, text="App & URL tracking:", font=label_font, bg="#F0F0F0"
        ).grid(row=3, column=2, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="Yes", font=label_font, fg="#4CAF50", bg="#F0F0F0"
        ).grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Add buttons at the bottom, with responsiveness
        # save_button = tk.Button(settings_window, text="Save", width=12, height=1, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief="flat", command=self.save_settings)
        # cancel_button = tk.Button(settings_window, text="Cancel", width=12, height=1, bg="#F44336", fg="white", font=("Arial", 10, "bold"), relief="flat", command=settings_window.destroy)

        # save_button.grid(row=5, column=2, pady=20, padx=20, sticky="e")
        # cancel_button.grid(row=5, column=3, pady=20, padx=20, sticky="w")

        # Make sure focus stays on the settings window
        settings_window.grab_set()
    
    
        
    @objc.typedSelector(b"v@:@")
    def on_settings_click(self, sender):
        print("Settings button clicked (PyObjC)")
    
        # Create a new popup window
        self.settings_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(200, 200, 700, 340),
            15,  # Titled, Closable
            2,
            False
        )
        self.settings_window.setTitle_("Settings")
        self.settings_window.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(0.06, 0.28, 0.45, 1.0))
        self.settings_window.makeKeyAndOrderFront_(None)
    
        settings_content = self.settings_window.contentView()
    
        # --- Settings Title ---
        settings_title = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 300, 300, 30))
        settings_title.setStringValue_("Settings")
        settings_title.setFont_(NSFont.boldSystemFontOfSize_(20))
        settings_title.setBezeled_(False)
        settings_title.setDrawsBackground_(False)
        settings_title.setEditable_(False)
        settings_title.setSelectable_(False)
        settings_title.setTextColor_(NSColor.whiteColor())
        settings_content.addSubview_(settings_title)
    
        # --- Close Button ---
        self.close_button = NSButton.alloc().initWithFrame_(NSMakeRect(660, 305, 20, 20))
        self.close_button.setTitle_("x")
        self.close_button.setFont_(NSFont.boldSystemFontOfSize_(14))
        self.close_button.setBezelStyle_(0)
        self.close_button.setBordered_(False)
        self.close_button.setWantsLayer_(True)
        self.close_button.layer().setBackgroundColor_(NSColor.whiteColor().CGColor())
        self.close_button.setTarget_(self)
        self.close_button.setAction_("close_settings:")
        settings_content.addSubview_(self.close_button)
    
        # --- Static Labels ---
        fields = [
            ("Launch on Startup", 250),
            ("Auto-start Tracking", 220),
            ("Screenshots:", 180),
            ("Auto-pause:", 150),
            ("Weekly limit:", 120),
            ("Allow Offline Time:", 90),
            ("Activity Level Tracking:", 60),
            ("App & URL Tracking:", 30)
        ]
    
        for text, y in fields:
            label = NSTextField.alloc().initWithFrame_(NSMakeRect(30, y, 250, 24))
            label.setStringValue_(text)
            label.setFont_(NSFont.systemFontOfSize_(12))
            label.setBezeled_(False)
            label.setDrawsBackground_(False)
            label.setEditable_(False)
            label.setSelectable_(False)
            label.setTextColor_(NSColor.whiteColor())
            settings_content.addSubview_(label)
    



    def open_settingsMy(self):
        # Create a new Toplevel window for settings
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("700x340")  # Set initial window size
        settings_window.configure(bg="#0E4772")  # Light background color

        # Add padding and layout styling
        title_font = ("Arial", 10, "bold")
        label_font = ("Arial", 9)

        # Configure the grid layout to make it responsive
        settings_window.columnconfigure(0, weight=1)
        settings_window.columnconfigure(1, weight=1)
        settings_window.columnconfigure(2, weight=1)
        settings_window.columnconfigure(3, weight=1)

        # Team Settings Section
        tk.Label(
            settings_window,
            text="Team settings (set by company manager)",
            font=title_font,
            bg="#0E4772",
        ).grid(row=0, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # First column labels and values
        tk.Label(
            settings_window, text="Screenshots:", font=label_font, bg="#0E4772"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="30/hr", font=label_font, fg="#4CAF50", bg="#0E4772"
        ).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(
            settings_window, text="Auto-pause tracking:", font=label_font, bg="#0E4772"
        ).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="40 min", font=label_font, fg="#4CAF50", bg="#0E4772"
        ).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(
            settings_window, text="Weekly time limit:", font=label_font, bg="#0E4772"
        ).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window,
            text="No limit",
            font=label_font,
            fg="#4CAF50",
            bg="#0E4772",
        ).grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Second column labels and values
        tk.Label(
            settings_window,
            text="Allow adding offline time:",
            font=label_font,
            bg="#0E4772",
        ).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="No", font=label_font, fg="#F44336", bg="#0E4772"
        ).grid(row=1, column=3, padx=10, pady=5, sticky="w")

        tk.Label(
            settings_window,
            text="Activity Level tracking:",
            font=label_font,
            bg="#0E4772",
        ).grid(row=2, column=2, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="Yes", font=label_font, fg="#4CAF50", bg="#0E4772"
        ).grid(row=2, column=3, padx=10, pady=5, sticky="w")

        tk.Label(
            settings_window, text="App & URL tracking:", font=label_font, bg="#0E4772"
        ).grid(row=3, column=2, padx=10, pady=5, sticky="w")
        tk.Label(
            settings_window, text="Yes", font=label_font, fg="#4CAF50", bg="#0E4772"
        ).grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Add buttons at the bottom, with responsiveness
        save_button = tk.Button(
            settings_window,
            text="Save",
            width=12,
            height=1,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=self.save_settings,
        )
        cancel_button = tk.Button(
            settings_window,
            text="Cancel",
            width=12,
            height=1,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            command=settings_window.destroy,
        )

        # Position the Save button on the right
        save_button.grid(row=4, column=2, padx=20, pady=20, sticky="e")

        # Position the Cancel button on the bottom-left corner
        cancel_button.grid(row=4, column=3, padx=20, pady=20, sticky="w")

        # Make sure focus stays on the settings window
        settings_window.grab_set()

    def save_settings(self):
        print("Settings saved!")

    #    system tray
    def create_image(self):
        # Create an image for the system tray icon
        width = 64
        height = 64
        image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=(0, 0, 0), fill=(255, 255, 0))
        return image



    def stop_process(self):
        """Terminate the SSTRACK process."""
        try:
            os.system("taskkill /f /im SSTRACK.exe")  # Terminate the process directly
            print("SSTRACK process terminated.")
            self.root.destroy()  # Close the application window
        except Exception as e:
            print(f"Error while terminating SSTRACK process: {e}")

    def setup_tray_icon(self, icon):
        icon.visible = True

    def show_window(self):
        """Show the Tkinter window and bring it to the front."""
        self.root.deiconify()  # Show the window
        self.root.lift()  # Bring the window to the front
        self.root.focus_force()  # Focus the window

    def on_quit(self, icon, item):
        try:
            #    # Check if the timer is running
            if self.is_timer_running:
                confirm = messagebox.askyesno(
                    "App Closing", "Are you sure you want to stop the SSTRACK?"
                )
                if confirm:
                    # self.icon = self.custom_shutdown()
                    self.click_pause_button()  # Pause tracking before exiting
                    # self.icon.stop()  # Safely remove the tray icon
                    #         # self.root.quit()  # Close the application
                    print("removed icon")
                    # Delay the process termination to allow time for the icon to be removed
                    # threading.Timer(1, self.stop_process).start()  # Delay for 1 second
                    self.after(1000, self.stop_process)  # Delay for 1 second (1000 milliseconds)

        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"



    def screenshots_data(self):
        try:
            with self.screenshots_data_lock:
                # Capture the screenshot using PIL's ImageGrab
                screenshot = ImageGrab.grab()
                
                # Convert the screenshot to RGB mode if it is in RGBA
                if screenshot.mode == "RGBA":
                    screenshot = screenshot.convert("RGB")
                    
                jpeg_quality = 50  # You can adjust this value

                # Convert the image to a variable (in-memory data) with the specified quality
                with io.BytesIO() as output:
                    screenshot.save(output, format="JPEG", quality=jpeg_quality)
                    screenshot_data = output.getvalue()

                # with open(filename, "wb") as file:
                active_window_url = self.get_active_window_hostname()
                if active_window_url:
                    print(f"Active Window: {active_window_url}")
                    time_entry_id_path = GUIApp.get_data_file_path("time_entry_id.pkl")
                    with open(time_entry_id_path, "rb") as f:
                        timeEntryId = pickle.load(f)
                        current_time = datetime.datetime.now(pytz.UTC)
                        formatted_time = current_time.strftime("%I-%M-%S-%p_%m-%d-%Y")

                        filename = f"screenshot_{formatted_time}_{self.user_id}"
                        print(filename)

                        # if os.path.isfile("screenshots_data.pkl"):
                        if os.path.isfile(GUIApp.get_data_file_path("screenshots_data.pkl")):
                            try:
                                with open(GUIApp.get_data_file_path("screenshots_data.pkl"), "rb") as f:
                                    try:
                                        self.screenshot_data_list = pickle.load(f)
                                    except pickle.UnpicklingError as e:
                                        # Handle the unpickling error gracefully
                                        print(
                                            f"Error while unpickling: {e}. Skipping loading screenshots data."
                                        )
                                        self.screenshot_data_list = []  # Initialize empty list or take appropriate action
                            except EOFError:
                                # Handle the case when there is no data in the file
                                self.screenshot_data_list = []  # or any other appropriate action

                    screenshots_data = {
                        "files": {
                            "file": (f"{filename}.jpeg", screenshot_data, "image/jpeg")
                        },
                        "description": active_window_url,
                        "activityPercentage": self.percentage,
                        "startTime": self.startTime,
                        "createdAt": current_time,
                        "timeEntryId": timeEntryId,
                        "disabled": self.disabled,
                    }
                    self.screenshot_data_list.append(screenshots_data)
                    with open(GUIApp.get_data_file_path("screenshots_data.pkl"), "wb") as f:
                        pickle.dump(self.screenshot_data_list, f)
                    if len(self.trackingStart_list) > 0:
                        self.start_Timer()
                    threading.Thread(target=self.addScreenshots).start()
                    self.startTime = datetime.datetime.now(pytz.UTC)

        except Exception as e:
            print(f"An error occurred screenshots_data: {e}")
            return "N/A"

    def check_activity(self):
        try:
            self.startTime = datetime.datetime.now(pytz.UTC)
            start_time1 = time.time()  # Get the current time
            while time.time() - start_time1 < 10:
                if not self.is_timer_running:
                    print("timer isnt running")
                    # reset the intervals
                    self.total_intervals = 0
                    self.active_intervals = 0
                    return
                time.sleep(1)  # Check termination flag every second
            while self.is_timer_running:
                with self.check_activity_lock:
                  
                    # print("Acquired check_activity_lock.")

                    # Check for mouse and keyboard activity
                    self.activity_monitor.check_mouse_activity()
                    self.activity_monitor.check_keyboard_activity()
                    # Log activity detection
                    # print(f"Activity flag after checks: {self.activity_monitor.activity_flag}")
                    # if self.total_intervals == 12:  # Change this value to your desired interval
                    pauseAfter = 0
                    if (
                        isinstance(self.autoPauseTrackingAfter, int)
                        and self.autoPauseTrackingAfter > 0
                    ):
                        pauseAfter = int(self.autoPauseTrackingAfter / self.frequency)

                    self.total_intervals += 1
                    if self.activity_monitor.activity_flag:  # Use the activity flag from the monitor
                        self.active_intervals += 1
                        print(f"Active intervals: {self.active_intervals} (Detected Keyboard Activity)")

                    if (
                        self.total_intervals >= self.activityinterval
                    ):  # Change this value to your desired interval
                        self.percentage = (
                            self.active_intervals / self.total_intervals
                        ) * 100
                        print(f"Calculated percentage: {self.percentage}")
                        # reset the intervals
                        self.total_intervals = 0
                        self.active_intervals = 0
                        # Start a new thread to run screenshots_data concurrently
                        threading.Thread(target=self.screenshots_data).start()

                        # Start another thread to run update_daily_time concurrently
                        # threading.Thread(target=self.update_daily_time).start()

                        if self.percentage == 0:
                            self.total += 1
                            if self.total >= pauseAfter:
                                print(
                                    "All of the last 20 activity entries have an activity self.percentage of 0."
                                )
                                threading.Thread(target=self.click_pause_button).start()

                                tkinter.messagebox.showinfo(
                                    "SStrack Monitor Paused",
                                    "Your SStrack Monitor has been paused due to inActivity.\nPlease start again!",
                                )
                        else:
                            self.total = 0
                    if self.total_intervals % 6 == 0:
                        threading.Thread(target=self.update_daily_time).start()
                        # threading.Thread(target=self.update_User_status).start()

                    self.activity_monitor.activity_flag = False

                # Run check_activity every 2 seconds
                # time.sleep(10 - time.time() % 10)
                start_time = time.time()  # Get the current time
                while time.time() - start_time < 10:
                    if not self.is_timer_running:
                        print("timer isnt running")
                        # reset the intervals
                        self.total_intervals = 0
                        self.active_intervals = 0
                        return
                    time.sleep(1)  # Check termination flag every second
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"


    def addScreenshots(self):
        try:
            if len(self.trackingStart_list) == 0:
                if self.is_timer_running:
                    with self.screenshots_add_lock:
                        try:
                            with open(GUIApp.get_data_file_path("screenshots_data.pkl"), "rb") as f:
                                self.screenshot_data_list = pickle.load(f)

                            if self.screenshot_data_list:
                                api_url = "https://myuniversallanguages.com:9093/api/v1"
                                headers = {
                                    "Authorization": "Bearer " + self.token,
                                }

                                try:
                                    # Now you can iterate over the loaded data
                                    index = 0
                                    while index < len(self.screenshot_data_list):
                                        screenshot_data = self.screenshot_data_list[
                                            index
                                        ]
                                        count = 0
                                        files = screenshot_data["files"]
                                        timeEntryId = screenshot_data["timeEntryId"]

                                        response = requests.patch(
                                            f"{api_url}/timetrack/time-entries/{timeEntryId}/screenshotss",
                                            headers=headers,
                                            files=files,
                                            data=screenshot_data,
                                        )

                                        if response.ok:
                                            data = response.json()

                                            # Use get to avoid potential KeyError
                                            filename = data.get("filename")

                                            # Remove the first item from the list
                                            self.screenshot_data_list.pop(0)
                                            # Reset index to 0
                                            index = 0
                                            with open(
                                                GUIApp.get_data_file_path("screenshots_data.pkl"), "wb"
                                            ) as f:
                                                pickle.dump(
                                                    self.screenshot_data_list, f
                                                )

                                            if len(self.screenshot_data_list) == 0:
                                                self.fetch_data()

                                        else:
                                            print(
                                                f"Failed to get data: {response.status_code} - {response.text}"
                                            )
                                            count += 1
                                            if count >= 3:
                                                # Skip this item for now and move to the next one
                                                print(
                                                    f"Skipping item {index} after 3 failed attempts"
                                                )
                                                count = 0  # Reset the count for the next item
                                                index += 1  # Move to the next item
                                            else:
                                                # Retry the same item
                                                print(
                                                    f"Retrying item {index}, attempt {count}"
                                                )
                                                self.screenshot_data_list.pop(0)
                                                index = 0

                                except (
                                    requests.exceptions.RequestException
                                ) as internet_error:
                                    # Handle internet-related errors, such as connection issues
                                    print("Internet issue:", internet_error)
                                    return None  # This will stop the function from continuing
                            else:
                                return None  # This will stop the function from continuing

                        except FileNotFoundError:
                            # Handle the case where the pickle file doesn't exist or is empty
                            (print("file not found"),)
                            return None  # This will stop the function from continuing
            else:
                # threading.Thread(target=self.start_Timer).start()
                self.start_Timer

        except Exception as e:
            (print(f"An error occurred: {e}"),)
            return None  # This will stop the function from continuing

    def on_activity(self):
        self.activity_flag = True

    def get_active_window_hostname(self):
        try:
            if platform.system() == "Windows":
                try:
                    active_window = gw.getActiveWindow()
                    if active_window:
                        print(f"active window", active_window.title)
                        hostname = active_window.title.split(" - ")[0].strip()
                        return hostname
                    else:
                        return None
                except gw.PyGetWindowException:
                    return None
            elif platform.system() == "Linux":
                try:
                    active_window = ewmh.getActiveWindow()
                    if active_window:
                        window_class = active_window.get_wm_class()
                        window_name = active_window.get_wm_name()
                        hostname = f"{window_class[0]} - {window_name}".split(" - ")[
                            0
                        ].strip()
                        return hostname
                    else:
                        return None
                except ewmh.EWMHException:
                    return None
            elif platform.system() == "Darwin":
                # try:
                # from AppKit import NSWorkspace
                #     active_app_name = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
                #     return active_app_name
                # except ImportError:
                #     return None
                try:
                    active_app_name = subprocess.check_output(
                        [
                            "osascript",
                            "-e",
                            'tell application "System Events" to name of first application process whose frontmost is true',
                        ]
                    ).strip()
                    return active_app_name
                except subprocess.CalledProcessError:
                    pass
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"

    def load_icon_with_margin(self, image_path, width, height, margin):
        """Loads, resizes, and adds a transparent margin to an icon."""
        try:
            img = Image.open(image_path)
            img = img.resize((width, height), Image.LANCZOS)
            img_with_margin = Image.new(
                "RGBA", (width + 2 * margin, height + 2 * margin), (255, 255, 255, 0))
            img_with_margin.paste(img, (margin, margin))
            return ImageTk.PhotoImage(img_with_margin)
        except Exception as e:
            print(f"Error loading image '{image_path}': {e}")
            return None


    def resize_image(self, image_path, width, height, margin):
        img = Image.open(image_path)
        img = img.resize((width, height))
        img_with_margin = Image.new(
            "RGBA", (width + 2 * margin, height + 2 * margin), (255, 255, 255, 0)
        )
        img_with_margin.paste(img, (margin, margin))
        return ImageTk.PhotoImage(img_with_margin), img_with_margin

    def resize_image2(self, image_path, width, height, margin):
        """Resize the image and add margins"""
        img = Image.open(image_path)
        img = img.resize((width, height))
        img_with_margin = Image.new(
            "RGBA", (width + 2 * margin, height + 2 * margin), (255, 255, 255, 0)
        )
        img_with_margin.paste(img, (margin, margin))
        return img_with_margin  # Return the raw PIL Image, not PhotoImage

    def resize_pause_image(self, image_path, width, height):
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

    def update_time(self):
        try:
            while self.is_timer_running:
                with self.update_time_lock:
                    # Update your time logic here
                    # For example, if you want to blink the colon
                    self.colon_label.config(
                        fg="white"
                        if self.colon_label.cget("fg") == "#0E4772"
                        else "#0E4772"
                    )

                time.sleep(1)  # Blink every second
        except Exception as e:
            print(f"An error occurred update_time: {e}")
            return "N/A"

    def update_timenew(self):
        try:
            blink = 0
            while self.is_timer_running:
                with self.update_time_lock:
                    blink += 1
                    if blink % 2 == 0:
                        self.colon_label.config(
                            fg="#0E4772"
                        )  # Make colon invisible (background color)
                    else:
                        self.colon_label.config(
                            fg="white"
                        )  # Make colon visible (white color)

                time.sleep(1)  # Blink every second

        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"

    def update_timeMy(self):
        try:
            while self.is_timer_running:
                with self.update_time_lock:
                    blink = 0
                    blink += 1
                    if ":" in self.dailytime:
                        self.dailytime = self.dailytime.replace(":", " ")
                    else:
                        self.dailytime = self.dailytime.replace(" ", ":")
                    self.dailytime_label.config(text=self.dailytime)
                time.sleep(1 - time.time() % 1)

                # self.update_time_lock.start()
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"


    def update_User_status(self):
        if self.is_timer_running:
            try:
                with self.update_User_status_lock:
                    current_time = datetime.datetime.now(pytz.UTC)
                    data = {
                        "createdAt": current_time,
                    }
                    api_url = "https://myuniversallanguages.com:9093/api/v1"
                    headers = { 
                        "Authorization": "Bearer " + self.token,
                    }

                    response = requests.post(
                        f"{api_url}/timetrack/updateUserStatus",
                        headers=headers,
                        data=data
                    )

                    if response.ok:
                        data = response.json()
                        print("status update")

                    else:
                        return None

            except Exception as e:
                print(f"Error occured while updating user status: {e}")
                return None

    def update_daily_time(self):
        if self.is_timer_running:
            try:
                with self.update_daily_time_lock:
                    # if ":" in self.dailytime:
                    #     self.dailytime = self.dailytime.replace(":", " ")
                    # data = self.dailytime

                    # # Split the data into hour and minute parts
                    # parts = data.split()

                    # # Extract hours and minutes
                    # hour_part = parts[0]  # "1h"
                    # minute_part = parts[1]  # "24m"

                    # Remove the "h" and "m" characters to get the numeric values
                    # Remove the last character "h" and convert to an integer
                    hour = int(self.hours)
                    # Remove the last character "m" and convert to an integer
                    minute = int(self.minutes)

                    # Simulate time passing, add 1 minute in a loop
                    minute += 1

                    if minute >= 60:
                        hour += 1
                        minute -= 60

                    # Format the updated time back into the "1h 24m" format
                    self.hours = f"{hour:02d}"  # Ensures two digits, e.g., "01" for 1
                    self.minutes = f"{minute:02d}"  # Ensures two digits, e.g., "09" for 9
                    self.dailytime = f"{hour} {minute}"
                    # self.dailytime_label.config(text=self.dailytime)
                    print("Updated Time:", self.dailytime)
                    self.hoursLength()
                    self.update_User_status()

            except Exception as e:
                print(f"Error occured while fetching data: {e}")
                return None


    #     if not self.calledImmediate:
    #         threading.Thread(target=self.fetch_data).start()
    #         self.root.after(300000, self.get_data)

    def fetch_data(self):
        try:
            print("hello fetch data")
            if not self.calledImmediate:
                with self.fetch_data_lock:
                    if not self.token:
                        print("❗Token not found. You must login first.")
                        return None
                    api_url = "https://myuniversallanguages.com:9093/api/v1"

                    headers = {
                        "Authorization": "Bearer " + self.token,
                        "Content-Type": "application/json",
                    }

                    response = requests.get(
                        f"{api_url}/timetrack/hours", headers=headers
                    )
                    json_data = response.json()
                    if response.ok:
                        
                        data = json_data["data"]
                        self.dailytime = data["totalHours"]["daily"]

                        # Extract hours and minutes from the string (e.g., '0h 22m')
                        time_parts = self.dailytime.split(" ")  # Split the string by spaces
                        self.hours = time_parts[0].replace("h", "").zfill(2)  # Remove 'h' and pad with zero
                        self.minutes = time_parts[1].replace("m", "").zfill(2)  # Remove 'm' and pad with zero
                        self.hoursLength()
                    else:
                        print(
                            f"Failed to get data: {response.status_code} - {response.text}"
                        )
                      # Check if the user is not logged in or if the message indicates the user doesn't exist
                        # Check if the user is not logged in, access is blocked, or the user is archived
                        if (
                            not json_data.get("loggedIn", True) or
                            json_data.get("accessBlock", False) or
                            json_data.get("isArchived", False) or
                            "user not exists" in json_data.get("Message", "").lower()
                        ):
                            print("User access blocked, archived, or not logged in. Logging out...")

                            # List of files to delete
                            files_to_remove = [
                                'screenshots_data.pkl',
                                'trackingStart_list.pkl',
                                'trackingStop_list.pkl',
                                'breakData.pkl',
                                'breakUsed.pkl',
                                'new_data.pkl'
                            ]

                            # Attempt to remove each file
                            for file in files_to_remove:
                                file_path = GUIApp.get_data_file_path(file)
                                try:
                                    os.remove(file_path)
                                except FileNotFoundError:
                                    print(f"File not found: {file_path}")  # Ignore missing files
                                except Exception as e:
                                    print(f"Error deleting {file_path}: {e}")

                            self.logout()
                            return  # Exit function early

        except Exception as e:
            print(f"Error occured while fetching sdata: {e}")
            return None
            # self.root.after(300000, self.get_data)


    def hoursLength(self):
        # self.hours = '2h'
        # self.minutes = '22m'
        # Set the text of the labels accordingly
        self.hour_label.setStringValue_(str(self.hours))
        self.minute_label.setStringValue_(str(self.minutes))

        # Place the labels initially at arbitrary positions
        # self.hour_label.place(x=320, y=47)

        if len(self.hours) == 3 and len(self.minutes) == 3:
            colon_x = (
                320 + 62
            )  # Adjust for single-digit hour (add 30 pixels to x) diff 62
            minute_x = (
                colon_x + 17
            )  # Adjust minute label (15 pixels after colon) diff 17
        elif len(self.hours) == 2 and len(self.minutes) == 2:
            colon_x = 320 + 42  # Adjust for single-digit hour (add 30 pixels to x)
            minute_x = colon_x + 17  # Adjust minute label (15 pixels after colon)
        elif len(self.hours) == 3 and len(self.minutes) == 2:
            colon_x = 320 + 62  # Adjust for double-digit hour (add 50 pixels to x)
            minute_x = colon_x + 17  # Adjust minute label (15 pixels after colon)
        elif len(self.minutes) == 3 and len(self.hours) == 2:
            colon_x = 320 + 42  # Adjust for double-digit hour (add 50 pixels to x)
            minute_x = colon_x + 17  # Adjust minute label (15 pixels after colon)

        # Adjust positions based on the length of hours
        # if len(self.hours) == 2:  # Single-digit hour
        #     colon_x = 320 + 57  # Adjust for single-digit hour (add 30 pixels to x)
        #     minute_x = colon_x + 15  # Adjust minute label (15 pixels after colon)
        # else:  # Double-digit hour
        #     colon_x = 320 + 65  # Adjust for double-digit hour (add 50 pixels to x)
        #     minute_x = colon_x + 15  # Adjust minute label (15 pixels after colon)

        # if len(self.minutes) == 3:  # Single-digit hour
        #     colon_x = 320 + 67  # Adjust for single-digit hour (add 30 pixels to x)
        #     minute_x = colon_x + 22  # Adjust minute label (15 pixels after colon)
        # else:  # Double-digit hour
        #     colon_x = 320 + 60  # Adjust for double-digit hour (add 50 pixels to x)
        #     minute_x = colon_x + 15  # Adjust minute label (15 pixels after colon)

        # Place the colon and minute labels
        # self.colon_label.place(x=colon_x, y=47)
        # self.minute_label.place(x=minute_x, y=47)

    def schedule_update_check(self):
        # Call check_for_update to perform the update check
        self.check_for_update()

        # Schedule the next update check after 1 hour
        # threading.Timer(3600, self.schedule_update_check).start()

    def check_for_update(self):
        with self.check_for_update_lock:
            api_url = "https://myuniversallanguages.com:9093/api/v1"
            headers = {"Content-Type": "application/json"}

            try:
                response = requests.get(
                    f"{api_url}/timetrack/getSiliconFile", headers=headers
                )
                if response.ok:
                    json_data = response.json()
                    data = json_data["data"]
                    self.latest_v = data["version"]
                    self.url = data["url"]

                    if self.latest_v == self.current_v:
                        self.updated = False
                    elif self.latest_v > self.current_v:
                        self.updated = True
                else:
                    print("Error: Failed to check for updates.")
            except Exception as e:
                print(f"An error occurred: {e}")
                return "N/A"

    def download_new_version(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            if os.path.exists("SSTRACKAppleSetup1.1.19.dmg"):
                os.remove("SSTRACKAppleSetup1.1.19.dmg")
            with open("SSTRACKAppleSetup1.1.19.dmg", "wb") as new_file:
                new_file.write(response.content)
                self.download = True
            print("SSTRACKAppleSetup1.1.19.dmg downloaded successfully.")

            try:
                os.remove(GUIApp.get_data_file_path("data.pkl"))
                # os.remove("data.pkl")
            except FileNotFoundError:
                pass

            try:
                os.remove(GUIApp.get_data_file_path("time_entry_id.pkl"))
                # os.remove("time_entry_id.pkl")
            except FileNotFoundError:
                pass

            # Restart the main.py script as a new process
            subprocess.Popen(["open", "SSTRACKAppleSetup1.1.19.dmg"])


        else:
            print("Failed to download SSTRACKAppleSetup1.1.19.dmg.")

    def show_loading_message(self):
        self.loading_popup = tk.Toplevel(self.root)
        self.loading_popup.wm_attributes("-topmost", True)
        self.loading_popup.title("Downloading Update")
        tk.Label(
            self.loading_popup, text="Please wait while we downloading your file..."
        ).pack(padx=40, pady=40)

    # def set_icon(self, icon_path):
    #     if os.path.exists(icon_path):
    #         self.window.Icon = icon_path

    def set_taskbar_icon(self, icon_path):
        # Set the taskbar icon using WM_SETICON message
        # (Only works on Windows)
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        icon = ctypes.windll.shell32.ExtractIconW(0, icon_path, 0)
        ctypes.windll.user32.SendMessageW(hwnd, 0x80, 1, icon)
        print(f"Taskbar icon set to: {icon_path}")

    def start_Timer(self):
        try:
            
            with self.play_timer_lock:
                # if os.path.isfile('trackingStart_list.pkl'):
                if os.path.isfile(GUIApp.get_data_file_path("trackingStart_list.pkl")):
                    with open(GUIApp.get_data_file_path("trackingStart_list.pkl"), "rb") as f:
                        self.trackingStart_list = pickle.load(f)

                        if len(self.trackingStart_list) > 0:
                            index = 0
                            while index < len(self.trackingStart_list):
                                startTracking = self.trackingStart_list[index]

                                uniqueId = startTracking['timeEntryId']
                          
                                api_url = "https://myuniversallanguages.com:9093/api/v1"

                                headers = {
                                    "Authorization": "Bearer " + self.token,
                                }

                                response = requests.post(
                                    f"{api_url}/timetrack/addd",
                                    headers=headers,
                                    data=startTracking,
                                )
                                print("API Response Status:", response.status_code)
                                if response.ok:

                                    data = response.json()

                                    print("timer start")
                                    timeEntry = data["data"]
                                    timeentryid = timeEntry
                                    # delete index from start timer list
                                    # Remove the first item from the list
                                    self.trackingStart_list.pop(0)
                                    # Reset index to 0
                                    index = 0

                                    with open(GUIApp.get_data_file_path("trackingStart_list.pkl"), "wb") as f:
                                        pickle.dump(self.trackingStart_list, f)
                                    # Checking if the pickle file exists

                                    if os.path.isfile(GUIApp.get_data_file_path("time_entry_id.pkl")):
                                        # Loading the previous time entry ID from the pickle file
                                        with open(GUIApp.get_data_file_path("time_entry_id.pkl"), "rb") as f:
                                            previousTimeEntryId = pickle.load(
                                                f)

                                            # Checking if the previous time entry ID matches the current one
                                        if previousTimeEntryId == uniqueId:
                                            # Writing the current time entry ID to the pickle file
                                            with open(GUIApp.get_data_file_path("time_entry_id.pkl"), "wb") as f:
                                                pickle.dump(timeentryid, f)

                                    # ======== read screenshots data and replace id =========== #
                                    if os.path.isfile(GUIApp.get_data_file_path("screenshots_data.pkl")):
                                        with open(GUIApp.get_data_file_path("screenshots_data.pkl"), "rb") as f:
                                            screenshotsData = pickle.load(f)

                                        # Check if screenshotsData contains any data
                                        if screenshotsData:
                                            # Iterate over the data
                                            for entry in screenshotsData:
                                                # Assuming entry has a key 'timeEntry'
                                                timeEntry = entry.get('timeEntryId')
                                                if timeEntry == uniqueId:
                                                    # Replace timeEntry with timeEntryId
                                                    entry['timeEntryId'] = timeentryid

                                            # Save the modified data back to the pickle file
                                            with open(GUIApp.get_data_file_path("screenshots_data.pkl"), "wb") as f:
                                                pickle.dump(screenshotsData, f)

                                    # ========= read stop Timer list data and replace id =========== #
                                    # if os.path.isfile("trackingStop_list.pkl"):
                                    if os.path.isfile(GUIApp.get_data_file_path("trackingStop_list.pkl")):
                                        with open(GUIApp.get_data_file_path("trackingStop_list.pkl"), "rb") as f:
                                            trackerStopList = pickle.load(f)

                                        if trackerStopList:
                                            for stop in trackerStopList:
                                                timeEntry = stop.get(
                                                    'timeEntryId')
                                                if timeEntry == uniqueId:

                                                    # Replace timeEntry with timeEntryId
                                                    stop['timeEntryId'] = timeentryid

                                            with open(GUIApp.get_data_file_path("trackingStop_list.pkl"), "wb") as f:
                                                pickle.dump(trackerStopList, f)

        except Exception as error:
            print("error start timmer:", error)
            return None

#
#    # Modify the click_play_button method to accept the event argument
    def click_play_button(self, event=None):
        try:
            print("play button")
            # Change the icon to indicate the running state
            # self.root.iconphoto(True, self.official_icon)
            # self.root.wm_iconbitmap(self.resource_path("images/animatedlogo.ico"))
            # self.set_icon("images/animatedlogo.ico")
            if self.updated:
                confirmation = messagebox.askyesno(
                    "Confirm Update", "A new version is available. Do you want to update?"
                )
                if confirmation:
                    self.download_new_version()
                    if self.download:
                        os.system("taskkill /f /im SSTRACK.exe")
                else:
                    # Destroy the current window
                    self.root.destroy()
                    # Restart the main.py script as a new process
                    subprocess.Popen([self.python_exe, "main.py"])
            else:
                if not self.updated:
                    self.exact_time = datetime.datetime.now(pytz.UTC)
                    self.playTime = datetime.datetime.now(pytz.UTC)
                    # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
                    if not self.is_timer_running:
                        self.is_timer_running = True
                        self.total = 0
                       
                        threading.Thread(target=self.update_time).start()

                        # self.play_button.config(state=tk.DISABLED)
                        # self.pause_button.config(state=tk.NORMAL)
                        # Change play button image to play_icon_grey
                      

                        # Other logic for starting the timer or performing actions goes here, 40, 10)  # Move pause button up to play position (e.g., x=40, y=5)

                        # Continue with the rest of your logic
                        self.current_date = datetime.date.today()
                        # Run the system tray in a separate thread
                        # self.start_tray()
                        # threading.Thread(target=self.run_tray, daemon=True).start()
                        # threading.Thread(
                        #     target=self.employeeSetting).start()
                        threading.Thread(target=self.handle_sleep_mode).start()
                        threading.Thread(target=self.check_activity).start()
                        self.total_intervals = 0
                        self.active_intervals = 0
                        # self.get_data()

                        # Check if the file exists before reading from it
                        # Check if the file exists
                        if os.path.isfile(GUIApp.get_data_file_path("trackingStart_list.pkl")):
                            # Check if the file is empty
                            if os.path.getsize(GUIApp.get_data_file_path("trackingStart_list.pkl")) > 0:
                                with open(GUIApp.get_data_file_path("trackingStart_list.pkl"), "rb") as f:
                                    # Load trackingStart_list from the file
                                    self.trackingStart_list = pickle.load(f)
                            else:
                                # If the file is empty, initialize trackingStart_list as an empty list
                                self.trackingStart_list = []
                        else:
                            # If the file doesn't exist, initialize trackingStart_list as an empty list
                            self.trackingStart_list = []

                        unique_id = str(uuid.uuid4())
                        # unique_id='b9dd81d6-a959-4916-b628-d80223e5cb70'
                        # self.playTime = datetime.datetime.now(pytz.UTC)

                        trackingstart = {
                            "projectId": self.projectId,
                            "description": self.description,
                            "startTime": self.playTime,
                            "userId": self.user_id,
                            "timeEntryId": unique_id,
                        }

                        try:
                            # Append tracking start data to the list
                            self.trackingStart_list.append(trackingstart)

                            # Save the updated list to the file
                            with open(GUIApp.get_data_file_path("trackingStart_list.pkl"), "wb") as f:
                                pickle.dump(self.trackingStart_list, f)

                            # Save the time entry ID to a separate file
                            with open(GUIApp.get_data_file_path("time_entry_id.pkl"), "wb") as f:
                                pickle.dump(unique_id, f)

                            print("Tracking start data saved successfully.")
                            # self.minimize_window()
                        
                        
                            message = ""
                            if self.description:
                                message = self.description

                            # Include project name in the notification message
                            if hasattr(self, 'selected_project_name') and self.selected_project_name and self.selected_project_name != "no project":  # Check if projectName exists and is not empty
                                project_name = self.selected_project_name.upper()  # Convert projectName to uppercase
                                message = f"{project_name}\n{message}"

                            if self.breakActive:
                                self.popActive=True
                                self.breakActive = False
                               
                                os.system('terminal-notifier -title "SSTRACK started" -message "Your break has been stopped. SSTRACK is started." -appIcon "images/animatedlogo.png"')
                               
                            else:
                           
                                os.system('terminal-notifier -title "SSTRACK started" -message "SSTRACK started" -appIcon "images/animatedlogo.png"')
                            # Start the timer in a separate thread
                            threading.Thread(target=self.setUpBreak).start()

                        except Exception as e:
                            print("Failed to save tracking start data:", e)
                            return None
        
        except Exception as e:
            print("Failed to start SSTRACK:", e)
            return None
        
        
    def setUpBreak(self):
        try:
            # self.break_button.config(
            #                 text="Break",
            #                 bg="#E8F4FC",  # Initial background color
            #                 fg="#7094B0",  # White text when break ends
            # )
                    
            # if os.path.isfile("breakData.pkl"):
            if os.path.isfile(GUIApp.get_data_file_path("breakData.pkl")):
                with open(GUIApp.get_data_file_path("breakData.pkl"), "rb") as f:
                    self.breakData = pickle.load(f)

            # Load existing break data if the file exists
            if os.path.isfile(GUIApp.get_data_file_path("breakUsed.pkl")):
                with open(GUIApp.get_data_file_path("breakUsed.pkl"), "rb") as f:
                    self.breakUsed = pickle.load(f)

            self.playTime = datetime.datetime.now(pytz.UTC)
            if self.breakActive:
                self.breakActive = False
                # self.breakEndOn=playTime
                self.breakUsed["breakEndOn"] = self.playTime
            if self.breakUsed:
                self.breakData.append(self.breakUsed)
                self.break_button.config(
                            text="Break",
                            bg="#E8F4FC",  # Initial background color
                            fg="#7094B0",  # White text when break ends
                        )
                # Save the updated data to `breakData.pkl`
                with open(GUIApp.get_data_file_path("breakData.pkl"), "wb") as f:
                    pickle.dump(self.breakData, f)

                # Remove `breakUsed.pkl` after processing
                if os.path.isfile(GUIApp.get_data_file_path("breakUsed.pkl")):
                    os.remove(GUIApp.get_data_file_path("breakUsed.pkl"))
            if self.is_timer_running:
                self.start_Timer()
            self.breakExecution()
                    
            # Create a notifier object
            # message = 'no note'
            # if self.description:
            #     message = self.description
                       
            # # Display a notification with an icon
            # notification.notify(
            #     title="SSTRACK started",
            #     message=message,
            #     timeout=3,  # Notification disappears after 3 seconds
            #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
            # ) 
            #   # Start the timer in a separate thread
            # threading.Thread(target=self.start_Timer).start()
            # threading.Thread(target=self.breakExecution).start()
        except Exception as error:
            print(error)
            return None

    def stop_Timer(self):
        try:
            with self.stop_timer_lock:
                if os.path.isfile(GUIApp.get_data_file_path("trackingStop_list.pkl")):
                    with open(GUIApp.get_data_file_path("trackingStop_list.pkl"), "rb") as f:
                        self.trackingStop_list = pickle.load(f)

                if self.trackingStop_list:
                    index = 0
                    while index < len(self.trackingStop_list):
                        stoptracking = self.trackingStop_list[index]
                        entryId = stoptracking["timeEntryId"]

                        api_url = "https://myuniversallanguages.com:9093/api/v1"

                        headers = {
                            "Authorization": "Bearer " + self.token,
                        }

                        response = requests.patch(
                            f"{api_url}/timetrack/edit/{entryId}",
                            headers=headers,
                            data=stoptracking,  # Use the json parameter to send JSON data in the request body
                        )
                        if response.ok:
                            if self.trackingStop_list:
                                del self.trackingStop_list[0]
                                index = 0
                                with open(GUIApp.get_data_file_path("trackingStop_list.pkl"), "wb") as f:
                                    pickle.dump(self.trackingStop_list, f)
                            # data = response.json()
                            print("Timer stopped:")
                        else:
                            print("Failed to stop the timer")
                            break

        except Exception as error:
            print(error)
            return None

    def click_pause_button(self, event=None):
        self.root.wm_iconbitmap(self.resource_path("images/pauseico.ico"))
        try:
            with self.click_pause_button_lock:
                if self.is_timer_running:
                    self.is_timer_running = False

                    if hasattr(self, 'icon') and isinstance(self.icon, Icon):
                        self.icon.stop()
                        print("Tray icon removed.")
                    else:
                        print("Tray icon is not initialized or not of type 'Icon'")

                # Attempt to load time_entry_id.pkl
                try:
                    with open(GUIApp.get_data_file_path("time_entry_id.pkl"), "rb") as f:
                        timeEntryId = pickle.load(f)
                except (FileNotFoundError, EOFError):
                    print("Error: time_entry_id.pkl not found or is empty.")
                    return None

                # Initialize or load trackingStop_list.pkl
                self.trackingStop_list = []
                if os.path.isfile(GUIApp.get_data_file_path("trackingStop_list.pkl")):
                    try:
                        with open(GUIApp.get_data_file_path("trackingStop_list.pkl"), "rb") as f:
                            self.trackingStop_list = pickle.load(f)
                    except EOFError:
                        print("Error: trackingStop_list.pkl is empty. Initializing a new list.")
                        self.trackingStop_list = []

                # Add new tracking stop data
                current_time = self.exact_time if self.sleep_mode else datetime.datetime.now(pytz.UTC)
                trackingstop = {"endTime": current_time, "timeEntryId": timeEntryId}
                self.trackingStop_list.append(trackingstop)

                # Save updated trackingStop_list.pkl
                with open(GUIApp.get_data_file_path("trackingStop_list.pkl"), "wb") as f:
                    pickle.dump(self.trackingStop_list, f)

                # Update UI components
                self.canvas.itemconfig(self.play_button, image=self.play_icon)
                self.canvas.itemconfig(self.pause_button, image=self.pause_icon_grey)
                self.canvas.tag_unbind(self.pause_button, "<Button-1>")
                self.canvas.tag_bind(self.play_button, "<Button-1>", self.click_play_button)
                self.canvas.lift(self.play_button)
                if not self.breakActive:

                    message = ""
                    if self.description:
                        message = self.description

                    # Include project name in the notification message
                    if hasattr(self, 'selected_project_name') and self.selected_project_name and self.selected_project_name != "no project":  # Check if projectName exists and is not empty
                        project_name = self.selected_project_name.upper()  # Convert projectName to uppercase
                        message = f"{project_name}\n{message}"
                                
                    # Display a notification with an icon
                    # Notifier.notify(
                    #     title="SSTRACK stopped",
                    #     message=message,
                    #     timeout=3,  # Notification disappears after 3 seconds
                    #     app_icon="images/logopause.ico"  # Provide the path to your icon file (e.g., .ico or .png)
                    # )
                    os.system('terminal-notifier -title "SSTRACK started" -message "SSTRACK stopped" -appIcon "images/animatedlogo.png"')
                # Break handling
                self.total_intervals = 0
                self.active_intervals = 0
                self.breakStartedOn = current_time
                onlytime = current_time.strftime("%H:%M:%S")
                # if self.is_break_time_valid(self.BreakTime):
                #     if self.puncEndTime > onlytime:
                #         self.breakId = str(uuid.uuid4())
                #         self.breakActive = True
                if self.popActive:
                    self.popActive = False
                    threading.Thread(target=self.getBreaktimes).start()

                # Start timer stopping thread
                threading.Thread(target=self.stop_Timer).start()
                # self.stop_Timer()

        except Exception as e:
            print(f"An error occurred click_pause_button: {e}")

    def restartTimer(self):
        try:
            with open(GUIApp.get_data_file_path("time_entry_id.pkl"), "rb") as f:
                timeEntryId = pickle.load(f)

            message = ""
            if self.description:
                message = self.description

            # Include project name in the notification message
            if hasattr(self, 'selected_project_name') and self.selected_project_name and self.selected_project_name != "no project":  # Check if projectName exists and is not empty
                project_name = self.selected_project_name.upper()  # Convert projectName to uppercase
                message = f"{project_name}\n{message}"


            # Display a notification with an icon
            # Notifier.notify(
            #     title="SSTRACK started",
            #     message=message,
            #     timeout=3,  # Notification disappears after 3 seconds
            #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
            # )
            os.system('terminal-notifier -title "SSTRACK started" -message "SSTRACK started" -appIcon "images/animatedlogo.png"')
            self.trackingStop_list = []
            if os.path.isfile(GUIApp.get_data_file_path("trackingStop_list.pkl")):
                with open(GUIApp.get_data_file_path("trackingStop_list.pkl"), "rb") as f:
                    self.trackingStop_list = pickle.load(f)

            if self.sleep_mode:
                current_time = self.exact_time
            else:
                current_time = datetime.datetime.now(pytz.UTC)
            trackingstop = {"endTime": current_time, "timeEntryId": timeEntryId}
            self.trackingStop_list.append(trackingstop)
            with open(GUIApp.get_data_file_path("trackingStop_list.pkl"), "wb") as f:
                pickle.dump(self.trackingStop_list, f)

            ############## Timer Start
            unique_id = str(uuid.uuid4())
            # unique_id='b9dd81d6-a959-4916-b628-d80223e5cb70'
            self.playTime = datetime.datetime.now(pytz.UTC)

            trackingstart = {
                "projectId": self.projectId,
                "description": self.description,
                "startTime": self.playTime,
                "userId": self.user_id,
                "timeEntryId": unique_id,
            }

            # Append tracking start data to the list
            self.trackingStart_list.append(trackingstart)

            # Save the updated list to the file
            with open(GUIApp.get_data_file_path("trackingStart_list.pkl"), "wb") as f:
                pickle.dump(self.trackingStart_list, f)

            # Save the time entry ID to a separate file
            with open(GUIApp.get_data_file_path("time_entry_id.pkl"), "wb") as f:
                pickle.dump(unique_id, f)

            # Start the timer in a separate thread
            self.start_Timer()
        except Exception as e:
            print(f"An error occurred restartTimer: {e}")
            return "N/A"


   

    def can_display_notification(self):
        current_time = time.time()
        # Check if the last notification was shown more than `notification_timeout` seconds ago
        if current_time - self.last_notification_time >= self.notification_timeout:
            self.last_notification_time = current_time
            return True
        return False

    def click_break_button(self, event=None):
        if not self.break_button_enabled:
            self.break_button_enabled = True
            print("Break button is disabled. Click ignored.")
              # Display a notification with an icon
            # Notifier.notify(
            #     title="Break stopped",
            #     message="Your break has stopped",
            #     timeout=3,  # Notification disappears after 3 seconds
            #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
            # )
            os.system('terminal-notifier -title "SSTRACK started" -message "Break stopped" -appIcon "images/animatedlogo.png"')
            # self.setUpBreak()
            threading.Thread(target=self.setUpBreak, daemon=True).start()
            return

        if self.breakFound and self.parse_remaining_break_time(self.BreakTime) > 1:
            try:
                self.breakActive = True
                self.breakStartedOn = datetime.datetime.now(pytz.UTC)

                # Disable the break button
                self.break_button_enabled = False

                # Display a notification with an icon
                if self.can_display_notification():
                    # Notifier.notify(
                    #     title="Break started",
                    #     message="Your break has started",
                    #     timeout=3,
                    #     app_icon="images/animatedlogo.ico"
                    # )
                    os.system('terminal-notifier -title "SSTRACK started" -message "break started" -appIcon "images/animatedlogo.png"')
                self.breakId = str(uuid.uuid4())

                # Start `startBreakTime` in a separate thread
                threading.Thread(target=self.startBreakTime, daemon=True).start()
            except Exception as e:
                print(f"Error starting break time: {e}")

        elif self.breakFound and self.parse_remaining_break_time(self.BreakTime) < 1:
            if self.can_display_notification():
                # Display a notification with an icon
                # Notifier.notify(
                #     title="Break Time",
                #     message="The assigned break time has already been utilized",
                #     timeout=3,
                #     app_icon="images/animatedlogo.ico"
                # )
                os.system('terminal-notifier -title "SSTRACK started" -message "BThe assigned break time has already been utilized" -appIcon "images/animatedlogo.png"')
        elif not self.breakFound:
            if self.can_display_notification():
                # Display a notification with an icon
                # Notifier.notify(
                #     title="Break Time",
                #     message="No break time has been assigned by the company.",
                #     timeout=3,
                #     app_icon="images/animatedlogo.ico"
                # )
                os.system('terminal-notifier -title "SSTRACK started" -message "No break time has been assigned by the company." -appIcon "images/animatedlogo.png"')

    def on_closing(self):
        try:
            if self.is_timer_running:
                confirm = messagebox.askyesno(
                    "App Closing", "Are you sure you want to stop the SSTRACK?"
                )
                if confirm:
                    self.click_pause_button()
                    # Close the main.py script
                    try:
                        os.system("taskkill /f /im SSTRACK.exe")
                        self.root.destroy()  # Close the application window
                        # Close all running Python processes
                    except Exception as e:
                        print("Error:", e)
                        return None
            else:
                os.system("taskkill /f /im SSTRACK.exe")
                self.root.destroy()
        except Exception as e:
            os.system("taskkill /f /im SSTRACK.exe")
            self.root.destroy()
            print(f"An error occurred: {e}")
            return "N/A"

    @objc.typedSelector(b"v@:@")
    def logout_(self, sender):
        print("🚪 Logout button clicked")

        # --- 1. Stop timer if running ---
        if hasattr(self, "is_timer_running") and self.is_timer_running:
            self.pauseButtonClicked_(None)

        # --- 2. Remove session files ---
        try:
            os.remove(GUIApp.get_data_file_path("data.pkl"))
        except FileNotFoundError:
            pass

        try:
            os.remove(GUIApp.get_data_file_path("time_entry_id.pkl"))
        except FileNotFoundError:
            pass

        # --- 3. Close current window ---
        if hasattr(self, "window"):
            self.window.close()

        # --- 4. Relaunch login.py ---
        try:
            python_executable = sys.executable  # Current venv Python path
            script_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory
            login_script_path = os.path.join(script_dir, "login.py")  # Full path to login.py

            # Launch login.py
            subprocess.Popen([python_executable, login_script_path])

            print("🔄 Relaunching login window...")

            # --- 5. Quit current app safely ---
            NSApplication.sharedApplication().terminate_(self)

        except Exception as e:
            print("❌ Failed to relaunch login:", e)

    
    def handle_sleep_mode(self):
        """Continuously monitors system state and triggers sleep mode or break time."""
        last_break_triggered_time = None  # Track the last time a break was triggered

        while self.is_timer_running:
            with self.handle_sleep_mode_lock:
                currenttime = datetime.datetime.now(pytz.UTC)
                print(f"Exact Time: {self.exact_time}, Current Time: {currenttime}")

                # Convert currenttime into user's timezone based on timezoneOffset
                # Convert timezoneOffset to int (or float if fractional offsets are possible)
                timezone_offset_str = self.user_info.get('timezoneOffset', '0')  # Default to '0' if not provided
                try:
                    self.timezone_offset = int(timezone_offset_str)  # Convert to int
                except ValueError:
                    print(f"Invalid timezone offset: {timezone_offset_str}. Defaulting to UTC.")
                    self.timezone_offset = 0  # Default to UTC if conversion fails
                user_timezone = datetime.timezone(datetime.timedelta(hours=self.timezone_offset))
                currenttime_user = currenttime.astimezone(user_timezone)

                # print(f"Exact Time (UTC): {self.exact_time}, Current Time (User Timezone): {currenttime_user}")

                three_minutes_ago = currenttime_user - datetime.timedelta(minutes=3)
                
                # remove 1st breakTime 
                if self.popActive and self.breakConvertedData:
                    self.breakConvertedData.pop(0)
                if self.breakConvertedData:  # Check if breakConvertedData is not None or empty

                    for break_period in self.breakConvertedData:
                        breakStartTime = break_period.get("breakStartTime")  # String with timezone info
                        try:
                            # Parse the break start time into a datetime object and convert to UTC
                            breakStartTime_dt = parser.isoparse(breakStartTime).astimezone(pytz.UTC)
                            
                            # Truncate to hour and minute only (removing seconds and microseconds)
                            breakStartTime_dt = breakStartTime_dt.replace(second=0, microsecond=0)
                            currenttime_truncated = currenttime_user.replace(second=0, microsecond=0)


                            # Compare only the truncated hour and minute, and ensure the break is triggered only once per minute
                            # Compare only the hour and minute
                            if (breakStartTime_dt.hour == currenttime_truncated.hour and
                                breakStartTime_dt.minute == currenttime_truncated.minute and
                                last_break_triggered_time != currenttime_truncated):
                                self.breakEndTime = break_period.get("breakEndTime")
                                if self.parse_remaining_break_time(self.BreakTime) > 1:
                                    print("It's break time!")
                                    # Display a notification with an icon
                                    # Notifier.notify(
                                    #     title="Break started",
                                    #     message="your break has started",
                                    #     timeout=3,  # Notification disappears after 3 seconds
                                    #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
                                    # )
                                    os.system('terminal-notifier -title "SSTRACK started" -message "Break Started" -appIcon "images/animatedlogo.png"')
                                    self.breakStartedOn =self.exact_time
                                    self.breakActive=True
                                    self.breakId = str(uuid.uuid4())
                                    threading.Thread(target=self.startBreakTime).start()
                                    threading.Thread(target=self.stop_break).start()
                                    last_break_triggered_time = currenttime_truncated  # Update the last triggered time
                        except Exception as e:
                            print(f"Error parsing break time: {breakStartTime}. Error: {e}")

                time_difference = currenttime - self.exact_time

                # Check if system has been in sleep mode for over 3 minutes
                if self.exact_time < three_minutes_ago:
                    if not self.sleep_mode:  # Avoid multiple triggers for the same sleep event
                        self.sleep_mode = True
                        print("Computer is in sleep mode")
                        threading.Thread(target=self.click_pause_button).start()

                        if time_difference.total_seconds() <= 2 * 60 * 60:  # Check if time difference is less than 2 hours
                            tkinter.messagebox.showinfo(
                                "SSTRACK Paused", 
                                "Your SStrack has been paused due to Sleep Mode.\nPlease start again!"
                            )

                # Update exact_time if the date has changed
                if self.exact_time.date() != currenttime.date():
                    self.exact_time = currenttime

                # Update exact_time to the current time if it's not in sleep mode
                if not self.sleep_mode:
                    self.exact_time = currenttime

            # Sleep for 1 second, ensuring alignment with the start of each second
            time.sleep(1 - time.time() % 1)

    #### socket

    def connect_to_server(self):
        print("Connecting to server...")
        try:
            self.sio.connect(
                "https://myuniversallanguages.com:9093", namespaces=["/"]
            )  # Adjust namespaces as per your server configuration
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return None

        @self.sio.event
        def connect():
            print("Connected to server")

        @self.sio.event
        def message(data):
            print(f"Received from server: {data}")

        @self.sio.event
        def disconnect():
            print("Disconnected from server")

        @self.sio.event
        def profile_update(data):
            try:
                print(f"Received profile update: {data}")
                if self.user_id == data.get("user", {}).get("_id"):
                    self.token = data.get("token")
                    with open("data.pkl", "wb") as f:
                        pickle.dump(self.token, f)
                        # Decode the Base64-encoded parts of the token
                        header, payload, signature = self.token.split(".")
                        decoded_payload = base64.urlsafe_b64decode(payload + "==").decode(
                            "utf-8"
                        )
                        self.user_info = json.loads(decoded_payload)
                        self.name = self.user_info["name"]
                        nameLength = len(self.name)
                                    # Format name based on length
                        if nameLength > 15:
                            self.name = (
                                self.name[:12] + "..."
                            )  # Take the first 16 characters and add "..."
                        else:
                            self.name = self.name  # Use the full name if it's 19 characters or less
                            
                        self.company = self.user_info["company"]
                        self.username.config(
                            text=self.name
                        )  # Assuming 'self.username' is the tkinter Label widget
            # Process the received data here
            except Exception as e:
                print(f"Failed to update profile: {e}")
                return None

        @self.sio.event
        def user_setting(data):
            userId = data.get("userId")
            if self.user_id == userId:
                self.settings = data
                self.updateSettings()

        @self.sio.event
        def users_settings(data):
            for setting in data:
                if self.user_id == setting.get("userId"):
                    self.settings = setting
                    self.updateSettings()

        @self.sio.event
        def user_archive(data):
            try:
                if self.user_id == data.get("userId"):
                    if data.get("archived"):
                        self.token = None
                        self.user_info = None
                        self.user_Data()
                        # Remove the data.pkl file if it exists
                        if os.path.exists("data.pkl"):
                            os.remove("data.pkl")

                            # Destroy the Tkinter root window
                            self.root.quit()
                            os.system("taskkill /f /im SSTRACK.exe")
                            # Restart the main.py script as a new process
                            subprocess.Popen([self.python_exe, "main.py"])
            except Exception as e:
                print(f"Failed to make user archive: {e}")
                return None

        @self.sio.event
        def role_update(data):
            if self.user_id == data.get("user", {}).get("_id"):
                self.token = data.get("token")
                with open("data.pkl", "wb") as f:
                    pickle.dump(self.token, f)
                    # self.user_Data()
                    # Decode the Base64-encoded parts of the token
                    header, payload, signature = self.token.split(".")
                    decoded_payload = base64.urlsafe_b64decode(payload + "==").decode(
                        "utf-8"
                    )
                    self.user_info = json.loads(decoded_payload)
                    self.name = self.user_info["name"]
                    self.company = self.user_info["company"]

        @self.sio.event
        def Update_version(data):
            self.latest_v = data
            if self.latest_v == self.current_v:
                self.updated = False
            elif self.latest_v > self.current_v:
                self.updated = True

        @self.sio.event
        def new_project(data):
            self.fetch_projects()
            userIds= data.get("allowedEmployees")
            for userId in userIds:
                if self.user_id == userId:
                    pro_name = data.get("name")
                    pro_id = data.get("_id")
                    if pro_name not in self.projects:
                        self.projects.append(pro_name)
                        self.project_map.append(
                            {"projectname": pro_name, "projectid": pro_id}
                        )

        @self.sio.event
        def punctuality_settings(data):
            self.getRemainingBreakTime()
            self.getBreaktimes()

        @self.sio.event
        def assign_project(data):
            self.fetch_projects()

        @self.sio.event
        def archive_project(data):
            try:
                with self.archive_project_lock:
                    # self.fetch_projects()
                    # Since `data` directly contains the projectId, no need to use `data.get()`
                    # pro_id = data  # Directly use `data` as the projectId

                    project_id = data.get("projectId")
                    is_archived = data.get("isArchived")
                    project_name = data.get("projectName")
                    
                    # remove project if it's archived
                    if is_archived:
                        self.projects = [proj for proj in self.projects if proj != project_name]
                        self.project_map = [
                            proj for proj in self.project_map if proj["projectid"] != project_id
                        ]
                    # add project if it's not archived
                    else:
                        if project_name not in self.projects:
                            self.projects.append(project_name)
                        if not any(proj["projectid"] == project_id for proj in self.project_map):
                            self.project_map.append({
                                "projectname": project_name,
                                "projectid": project_id,
                            })
                    
                    self.update_projects_dropdown()  # Update dropdown with new projects
            except Exception as e:
                print(f"failed to apply archive socket: {e}")
                return None
                


        @self.sio.event
        def delete_project(data):
            # self.fetch_projects()

            project_id = data.get("projectId")
            project_name = data.get("projectName")
            
            # remove project if it's archived
            self.projects = [proj for proj in self.projects if proj != project_name]
            self.project_map = [
                proj for proj in self.project_map if proj["projectid"] != project_id
            ]
            # add project if it's not archived
           
            self.update_projects_dropdown()  # Update dropdown with new projects

            # Since `data` directly contains the projectId, no need to use `data.get()`
            # pro_id = data  # Directly use `data` as the projectId

            # # Find the project name associated with the given project ID
            # project_to_remove = next(
            #     (project["projectname"] for project in self.project_map if project["projectid"] == pro_id), 
            #     None
            # )

            # if project_to_remove:
            #     # Remove the project name from self.projects
            #     if project_to_remove in self.projects:
            #         self.projects.remove(project_to_remove)
            #         print(f"Project '{project_to_remove}' removed from projects.")
            #     else:
            #         print(f"Project '{project_to_remove}' not found in projects.")

            #     # Remove the project from self.project_map
            #     self.project_map = [
            #         project for project in self.project_map if project["projectid"] != pro_id
            #     ]
            #     print(f"Project '{project_to_remove}' removed from project_map.")
            # else:
            #     print(f"No project found with projectid: {pro_id}")


    def get_user_startup_path(self):
        try:
            # Get the current username
            current_user = os.getlogin()

            # Build the paths dynamically based on the current user's name
            startup_folder = os.path.join(
                r"C:\Users",
                current_user,
                "AppData",
                "Roaming",
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
                "Startup",
            )
            shortcut_source = os.path.join(
                r"C:\Users",
                current_user,
                "AppData",
                "Roaming",
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
                "SSTRACK.lnk",
            )

            return shortcut_source, startup_folder
        except Exception as e:
            print(f"Failed to getting user path: {e}")
            return None

    def add_shortcut_to_startup(self):
        try:
            # Get the dynamically generated paths
            shortcut_source, startup_folder = self.get_user_startup_path()

            # Check if the shortcut exists
            if os.path.exists(shortcut_source):
                # Define the destination path where the shortcut will be copied
                destination = os.path.join(startup_folder, "SSTRACK.lnk")

                # Copy the shortcut to the startup folder
                try:
                    shutil.copy(shortcut_source, destination)
                    print("SSTRACK has been added to startup.")
                    # Notifier.notify(
                    #     title="SSTRACK",
                    #     message="Settings updated.",
                    #     timeout=3,  # Notification disappears after 3 seconds
                    #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
                    #             )
                    os.system('terminal-notifier -title "SSTRACK started" -message "SStrack" -appIcon "images/animatedlogo.png"')
                except Exception as e:
                    print(f"Failed to add SSTRACK to startup: {e}")
            else:
                print("SSTRACK shortcut not found.")
        except Exception as e:
            print(f"Failed to adding shortcut: {e}")
            return None

    def remove_shortcut_from_startup(self):
        try:
            # Get the dynamically generated paths
            _, startup_folder = self.get_user_startup_path()
            shortcut_path = os.path.join(startup_folder, "SSTRACK.lnk")

            # Check if the shortcut exists and remove it
            if os.path.exists(shortcut_path):
                try:
                    os.remove(shortcut_path)
                    print("SSTRACK has been removed from startup.")
                    # Notifier.notify(
                    #     title="SSTRACK",
                    #     message="Settings updated.",
                    #     timeout=3,  # Notification disappears after 3 seconds
                    #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
                    #             )
                    os.system('terminal-notifier -title "SSTRACK started" -message "SStrack" -appIcon "images/animatedlogo.png"')
                except Exception as e:
                    print(f"Failed to remove SSTRACK from startup: {e}")
            else:
                print("SSTRACK shortcut not found in startup folder.")
        except Exception as e:
            print(f"Failed to removing shortcut: {e}")
            return None
    # Example Usage
    # remove_shortcut_from_startup()  # Uncomment this to remove SSTRACK from startup

    # Bind the checkboxes to functions
    def on_launch_monitor_change(self):
        if self.launch_monitor_var.get():
            self.launch_monitor = True
            self.add_shortcut_to_startup()
        else:
            self.remove_shortcut_from_startup()

    def on_auto_start_change(self):
        try:
            if self.auto_start_var.get():
                self.autoLaunch = True
                with open("autoLaunch.pkl", "wb") as f:
                    pickle.dump(self.autoLaunch, f)

                # Logic for auto-start
                print("Auto-start enabled")
            else:
                # Logic for auto-start off
                print("Auto-start disabled")
                os.remove("autoLaunch.pkl")
            # Notifier.notify(
            #     title="SSTRACK",
            #     message="Settings updated.",
            #     timeout=3,  # Notification disappears after 3 seconds
            #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
            #     )
            os.system('terminal-notifier -title "SSTRACK started" -message "SStrack" -appIcon "images/animatedlogo.png"')
            
        except Exception as e:
            print(f"Failed to change: {e}")
            return None

    def checkAutoLaunch(self):
        try:
            if os.path.isfile("autoLaunch.pkl"):
                with open("autoLaunch.pkl", "rb") as f:
                    self.autoLaunch = pickle.load(f)
                    if self.autoLaunch:
                        self.auto_start_var.set(1 if self.autoLaunch else 0)
                        self.click_play_button()

                        """Checks if the shortcut already exists in the startup folder"""
                        _, startup_folder = self.get_user_startup_path()

                        # Define the path where the shortcut should be located in the startup folder
                        startup_shortcut = os.path.join(startup_folder, "SSTRACK.lnk")

                        # Check if the shortcut exists
                        if os.path.exists(startup_shortcut):
                            self.launch_monitor = True

                    print("autoLaunch", self.autoLaunch)
        except Exception as e:
            print(f"Failed to checking autolaunch: {e}")
            return None

    def minimize_window(self):
        # Minimize the window
        # self.root.iconify()

        # Once the window is small enough, minimize it
        self.root.iconify()
        
    def getBreaktimes(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"https://myuniversallanguages.com:9093/api/v1/superAdmin/getPunctualityDataEachUser/{self.user_id}",
                headers=headers,
            )
            if response.ok:
                json_data = response.json()
                # print("API Response:", json_data)
                self.puncStartTime=json_data.get("data", {}).get('puncStartTime')
                self.puncEndTime = json_data.get("data", {}).get('puncEndTime')

                # self.breakConvertedData = json_data.get("data", {}).get('breakConvertedData') breakTime
                # Initialize total break duration
                self.breakConvertedData = json_data.get("data", {}).get('breakTime') 
                # self.breakConvertedData = json_data.get("data", {}).get('breakConvertedData') 
                total_break_duration = timedelta()

                for break_period in self.breakConvertedData:
                    start = break_period.get("breakStartTime")
                    end = break_period.get("breakEndTime")
                    if start and end:
                        # Convert strings to datetime objects using `dateutil.parser.parse`
                        start_time = parse(start)
                        end_time = parse(end)
                        
                        # Calculate the duration
                        duration = end_time - start_time
                        total_break_duration += duration

                # Convert total duration to hours, minutes, seconds
                total_seconds = int(total_break_duration.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.BreakTimeavailable=f"{hours}h {minutes}m"
            

            print(minutes)
        except Exception as e:
            print(f"Failed to getting break time: {e}")
            return None


    # Parse remainingBreakTime to get the total minutes
    def parse_remaining_break_time(self, remaining_break_time):
        hours, minutes = 0, 0
        if 'h' in remaining_break_time:
            hours = int(remaining_break_time.split('h')[0].strip())
            minutes = int(remaining_break_time.split('h')[1].split('m')[0].strip())
        else:
            minutes = int(remaining_break_time.split('m')[0].strip())
        return hours * 60 + minutes


    def startBreakTime(self):
        
        try:
            while self.breakActive:
                with self.startBreakTime_lock:
                    if self.parse_remaining_break_time(self.BreakTime) > 1:
                        """Change the image of the break button when the break starts."""
                        # self.canvas.itemconfig(self.break_Button, image=self.break_start_icon)
                        self.breakCount +=1

                        print("Break active now")
                        self.breakEndOn = datetime.datetime.now(pytz.UTC)
                        print(self.breakEndOn, "breakstarted on")

                        self.break_button.config(
                                text=f"Time: {self.BreakTime}",  # Text when break ends
                                bg="#68BB45",  # Green background when break ends
                                fg="#FFFFFF",  # White text when break ends
                            )

                        if self.is_timer_running:
                            # self.click_pause_button()
                            threading.Thread(target=self.click_pause_button, daemon=True).start()
                        # Load or initialize breakUsed.pkl
                        if os.path.isfile(GUIApp.get_data_file_path("breakUsed.pkl")):
                            try:
                                with open(GUIApp.get_data_file_path("breakUsed.pkl"), "rb") as f:
                                    self.breakUsed = pickle.load(f)
                            except EOFError:
                                print("Error: breakUsed.pkl is empty. Initializing a new dictionary.")
                                self.breakUsed = {}
                        else:
                            self.breakUsed = {}

                        # Re-enable the break button
                        
                        # Update or add break data
                        self.breakUsed = {
                            "breakId": self.breakId,
                            "breakStartedOn": self.breakStartedOn,
                            "breakEndOn": self.breakEndOn,
                        }

                        # Save the updated breakUsed.pkl
                        with open(GUIApp.get_data_file_path("breakUsed.pkl"), "wb") as f:
                            pickle.dump(self.breakUsed, f)

                        # update break timer 
                        if self.breakCount > 1:
                            self.subtract_break_count(self.BreakTime)

                        if self.breakCount == 5:
                            self.breakCount = 0
                            self.breakId = str(uuid.uuid4())
                            self.breakStartedOn = datetime.datetime.now(pytz.UTC)
                            if os.path.isfile(GUIApp.get_data_file_path("breakData.pkl")):
                                with open(GUIApp.get_data_file_path("breakData.pkl"), "rb") as f:
                                    self.breakData = pickle.load(f)
                            if self.breakUsed:
                                self.breakData.append(self.breakUsed)

                                # Save the updated data to `breakData.pkl`
                                with open(GUIApp.get_data_file_path("breakData.pkl"), "wb") as f:
                                    pickle.dump(self.breakData, f)

                                # Remove `breakUsed.pkl` after processing
                                if os.path.isfile(GUIApp.get_data_file_path("breakUsed.pkl")):
                                    os.remove(GUIApp.get_data_file_path("breakUsed.pkl"))
                                
                                self.breakExecution()

                # Wait until the next minute
                # time.sleep(60 - time.time() % 60)    # Wait until exactly 60 seconds from breakStartedOn
                now = datetime.datetime.now(pytz.UTC)
                elapsed_time = (now - self.breakStartedOn).total_seconds()
                time_to_next_interval = max(0, 60 - (elapsed_time % 60))  # Calculate remaining time until next 60s
                time.sleep(time_to_next_interval)
                
        except Exception as e:
            print(f"Failed to starting break time: {e}")
            return None

    def stop_break(self):
        print("break time stop")

        try:
            while self.breakActive:
                with self.stopBreakTime_lock:
                    # Re-enable the break button
                    self.break_button_enabled = True

                    last_break_triggered_time = None  # Track the last time a break was triggered
                    # Parse the break start time into a datetime object and convert to UTC
                    self.playTime = datetime.datetime.now(pytz.UTC)
                    breakEndTime_dt = parser.isoparse(self.breakEndTime).astimezone(pytz.UTC)
                    
                    user_timezone = datetime.timezone(datetime.timedelta(hours=self.timezone_offset))
                    currenttime_user = self.playTime.astimezone(user_timezone)

                    # Truncate to hour and minute only (removing seconds and microseconds)
                    breakEndTime_dt = breakEndTime_dt.replace(second=0, microsecond=0)
                    currenttime_truncated = currenttime_user.replace(second=0, microsecond=0)

                    # Compare only the truncated hour and minute, and ensure the break is triggered only once per minute
                    if (breakEndTime_dt.hour == currenttime_truncated.hour and
                            breakEndTime_dt.minute == currenttime_truncated.minute and
                            last_break_triggered_time != currenttime_truncated):

                        print("break time off")
                         # Display a notification with an icon
                        # Notifier.notify(
                        #     title="Break ended",
                        #     message="Your break has ended",
                        #     timeout=3,  # Notification disappears after 3 seconds
                        #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
                        # )
                        os.system('terminal-notifier -title "SSTRACK started" -message "Break Ended" -appIcon "images/animatedlogo.png"')

                        # self.canvas.itemconfig(self.break_Button, image=self.break_icon)
                        # Load or initialize breakUsed.pkl
                        self.setUpBreak()

                        self.breakActive=False
                        last_break_triggered_time = currenttime_truncated  # Update the last triggered time
                        # threading.Thread(target=self.breakExecution).start()

            # Sleep for 1 second, ensuring alignment with the start of each second
            time.sleep(1 - time.time() % 1)
        except Exception as e:
            print(f"Failed to stop break time: {e}")
            return None

    def breakExecution(self):
        try:
            print("hello break exe")
            with self.breakExecution_lock:
                # Ensure that breakData.pkl exists and load it correctly
                if os.path.isfile(GUIApp.get_data_file_path("breakData.pkl")):
                    with open(GUIApp.get_data_file_path("breakData.pkl"), "rb") as f:
                        self.breakData_list = pickle.load(f)

                if self.breakData_list:
                    index = 0
                    while index < len(self.breakData_list):
                        breakData = self.breakData_list[index]

                        # Ensure breakData is in the correct format (a dictionary or JSON)
                        if isinstance(breakData, dict):
                            
                            api_url = "https://myuniversallanguages.com:9093/api/v1"

                            headers = {
                                "Authorization": f"Bearer {self.token}",
                            }

                            response = requests.patch(
                                f"{api_url}/timetrack/punctuality/{self.user_id}/break",
                                headers=headers,
                                data=breakData  # Use json instead of data if it's a dictionary
                            )

                            if response.ok:
                                print("Timer stopped:")
                                # Remove the processed data from the list and update the file
                                del self.breakData_list[0]
                                with open(GUIApp.get_data_file_path("breakData.pkl"), "wb") as f:
                                    pickle.dump(self.breakData_list, f)
                                index = 0  # Reset the index if we modified the list
                                self.getRemainingBreakTime()
                            else:
                                print("Failed to execute break data")
                                break
                        else:
                            print(f"Invalid breakData format: {breakData}")
                            break
                else:
                    return None
        except Exception as error:
            print(f"An error while break execution: {error}")
            return None

    def getRemainingBreakTime(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"https://myuniversallanguages.com:9093/api/v1/timetrack/remainingBreak/{self.user_id}",
                headers=headers,
            )
            if response.ok:
                self.breakFound = True
                json_data = response.json()
                print(json_data)
                self.BreakTime = json_data.get("data", {}).get('remainingBreakTime')
                # Validate and update UI only if BreakTime is valid
                # Dynamically update UI based on BreakTime
                self.update_break_label()
                # self.break_label.config(text=self.BreakTime)

        except Exception as error:
            print(f"An error occurred while getting remaining break time: {error}")
            return None

    def update_break_label(self):
        try:
            """
            Updates the break labels if the break time is valid.
            """
            if self.is_break_time_valid(self.BreakTime):
                # Remove the fetching placeholder
                # self.fetching_label.destroy()

                # Add "Remaining Break" label
                tk.Label(
                    self.frame0, text="", fg="#7ACB59", bg="#0E4772", font=("Roboto", 13)
                ).place(x=420, y=18)

                # Add break time label
              
            if not self.break_button_enabled:
                self.break_button.config(
                    text=f"Time: {self.BreakTime}",  # Text when break ends
                    bg="#68BB45",  # Green background when break ends
                    fg="#FFFFFF",  # White text when break ends
                )
           
                # self.break_button.config(
                #     text=self.BreakTime,  # Text when break ends
                #     bg="#68BB45",  # Green background when break ends
                #     fg="#FFFFFF",  # White text when break ends
                # )
        except Exception as e:
            print(f"Failed to updating break label: {e}")
            return None

def main():
    app = NSApplication.sharedApplication()
    delegate = GUIApp.alloc().init()
    app.setDelegate_(delegate)
    NSRunningApplication.currentApplication().activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    app.run()


if __name__ == "__main__":
    main()