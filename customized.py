from tkinter import *
from tkinter import Toplevel
from tkinter import messagebox
import datetime
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

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
# from pync import Notifier
from tkinter import font
# Import platform-specific libraries
if platform.system() == "Windows":
    import pygetwindow as gw
elif platform.system() == "Linux":
    import ewmh


class GUIApp:
    def __init__(self, root):
        # Initialize application variables and UI components
        # Initialize application variables and UI components
        self.sio = socketio.Client()
        self.token = None  # Initialize token as None
        self.sio = socketio.Client()
        print("hello customize")
        self.overall_timer = None
        self.is_timer_running = False
        self.screenshot_count = 0
        self.root = root
        self.root.title("HOME")
        self.root.geometry("700x340")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        # Set application icon
        # Resize the image and get both the PhotoImage and PIL Image objects
        # self.official_icon, self.icon_for_tray = self.resize_image('images/logo.png', 100, 100, 10)
        # self.icon_for_tray = self.resize_image2("images/logoTray.png", 50, 50, 5)
        self.icon_for_tray = self.resize_image2(self.resource_path("images/logoTray.png"), 50, 50, 5)
        self.icon = self.icon_for_tray

        # self.official_icon, _ = self.resize_image("images/logo.png", 100, 100, 10)
        self.official_icon, _ = self.resize_image(self.resource_path("images/logo.png"), 100, 100, 10)
        self.root.iconphoto(True, self.official_icon)
        self.forgotTimer = False
        self.projectId = None  # Variable to store selected project ID
        self.projectIdNew = None
        self.projectName = None
        self.selected_project_name = None
        # Load user token from a stored file
        self.user_Data()
        # with open("data.pkl", "rb") as f:
        #     stored_data = pickle.load(f)
        #     self.token = stored_data
        self.last_time = time.time()

        self.activity_flag = False
        
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
        self.current_v = "1.1.19"
        self.dailytime = "0h 0m"
        self.hours = "00"
        self.minutes = "00"
        self.BreakTime='0h 0m'
        # self.check_for_update()
        self.check_for_update_lock = threading.Lock()  # Initialize the lock

        self.percentage = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        # Initialize the overall report timer (but don't start it yet)
        self.overall_report = ""  # Initialize an empty string to store the report
        self.weeklyTimeLimit = "No limit"
        self.allowAddingOfflineTime = 0

        self.trackingStart_list = []
        self.trackingStop_list=[]
        self.breakData = []
        self.calledImmediate = False
        self.autoLaunch = False
        self.launch_monitor = False
        self.breakActive = False
        self.breakCount = 0
        self.breakUsed = {}
        self.breakConvertedData = []
        self.popActive=False
        self.breakFound = False
        self.last_notification_time = 0  # Timestamp of the last notification
        self.notification_timeout = 3  # Notification display timeout in seconds
        # threading.Thread(target=self.get_data).start()
        
        # Create and configure UI elements
        frame0 = Frame(self.root, width=700, height=80, bg="#0E4772")
        frame0.place(x=0, y=0)

        # self.logo_icon = ImageTk.PhotoImage(file='images/sstracklogo.png')
        self.logo_icon = ImageTk.PhotoImage(file=self.resource_path("images/sstracklogo.png"))
        logo_label = Label(frame0, image=self.logo_icon, bg="#0E4772")
        logo_label.place(x=20, y=10)

        # Load setting icon with margin using the new method
        # self.setting_icon = self.load_icon_with_margin('images/Settings_Icon.png', 20, 20, margin=10)
        self.setting_icon = self.load_icon_with_margin(self.resource_path("images/Settings_Icon.png"), 20, 20, margin=10)
        self.setting_label = tk.Label(
            frame0, image=self.setting_icon, bg="#0E4772", cursor='hand2')
        self.setting_label.place(x=600, y=18)
        self.setting_label.bind("<Button-1>", lambda e: self.open_settings())

        # Load logout icon with margin using the new method
        # self.logout_icon = self.load_icon_with_margin('images/log_out_white.png', 20, 20, margin=10)
        self.logout_icon = self.load_icon_with_margin(self.resource_path('images/log_out_white.png'), 20, 20, margin=10)
        self.logout_button = tk.Label(
            frame0, image=self.logout_icon, bg="#0E4772", cursor='hand2')
        self.logout_button.place(x=633, y=18)
        self.logout_button.bind("<Button-1>", lambda e: self.logout())

        # self.logout_icon, _ = self.resize_image(
        #     'images/logout.png', 30, 30, 10)
        # self.logout_button = tk.Button(
        #     frame0, image=self.logout_icon, bg="#0E4772", border=0, command=self.logout, cursor='hand2')
        # self.logout_button.place(x=600, y=15)

        # logout = Label(frame0, text="Logout", fg="#ffffff",
        #                bg="#0E4772", font=('Roboto', 14,), cursor='hand2')
        # logout.place(x=540, y=25)
        # logout.bind("<Button-1>", self.logout)

        frame2 = Frame(self.root, width=700, height=150, border=1, bg="#FFFFFF")
        frame2.place(x=50, y=100)

        self.username = Label(
            frame2,
            text=self.name,
            fg="#0E4772",
            bg="#FFFFFF",
            font=("Roboto", 24, "bold"),
        )
        self.username.place(x=203, y=8)

        # self.verified_icon, _ = self.resize_image("images/verified.png", 35, 35, 10)
        self.verified_icon, _ = self.resize_image(self.resource_path("images/verified.png"), 35, 35, 10)
        self.verified_label = tk.Label(
            frame2, image=self.verified_icon, bg="#ffffff", border=0)
        self.verified_label.place(x=150, y=0)

        # Example usage
        font_file = os.path.join(os.path.dirname(__file__), "font", "Technology.ttf") # Path to your .ttf file


        companies = [self.company]
        selected_company = tk.StringVar()
        newselected_company = tk.StringVar()
        selected_company.set(companies[0])  # Set the initial company to display\
        newselected_company = selected_company.get()
        if len(newselected_company) > 11:
            newselected_company = (
                newselected_company[:8] + "..."
            )  # Truncate and add ellipsis

        max_option_width = 12

        # Create a label to display the selected company
        company_label = tk.Label(
            frame2,
            text=newselected_company,
            fg="#FFFFFF",
            bg="#0E4772",
            font=("Roboto", 14),
            width=max_option_width,
            height=1,  # Keep height at 1 line
            pady=1.5,   # Add vertical padding
        )
        company_label.place(x=500, y=8)

        self.frame = Frame(root, width=700, height=150, border=1, bg="#FFFFFF")
        self.frame.place(x=60, y=160)

        self.description = None
        self.descriptions = Entry(
            self.frame,
            width=350,
            borderwidth=1,        # Add minimal border
            highlightthickness=1,  # Slight border around the entry
            highlightbackground="#FFFFFF",  # White border color
            highlightcolor="#FFFFFF",       # White color when focused
            fg="#0E4772",
            bg="#FFFFFF",
            font=("Roboto", 14),
            relief="flat"
        )
        self.descriptions.place(x=150, y=10)
        self.placeholder = 'What project are you engaged in?'
         
        # Canvas widget with increased width
        canvas_width = 200  # Increased width
        canvas_height = 150
        canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#FFFFFF", highlightthickness=0)
        canvas.place(x=0, y=80)

        # Draw the box with a top-right rounded corner
        radius = 50  # Radius for the rounded corner
        x0, y0, x1, y1 = 0, 0, canvas_width, canvas_height  # New dimensions for increased width

        # Draw the straight sides of the box (excluding the top-right corner)
        canvas.create_polygon(
            x0, y0,
            x1 - radius, y0,  # Top edge until the curve starts
            x1, y0 + radius,  # Curve start to bottom-right
            x1, y1,
            x0, y1,
            x0, y0,
            fill="#7ACB59", outline="#7ACB59"
        )

        # Draw the rounded corner arc (top-right corner)
        canvas.create_arc(
            x1 - 2 * radius, y0, x1, y0 + 2 * radius,  # Bounding box for the arc
            start=0, extent=90,  # Arc angle (0 to 90 degrees for top-right)
            style="pieslice", outline="#7ACB59", fill="#7ACB59"
        )

        # Add "Today" text inside the box
        canvas.create_text(
            20, 20,  # x and y position for the text
            text="Today",
            fill="#FFFFFF",  # White color for the text
            font=("Inter", 18),
            anchor="nw"  # Align the text to the top-left
        )
        
        # Load the custom font with size 52
        # custom_font = self.load_custom_font(size=52)
            # Clock display under "Today" text
        # hours = str(self.hours).replace('h', '').zfill(2)  # Remove 'h' and pad with zeros
        hours = self.hours,
        # minutes = str(self.minutes).replace('m', '').zfill(2)   # Ensures two digits
        minutes = self.minutes,
        
        # Hour label
        # self.hour_label = Label(root, text=hours, fg="#FFFFFF", bg="#7ACB59",
        #                    font=("courier", 52))
        # self.hour_label.place(x=10, y=130)  # Position under the "Today" text

        # # Colon label
        # self.colon_label = Label(root, text=":", fg="#FFFFFF", bg="#7ACB59",
        #                     font=("courier", 52))
        # self.colon_label.place(x=77, y=130)  # Adjust x-coordinate for alignment

        # # Minute label
        # self.minute_label = Label(root, text=minutes, fg="#FFFFFF", bg="#7ACB59",
        #                      font=("courier", 52))
        # self.minute_label.place(x=95, y=130)
        custom_font = font.Font(family="courier", size=42, weight="normal" )

# Hour label
        self.hour_label = Label(root, text=hours, fg="#FFFFFF", bg="#7ACB59",
                           font=custom_font)
        self.hour_label.place(x=5, y=130)  # Position under the "Today" text

        # Colon label
        self.colon_label = Label(root, text=":", fg="#FFFFFF", bg="#7ACB59",
                            font=custom_font)
        self.colon_label.place(x=70, y=130)  # Adjust x-coordinate for alignment

        # Minute label
        self.minute_label = Label(root, text=minutes, fg="#FFFFFF", bg="#7ACB59",
                             font=custom_font)
        self.minute_label.place(x=105, y=130)


        
        # Bind the Enter key to the get_description_value function
        self.descriptions.bind("<Return>", self.get_description_value)
        self.descriptions.bind("<FocusIn>", self.on_focus_in)
        self.descriptions.bind("<FocusOut>", self.on_focus_out)
        # Limit characters based on the maximum width (350 pixels)
        self.max_characters = self.calculate_max_characters() + 5
        self.descriptions.bind("<KeyRelease>", self.limit_text_length)

        # Set the initial value based on existing description
        if self.description:
            self.descriptions.insert(0, self.description)
        else:
            self.set_placeholder()

        Frame(self.frame, width=320, height=2, bg="#0E4772").place(x=150, y=35)
        self.projects = ["no project"]
        self.project_map = []
        self.selected_project = tk.StringVar()
        self.selected_project.set(self.projects[0])
        self.selected_project.trace("w", self.callback)  # Monitor changes in selection

        # Load dropdown icon
        # self.vector = PhotoImage(file="images/down.png")
        self.vector = PhotoImage(file=self.resource_path("images/down.png"))

        # Create dropdown button
        # self.button = tk.Button(
        #     self.frame, text=self.selected_project.get(), image=self.vector,
        #     compound="right", anchor="w", font=("Roboto", 15),
        #     fg="#FFFFFF", bg="#7ACB59", activebackground="#7ACB59", width=130, height=20,
        #     relief="flat", cursor="hand2", command=self.show_menu
        # )
        # self.button.place(x=390, y=6)

        # Create a Frame to hold the button and the icon
        # Create a Frame to hold the button and the icon
        # Create a Frame to hold the button and the icon with fixed height
        # Create a Frame to hold the button and the icon with fixed height and width
        self.button_frame = tk.Frame(
            self.frame, bg="#0E4772", height=25, width=115
        )  # Set fixed height and width
        self.button_frame.place(x=490, y=6)  # Place at specific coordinates

  # Button with text only, no click effects, and fixed width
        self.button = tk.Label(
            self.button_frame, text=self.selected_project.get(), font=("Roboto", 14),
            fg="#FFFFFF", bg="#0E4772", cursor="hand2", width=10
        )
        self.button.bind("<Button-1>", lambda e: self.show_menu())

        self.button.pack(side="left")

        # Label for the icon on the far right
        self.icon_label = tk.Label(
            self.button_frame, image=self.vector, bg="#0E4772"
        )
        self.icon_label.pack(side="left")
        self.button_frame.bind("<Button-1>", lambda e: self.show_menu())

        # Bind the label click to the show_menu command
        self.icon_label.bind("<Button-1>", lambda e: self.show_menu())
        # To ensure the frame's width is enforced, prevent it from resizing with `propagate`
        self.button_frame.pack_propagate(False)

        # Create a menu for the dropdown
        self.projects_dropdown = tk.Menu(self.frame, tearoff=0, bg="#FFFFFF", fg="#000000", font=("Roboto", 10))


        # self.button_frame.bind("<Button-1>", lambda e: self.show_menu())

        # # Bind the label click to the show_menu command
        # self.icon_label.bind("<Button-1>", lambda e: self.show_menu())
        # # To ensure the frame's width is enforced, prevent it from resizing with `propagate`
        # self.button_frame.pack_propagate(False)

        # Create a menu for the dropdown
        # self.projects_dropdown = tk.Menu(
        #     self.frame, tearoff=0, bg="#FFFFFF", fg="#000000", font=("Roboto", 10)
        # )

        # Bind dropdown update
        self.update_projects_dropdown()  # Initial population of dropdown menu

        frame1 = Frame(self.root, width=700, height=110, bg="#0E4772")
        frame1.place(x=0, y=230)

        # Resize the images
        # self.play_icon, _ = self.resize_image("images/playButton.png", 70, 70, 10)
        self.play_icon, _ = self.resize_image(self.resource_path("images/playButton.png"), 70, 70, 10)
        self.pause_icon_grey, _ = self.resize_image(
            # "images/Pause_Icon_Grey.png", 60, 60, 10
            self.resource_path("images/Pause_Icon_Grey.png"), 60, 60, 10
        )
              # self.break_icon, _ = self.resize_image(
        #     "images/BreakButton.png", 60, 60, 10
        # )
        self.play_icon_grey, _ = self.resize_image(
            self.resource_path("images/Play_Icon_Grey.png"), 70, 70, 10
            # "images/Play_Icon_Grey.png", 70, 70, 10
        )
        # self.pause_icon, _ = self.resize_image("images/Pause_Red.png", 60, 60, 10)
        self.pause_icon, _ = self.resize_image(self.resource_path("images/Pause_Red.png"), 60, 60, 10)
        # Create the play button
        # Create a Canvas widget to hold the images (transparent effect)
        self.canvas = tk.Canvas(
            frame1, width=700, height=110, bg="#0E4772", highlightthickness=0
        )
        self.canvas.place(x=0, y=0)

        # Adjust the y-position for images to align them properly like before
        y_position = 5  # Same as you had with Button.place(y=5)

        # Add the play button to the canvas (place at x=40, y=5 like the original Button)
        self.play_button = self.canvas.create_image(
            40, y_position, image=self.play_icon, anchor=tk.NW
        )
        self.canvas.tag_bind(self.play_button, "<Button-1>", self.click_play_button)

        # Add the pause button to the canvas (place at x=100, y=10 to avoid overlap)
        self.pause_button = self.canvas.create_image(
            100, y_position + 8, image=self.pause_icon_grey, anchor=tk.NW
        )
        self.canvas.tag_bind(
            self.pause_button, "<Button-1>", self.click_pause_button
        )  # Bind the click event for the pause button

        # Lower the play button to make sure pause is on top
        self.canvas.lift(self.play_button)

        # Bind mouse enter and leave events for the play button
        self.canvas.tag_bind(
            self.play_button, "<Enter>", lambda e: self.canvas.config(cursor="hand2")
        )
        self.canvas.tag_bind(
            self.play_button, "<Leave>", lambda e: self.canvas.config(cursor="")
        )

        # Bind mouse enter and leave events for the pause button
        self.canvas.tag_bind(
            self.pause_button, "<Enter>", lambda e: self.canvas.config(cursor="hand2")
        )
        self.canvas.tag_bind(
            self.pause_button, "<Leave>", lambda e: self.canvas.config(cursor="")
        )

        # Initially hide the pause button (like before)
        # self.canvas.itemconfig(self.pause_button, state='hidden')
        # abdullah ka button
              # Create a button
    
        # Create the label (instead of a button)
        self.break_button = tk.Label(
            frame1,
            text="Break",
            bg="#E8F4FC",       # Background color
            fg="#7094B0",       # Text color
            font=("Arial", 14, "bold"),
            width=20,               # Width in text units
            height=2,            # Height in text units
            anchor="center"     # Center align the text
        )

        # Place the label on the canvas
        self.break_button.place(x=200, y=30)

        # Bind a click event to mimic button behavior
        self.break_button.bind("<Button-1>", self.click_break_button)

# Create a rounded button
        # Styled label for the link
        self.link_label = tk.Label(
            frame1,
            text="VIEW BREAK TIMELINE",
            bg="#0E4772",  # Background color
            fg="#FFFFFF",  # Text color
            font=("Arial", 8, ),
            width=20,
            height=1,
            cursor="hand2"
        )
        self.link_label.place(x=232, y=72)
        # Bind the label to open the link
        self.link_label.bind("<Button-1>", self.open_link)
      
# Create a rounded button on a canvas
 
# Create a rounded button
 

        # self.play_button.config(state=tk.NORMAL)
        # self.pause_button.config(state=tk.DISABLED)
        # self.break_icon = PhotoImage(file="images/BreakButton.png")
        # self.break_start_icon = PhotoImage(file="images/activeBreak.png")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        # # Add the pause button to the canvas (place at x=100, y=10 to avoid overlap)
        # self.break_Button = self.canvas.create_image(
        #     475, 14, image=self.break_icon, anchor=tk.NW
        # )
        # self.canvas.tag_bind(
        #     self.break_Button, "<Button-1>", self.click_break_button
        # )  # Bind the click event for the pause button

   
        # Bind mouse enter and leave events for the pause button
        # self.canvas.tag_bind(
        #     self.break_Button, "<Enter>", lambda e: self.canvas.config(cursor="hand2")
        # )
        # self.canvas.tag_bind(
        #     self.break_Button, "<Leave>", lambda e: self.canvas.config(cursor="")
        # )



        # Adjust positions based on the length of hours
        if len(self.hours) == 2:  # Single-digit hour
            colon_x = 320 + 57  # Adjust for single-digit hour (add 30 pixels to x)
            minute_x = colon_x + 15  # Adjust minute label (15 pixels after colon)
        else:  # Double-digit hour
            colon_x = 320 + 60  # Adjust for double-digit hour (add 50 pixels to x)
            minute_x = colon_x + 15  # Adjust minute label (15 pixels after colon)

        # Place the colon and minute labels based on the calculated positions
        # self.colon_label.place(x=colon_x, y=47)
        # self.minute_label.place(x=minute_x, y=47)

        # self.TIMELINE, _ = self.resize_image("images/timeline.png", 160, 40, 0)
        self.TIMELINE, _ = self.resize_image(self.resource_path("images/timeline.png"), 160, 40, 0)
        TIMELINE_label = tk.Button(
            frame1,
            image=self.TIMELINE,
            bg="#0E4772",
            border=0,
            command=self.view_Timeline,
            cursor="hand2",
        )
        TIMELINE_label.place(x=480, y=30)
        self.python_exe = sys.executable
        self.fetch_data_lock = threading.Lock()
        # self.add_shortcut_to_startup()  # Add SSTRACK to startup

        # Start the first update check immediately upon initialization
        self.schedule_update_check()
        self.screenshot_data_list = []
        self.sleep_mode = False
        self.exact_time = datetime.datetime.now(pytz.UTC)
        self.puncEndTime = datetime.datetime.now(pytz.UTC)
        self.startTime = datetime.date.today()
        self.tl = False
        # Create threads and set them as daemons
        self.play_timer_lock = threading.Lock()
        self.screenshots_add_lock = threading.Lock()
        self.stop_timer_lock = threading.Lock()
        self.screenshots_data_lock = threading.Lock()
        self.handle_sleep_mode_lock = threading.Lock()
        self.check_activity_lock = threading.Lock()
        self.update_time_lock = threading.Lock()
        self.breakExecution_lock = threading.Lock()
        self.startBreakTime_lock = threading.Lock()
        self.stopBreakTime_lock = threading.Lock()

        self.updateProject_lock = threading.Lock()
        self.update_daily_time_lock = threading.Lock()
        self.click_pause_button_lock = threading.Lock()
        self.employeeSetting_lock = threading.Lock()
        self.archive_project_lock = threading.Lock()
        self.on_project_select_lock = threading.Lock()
        self.update_User_status_lock = threading.Lock()
        # self.notify_user()
        # speaker = win32com.client.Dispatch("SAPI.SpVoice")
        # speaker.Speak("hi Welcome to S STRACK") # <--------- I added this line

        # Create mouse and keyboard listeners
        # self.mouse_listener = mouse.Listener(
        #     on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
        # )
        # self.keyboard_listener = keyboard.Listener(
        #     on_press=self.on_press, on_release=self.on_release
        # )
        # self.total = 0
        # # Start the listeners
        # self.mouse_listener.start()
        # self.keyboard_listener.start()
        # Use a timer to call the functions after the window is shown
        # Start the listeners in a separate thread
        threading.Thread(target=self.start_listeners, daemon=True).start()
        # self.userProject()
        # self.fetch_projects()
        self.activity_monitor = ActivityMonitor()
        # Add the checkboxes for startup and auto-start functionality
        self.launch_monitor_var = tk.BooleanVar()
        self.auto_start_var = tk.BooleanVar()
        self.break_button_enabled = True 


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
        """Return the full path of a file inside the app directory."""
        return os.path.join(GUIApp.get_app_dir(), filename) 
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


    # def speak_text(self, text):
    #     try:
    #         speaker = win32com.client.Dispatch("SAPI.SpVoice")
    #         speaker.Speak(text)
    #     except Exception as e:
    #         print(f"Voice functionality is unavailable: {e}")
    #         # Optional: Log the error to a file for debugging
    #         with open("error_log.txt", "a") as log_file:
    #             log_file.write(f"Voice error: {str(e)}\n")

    # Load the font dynamically
    # Function to load the custom font dynamically
    # def load_custom_font(self, size=52):
    #     # Path to the custom font
    #     font_path = os.path.join(os.path.dirname(__file__), "font", "Technology.ttf")
        
    #     # Load the font using PIL and register it with tkinter
    #     pil_font = ImageFont.truetype(font_path, size)
    #     family = pil_font.getname()[0]

    #     # Return a tkinter font object
    #     return font.Font(family=family, size=size)

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
                    self.descriptions.delete(0, tk.END)  # Clear the entry widget
                    self.descriptions.insert(0, self.description)
                projectName = project.get('name')
                if projectName is not None:
                    self.projectId = project.get("_id")
                    self.selected_project.set(projectName)
                    self.selected_project_name = projectName
                else:
                    self.selected_project.set("no project")
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
            # Clear existing menu options
            self.projects_dropdown.delete(0, "end")
            # Ensure the current selected project is valid
            if self.selected_project.get() not in self.projects:
                self.selected_project.set("no project")
            # Calculate a fixed width based on the button width
            fixed_width = 15  # Set a fixed width in terms of characters

            for project in self.projects:
                # Add project with fixed length (by padding spaces)
                padded_label = project.ljust(fixed_width)  # Pad to fixed width
                self.projects_dropdown.add_command(
                    label=padded_label,
                    command=lambda p=project: self.selected_project.set(p),
                )

            self.fixProject()

            # Update button text to selected project with ellipsis if necessary

        except Exception as e:
            print(f"An error occurred: {e}")

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
            print(f"An error occurred: {e}")
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
                        print(f"An error occurred: {e}")
                        return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def set_placeholder(self):
        print("Setting placeholder")  # Debugging statement
        self.descriptions.delete(0, tk.END)  # Clear the entry widget
        self.descriptions.insert(0, self.placeholder)
        self.descriptions.config(fg="grey")

    def get_description_value(self, event=None):
        try:
            print("hello description value")
            value = self.descriptions.get()
            if value == self.placeholder:
                value = ""
            # Only update if the new value is different from the current description
            if value != self.description:
                self.description = value

                if self.description and self.is_timer_running:
                    # self.is_timer_running = False
                    self.restartTimer()
                # Move focus to root window to avoid blinking cursor
                if self.description:
                    self.descriptions.delete(0, tk.END)  # Clear the entry widget
                    self.descriptions.insert(0, self.description)
                # threading.Thread(target=self.updateProject).start()
                self.updateProject()

                print(value)  # or process the value as needed
                
            self.frame.focus_set()
        except Exception as e:
            print(f"An error occurred: {e}")
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
            # Load user token from a stored file
            data_path = os.path.join(self.get_app_dir(), "data.pkl") 
            if os.path.isfile(data_path):
                with open(data_path, "rb") as f:
                    stored_data = pickle.load(f)
                    self.token = stored_data
            # Decode the Base64-encoded parts of the token
            header, payload, signature = self.token.split(".")
            # decoded_header = base64.urlsafe_b64decode(
            #     header + '==').decode('utf-8')
            decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
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
            self.user_id = self.user_info["_id"]
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

    def open_settings(self):
        # Resize the icon to a smaller size
        self.settings_icon, _ = self.resize_image(self.resource_path("images/logoTray.png"), 20, 20, 10)

        # Create a new Toplevel window for the popup
        settings_popup = tk.Toplevel(self.root)
        settings_popup.title("Settings")
        settings_popup.geometry("700x340")
        settings_popup.configure(bg="#F0F0F0")
        settings_popup.overrideredirect(True)

        # Get the current window's position
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        settings_popup.geometry(f"+{x}+{y}")

        # Make the popup window movable
        def start_move(event):
            settings_popup.x = event.x
            settings_popup.y = event.y

        def stop_move(event):
            settings_popup.x = None
            settings_popup.y = None

        def on_motion(event):
            dx = event.x - settings_popup.x
            dy = event.y - settings_popup.y
            settings_popup.geometry(
                f"+{settings_popup.winfo_x() + dx}+{settings_popup.winfo_y() + dy}"
            )

        settings_popup.bind("<Button-1>", start_move)
        settings_popup.bind("<ButtonRelease-1>", stop_move)
        settings_popup.bind("<B1-Motion>", on_motion)

        # Header section with title, icon, and close (X) button
        header_frame = tk.Frame(settings_popup, bg="#FFFFFF")
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        # Set row height for the header frame (use a smaller value)
        settings_popup.grid_rowconfigure(0, minsize=30)  # Adjust the height as needed

        # Load the resized icon
        icon_label = tk.Label(header_frame, image=self.settings_icon, bg="#FFFFFF")
        icon_label.grid(row=0, column=0, padx=(5, 0), sticky="w")  # Reduced padding

        # Title label with smaller font
        title_label = tk.Label(
            header_frame, text="Settings", font=("Arial", 10), bg="white"
        )
        title_label.grid(row=0, column=1, padx=(2, 5), sticky="w")  # Reduced padding

        # Close button with smaller font
        close_button = tk.Button(
            header_frame,
            text="x",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black",
            relief="flat",
            command=settings_popup.destroy,
        )
        close_button.grid(row=0, column=2, padx=5, sticky="e")  # Reduced padding

        # Adjust the column weights for proper alignment
        header_frame.grid_columnconfigure(0, weight=0)  # Icon column doesn't expand
        header_frame.grid_columnconfigure(1, weight=1)  # Title column expands
        header_frame.grid_columnconfigure(2, weight=0)  # Button column doesn't expand

        # Hover effect for the close button
        def on_enter(event):
            close_button["background"] = "#F44336"  # Red on hover
            close_button["foreground"] = "white"

        def on_leave(event):
            close_button["background"] = "white"  # White when not hovered
            close_button["foreground"] = "black"

        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

        # Hover effect for the close button
        def on_enter(event):
            close_button["background"] = "#F44336"  # Red on hover
            close_button["foreground"] = "white"

        def on_leave(event):
            close_button["background"] = "white"  # White when not hovered
            close_button["foreground"] = "black"

        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

        # Hover effect for the close button
        def on_enter(event):
            close_button["background"] = "#F44336"  # Red on hover
            close_button["foreground"] = "white"

        def on_leave(event):
            close_button["background"] = "white"  # White when not hovered
            close_button["foreground"] = "black"

        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

        # Add padding and layout styling
        title_font = ("Arial", 10, "bold")
        label_font = ("Arial", 9)

        # Configure the grid layout to make it responsive
        settings_popup.columnconfigure(0, weight=1)
        settings_popup.columnconfigure(1, weight=1)
        settings_popup.columnconfigure(2, weight=1)
        settings_popup.columnconfigure(3, weight=1)

        # Team Settings Section
        # Team Settings Section
        # Replace the 'pack' call with 'grid'
        # Team Settings Section
        # User Settings Section
        tk.Label(
            settings_popup, text="User Settings", font=title_font, bg="#F0F0F0"
        ).grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # Checkboxes for launch and auto-start functionality
        tk.Checkbutton(
            settings_popup,
            text="Launch SSTRACK when I start Windows",
            variable=self.launch_monitor_var,
            bg="#F0F0F0",
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        tk.Checkbutton(
            settings_popup,
            text="Automatically start tracking when I launch SSTRACK",
            variable=self.auto_start_var,
            bg="#F0F0F0",
        ).grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Add traces to detect checkbox changes
        self.launch_monitor_var.trace(
            "w", lambda *args: self.on_launch_monitor_change()
        )
        self.auto_start_var.trace("w", lambda *args: self.on_auto_start_change())

        # Team Settings Section
        tk.Label(
            settings_popup,
            text="Team settings (set by company manager)",
            font=title_font,
            bg="#F0F0F0",
        ).grid(row=4, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # Screenshots
        tk.Label(
            settings_popup,
            text="Screenshots:",
            font=label_font,
            bg="#F0F0F0",
            anchor="e",
        ).grid(row=5, column=0, padx=5, pady=2, sticky="w")
        tk.Label(
            settings_popup,
            text=self.ssperhr,
            font=label_font,
            fg="#4CAF50",
            bg="#F0F0F0",
            anchor="w",
        ).grid(row=5, column=1, padx=5, pady=2, sticky="w")

        # Auto-pause tracking
        tk.Label(
            settings_popup, text="Auto-pause tracking:", font=label_font, bg="#F0F0F0"
        ).grid(row=6, column=0, padx=5, pady=2, sticky="w")
        tk.Label(
            settings_popup,
            text=str(self.autoPauseTrackingAfter) + " min",
            font=label_font,
            fg="#4CAF50",
            bg="#F0F0F0",
        ).grid(row=6, column=1, padx=5, pady=2, sticky="w")

        # Weekly time limit
        tk.Label(
            settings_popup, text="Weekly time limit:", font=label_font, bg="#F0F0F0"
        ).grid(row=7, column=0, padx=5, pady=2, sticky="w")
        tk.Label(
            settings_popup,
            text=self.weeklyTimeLimit,
            font=label_font,
            fg="#4CAF50",
            bg="#F0F0F0",
        ).grid(row=7, column=1, padx=5, pady=2, sticky="w")

        # Allow adding offline time
        tk.Label(
            settings_popup,
            text="Allow adding offline time:",
            font=label_font,
            bg="#F0F0F0",
        ).grid(row=5, column=2, padx=5, pady=2, sticky="w")
        tk.Label(
            settings_popup,
            text="Yes" if self.allowAddingOfflineTime else "No",
            font=label_font,
            fg="#4CAF50",
            bg="#F0F0F0",
        ).grid(row=5, column=3, padx=5, pady=2, sticky="w")

        # Activity Level tracking
        tk.Label(
            settings_popup,
            text="Activity Level tracking:",
            font=label_font,
            bg="#F0F0F0",
        ).grid(row=6, column=2, padx=5, pady=2, sticky="w")
        tk.Label(
            settings_popup, text="Yes", font=label_font, fg="#4CAF50", bg="#F0F0F0"
        ).grid(row=6, column=3, padx=5, pady=2, sticky="w")

        # App & URL tracking
        tk.Label(
            settings_popup, text="App & URL tracking:", font=label_font, bg="#F0F0F0"
        ).grid(row=7, column=2, padx=5, pady=2, sticky="w")
        tk.Label(
            settings_popup, text="Yes", font=label_font, fg="#4CAF50", bg="#F0F0F0"
        ).grid(row=7, column=3, padx=5, pady=2, sticky="w")

        # Add traces to detect checkbox changes
        # self.launch_monitor_var.trace("w", lambda *args: self.on_launch_monitor_change())
        # self.auto_start_var.trace("w", lambda *args: self.on_auto_start_change())

        # Add buttons at the bottom, with responsiveness
        # save_button = tk.Button(settings_popup, text="Save", width=12, height=1, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief="flat", command=self.save_settings)
        # cancel_button = tk.Button(settings_popup, text="Cancel", width=12, height=1, bg="#F44336", fg="white", font=("Arial", 10, "bold"), relief="flat", command=settings_popup.destroy)

        # save_button.grid(row=7, column=2, pady=20, padx=20, sticky="e")
        # cancel_button.grid(row=7, column=3, pady=20, padx=20, sticky="w")

        # Make sure focus stays on the popup window
        settings_popup.grab_set()

    def open_settingsMy(self):
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

    # def on_quit(self, icon, item):
    #     try:
    #         # Check if the timer is running
    #         if self.is_timer_running:
    #             confirm = messagebox.askyesno("App Closing", "Are you sure you want to stop the SSTRACK?")
    #             if confirm:
    #                 self.click_pause_button()  # Pause tracking before exiting
    #                 self.stop_process()  # Separate method to handle process termination
    #         else:
    #             self.stop_process()  # Directly stop the process if timer is not running

    #         # Safely remove the tray icon
    #         if self.icon:
    #             print("Removing tray icon...")
    #             self.icon.stop()
    #             print("Tray icon removed successfully.")

    #         # Close the Tkinter window
    #         self.root.destroy()

    #     except Exception as e:
    #         print(f"An error occurred during quitting: {e}")

    def stop_process(self):
        """Terminate the SSTRACK process."""
        try:
            os.system("taskkill /f /im SSTRACK.exe")  # Terminate the process directly
            print("SSTRACK process terminated.")
            self.root.destroy()  # Close the application window
        except Exception as e:
            print(f"Error while terminating SSTRACK process: {e}")

    def setup(self, icon):
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

    # def refresh_tray_icon(self):
    #     if self.icon:
    #         # Stop the current icon
    #         self.icon.stop()
    #         time.sleep(0.1)  # Small delay to ensure proper cleanup
    #         # Restart the tray icon
    #         self.run_tray()


    # def run_tray(self):
       
    #     # Set up the tray icon with a click event to show the window
    #     self.icon = Icon(
    #         "my_app",
    #         self.icon_for_tray,
    #         "SSTRACK",
    #         menu=Menu(
    #             MenuItem("Show", self.show_window),  # Show window menu item
    #             MenuItem("Quit", self.on_quit),  # Quit menu item
    #         ),
    #     )

    #     # Bind the click event to the tray icon to show the window
    #     # self.icon._icon.visible = True  # Ensure the icon is visible

    #     # Run the system tray in a separate thread
    #     self.icon.run()
    #     self.refresh_tray_icon()
    #     # threading.Thread(target=self.icon.run, daemon=True).start()

    # def start_tray(self):
    #     """Start the tray in a separate thread"""
    #     threading.Thread(target=self.run_tray, daemon=True).start()

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
            print(f"An error occurred: {e}")
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
        self.hour_label.config(text=self.hours)
        self.minute_label.config(text=self.minutes)

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
                    f"{api_url}/timetrack/updatedFile", headers=headers
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
            if os.path.exists("SSTRACKSetup.exe"):
                os.remove("SSTRACKSetup.exe")
            with open("SSTRACKSetup.exe", "wb") as new_file:
                new_file.write(response.content)
                self.download = True
            print("SSTRACKSetup.exe downloaded successfully.")

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
            subprocess.Popen(["SSTRACKSetup.exe"])

        else:
            print("Failed to download SSTRACKSetup.exe.")

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
            self.root.wm_iconbitmap(self.resource_path("images/animatedlogo.ico"))
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
                    self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
                    if not self.is_timer_running:
                        self.is_timer_running = True
                        self.total = 0
                        # Re-enable the break button
                        self.break_button_enabled = True
                        self.break_button.config(
                            text="Break",
                            bg="#E8F4FC",  # Initial background color
                            fg="#7094B0",  # White text when break ends
                        )
                        threading.Thread(target=self.update_time).start()

                        # self.play_button.config(state=tk.DISABLED)
                        # self.pause_button.config(state=tk.NORMAL)
                        # Change play button image to play_icon_grey
                        self.canvas.itemconfig(self.play_button, image=self.play_icon_grey)

                        # Change pause button image to pause_icon
                        self.canvas.itemconfig(self.pause_button, image=self.pause_icon)
                        self.canvas.lift(self.pause_button)
                        # Unbind the click event for the play button to simulate disabling it
                        self.canvas.tag_unbind(self.play_button, "<Button-1>")
                        self.canvas.tag_bind(
                            self.pause_button, "<Button-1>", self.click_pause_button
                        )

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
                            self.minimize_window()
                        
                            # Create a notifier object
                            # message = 'no note'
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
                                # Display a notification with an icon
                                # Notifier.notify(
                                #     title="SSTRACK started",
                                #     message="Your break has been stopped. SSTRACK is started.",
                                #     timeout=3,  # Notification disappears after 3 seconds
                                #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
                                # )
                                os.system('terminal-notifier -title "SSTRACK started" -message "Your break has been stopped. SSTRACK is started." -appIcon "images/animatedlogo.png"')
                                # Your break has been stopped. SSTRACK is started.
                            else:
                            # self.breakExecution()
                            # self.start_Timer()
     
                                # Display a notification with an icon
                                # Notifier.notify(
                                #     title="SSTRACK started",
                                #     message=message,
                                #     timeout=3,  # Notification disappears after 3 seconds
                                #     app_icon="images/animatedlogo.ico"  # Provide the path to your icon file (e.g., .ico or .png)
                                # ) 
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
            print(f"An error occurred: {e}")
            return "N/A"


    # def click_break_button(self, event=None):
    #     if not self.break_button_enabled:
    #         self.break_button_enabled = True
    #         print("Break button is disabled. Click ignored.")
    #         self.setUpBreak()
    #         return
       
    #     if self.breakFound and self.parse_remaining_break_time(self.BreakTime) > 1:

    #         try:
            
    #             self.breakActive = True
    #             self.breakStartedOn = datetime.datetime.now(pytz.UTC)
    
                
    #             # Disable the break button
    #             self.break_button_enabled = False
    #             # Display a notification with an icon
    #             notification.notify(
    #                 title="Break started",
    #                 message="Your break has started",
    #                 timeout=3,
    #                 app_icon="images/animatedlogo.ico"
    #             )
    #             self.breakId = str(uuid.uuid4())
                
    #             # Start `startBreakTime` in a separate thread
    #             threading.Thread(target=self.startBreakTime, daemon=True).start()
    #         except Exception as e:
    #             print(f"Error starting break time: {e}")
    #     elif self.breakFound and self.parse_remaining_break_time(self.BreakTime) < 1:
    #         # Display a notification with an icon
    #             notification.notify(
    #                 title="Break Time",
    #                 message="The assigned break time has already been utilized",
    #                 timeout=3,
    #                 app_icon="images/animatedlogo.ico"
    #             )

    #     elif not self.breakFound:
    #         # Display a notification with an icon
    #             notification.notify(
    #                 title="Break Time",
    #                 message="No break time has been assigned by the company.",
    #                 timeout=3,
    #                 app_icon="images/animatedlogo.ico"
    #             )



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

    def logout(self):
        # Stop the timer if running
        if self.is_timer_running:
            self.click_pause_button()

        # Clear the stored data
        try:
            os.remove("data.pkl")
        except FileNotFoundError:
            pass

        try:
            os.remove(GUIApp.get_data_file_path("time_entry_id.pkl"))
        except FileNotFoundError:
            pass

        # Destroy the Tkinter root window
        # os.system("taskkill /f /im SSTRACK.exe")
        self.root.destroy()
        # Restart the main.py script as a new process
        subprocess.Popen([self.python_exe, "main.py"])

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
    root = tk.Tk()
    app = GUIApp(root)
    # Bind the protocol method to the window closing event
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
