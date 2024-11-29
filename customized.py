from tkinter import *
from tkinter import messagebox
import datetime
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageTk, ImageGrab, ImageDraw, Image
import pickle
import base64
import json
import tkinter as tk

import pyautogui
import time
import os
import threading
import io
import platform
from urllib.parse import urlparse
# from pynput import mouse, keyboard
import sys
import subprocess
import webbrowser
import threading
import keyboard
import requests
import pytz
import ctypes
# import PySimpleGUIQt as sg
import re
# import messagebox from tkinter module 
import tkinter.messagebox 
import uuid  # Import the UUID module for generating a unique ID
import socketio
from bson import ObjectId
# from pystray import Icon, Menu, MenuItem
# from infi.systray import SysTrayIcon
# from infi.systray.traybar import PostMessage, WM_CLOSE
import shutil
from ActivityMonitor import ActivityMonitor
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
        self.root.title("SSTRack_under_construction")
        self.root.geometry("700x340")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        # Set application icon
                # Resize the image and get both the PhotoImage and PIL Image objects
        # self.official_icon, self.icon_for_tray = self.resize_image('images/logo.png', 100, 100, 10)
        _, self.icon_for_tray = self.resize_image('/Users/charlie/Downloads/SSTRACKApp/images/logoTray.png', 50, 50, 5)
        self.icon = self.icon_for_tray
        
        self.official_icon, _ = self.resize_image(
            '/Users/charlie/Downloads/SSTRACKApp/images/logo.png', 100, 100, 10)
        self.root.iconphoto(True, self.official_icon)
        self.forgotTimer = False
        self.projectId = None  # Variable to store selected project ID
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
        self.disabled =False
        self.autoPauseenabled = False
        self.frequency = 2
        self.ssperhr = 30
        self.updated = False
        self.download = False
        self.current_v = '1.1.11'
        self.dailytime = "0h 0m"
        self.hours ='0h'
        self.minutes='0m'
        # self.check_for_update()
        self.check_for_update_lock = threading.Lock()  # Initialize the lock
        self.lock = threading.Lock()
        self.check_activity_lock = threading.Lock() 
        self.percentage = 0
        # Initialize the overall report timer (but don't start it yet)
        self.overall_report = ""  # Initialize an empty string to store the report
        self.weeklyTimeLimit='No limit'
        self.allowAddingOfflineTime = 0
        # Decode the Base64-encoded parts of the token
        # header, payload, signature = self.token.split('.')
        # # decoded_header = base64.urlsafe_b64decode(
        # #     header + '==').decode('utf-8')
        # decoded_payload = base64.urlsafe_b64decode(
        #     payload + '==').decode('utf-8')
        # self.user_info = json.loads(decoded_payload)
        # self.name = self.user_info["name"]
        # self.company = self.user_info["company"]
        # self.user_id = self.user_info['_id']
        self.trackingStart_list = []
        self.calledImmediate = False
        self.autoLaunch = False
        self.launch_monitor = False
        # threading.Thread(target=self.get_data).start()

        # Create and configure UI elements
        frame0 = Frame(self.root, width=700, height=80, bg="#0E4772")
        frame0.place(x=0, y=0)

        self.logo_icon = ImageTk.PhotoImage(file='/Users/charlie/Downloads/SSTRACKApp/images/sstracklogo.png')
        logo_label = Label(frame0, image=self.logo_icon, bg="#0E4772")
        logo_label.place(x=20, y=10)

        # Load setting icon with margin using the new method
        self.setting_icon = self.load_icon_with_margin('/Users/charlie/Downloads/SSTRACKApp/images/Settings_Icon.png', 20, 20, margin=10)
        self.setting_label = tk.Label(frame0, image=self.setting_icon, bg="#0E4772", cursor='hand2')
        self.setting_label.place(x=600, y=18)
        self.setting_label.bind("<Button-1>", lambda e: self.open_settings())


        # Load logout icon with margin using the new method
        self.logout_icon = self.load_icon_with_margin('/Users/charlie/Downloads/SSTRACKApp/images/log_out_white.png', 20, 20, margin=10)
        self.logout_button = tk.Label(frame0, image=self.logout_icon, bg="#0E4772", cursor='hand2')
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

        frame2 = Frame(self.root, width=700, height=150,
                       border=1, bg="#FFFFFF")
        frame2.place(x=50, y=100)

        self.username = Label(frame2, text=self.name, fg="#0E4772",
                         bg="#FFFFFF", font=('Roboto', 24, 'bold'))
        self.username.place(x=73, y=8)

        self.verified_icon, _ = self.resize_image(
            '/Users/charlie/Downloads/SSTRACKApp/images/verified.png', 35, 35, 10)      
        # Display the verified icon using a Label instead of a Button
        self.verified_label = tk.Label(frame2, image=self.verified_icon, bg="#ffffff", border=0)
        self.verified_label.place(x=20, y=0)


        
        # companies = [self.company]
        # max_option_width = max(len(option) for option in companies)
        # selected_company = tk.StringVar()
        # selected_company.set(companies[0])
        # company_dropdown = OptionMenu(frame2, selected_company, *companies)
        # company_dropdown.config(width=max_option_width + 5, height=1, fg="#FFFFFF", bg="#7ACB59", font=("Roboto", 15),
        #                         borderwidth=0)
        # company_dropdown.place(x=400, y=6)
        
        companies = [self.company]
        selected_company = tk.StringVar()
        newselected_company = tk.StringVar()
        selected_company.set(companies[0])  # Set the initial company to display\
        newselected_company  = selected_company.get()
        if len(newselected_company) > 11:
                newselected_company = newselected_company[:8] + '...'  # Truncate and add ellipsis
        # selected_company = newselected_company
        # max_option_width = max(len(companies[0])+4, 10)
        max_option_width = 12

        # Create a label to display the selected company
        company_label = tk.Label(
            frame2, text=newselected_company, fg="#FFFFFF", bg="#0E4772",
            font=("Roboto", 14), width=max_option_width  # Adjust width as needed
        )
        company_label.place(x=401, y=8)

        self.frame = Frame(root, width=700, height=150,border=1,bg="#FFFFFF")
        self.frame.place(x=60, y=160)

        self.description =None
        self.descriptions=Entry(self.frame, width=350,border=0,fg="#0E4772",bg="#FFFFFF",font=('Roboto', 18), highlightthickness=0)
        self.descriptions.place(x=20,y=10)
        self.placeholder = 'What project are you engaged in?'
        # self.descriptions = tk.Entry(self.self.frame, width=350, border=0, fg="#0E4772", font=('Roboto', 11))
        # self.descriptions.place(x=20, y=10)
        
# Bind the Enter key to the get_description_value function
        self.descriptions.bind('<Return>', self.get_description_value)
        self.descriptions.bind("<FocusIn>", self.on_focus_in)
        self.descriptions.bind("<FocusOut>", self.on_focus_out)
         # Limit characters based on the maximum width (350 pixels)
        self.max_characters = (self.calculate_max_characters() + 5)
        self.descriptions.bind("<KeyRelease>", self.limit_text_length)
        
        # Set the initial value based on existing description
        if self.description:
            self.descriptions.insert(0, self.description)
        else:
            self.set_placeholder()
            
        Frame(self.frame, width=350, height=2, bg='#0E4772').place(x=20, y=35)
        self.projects = ["+ Project"]
        self.project_map = []
        self.selected_project = tk.StringVar()
        self.selected_project.set(self.projects[0])
        self.selected_project.trace("w", self.callback)  # Monitor changes in selection

        # Load dropdown icon
        self.vector = PhotoImage(file="/Users/charlie/Downloads/SSTRACKApp/images/Vector.png")

        self.button_frame = tk.Frame(self.frame, bg="#0E4772", height=30, width=140)  # Set fixed height and width
        self.button_frame.place(x=390, y=6)  # Place at specific coordinates

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
        self.icon_label.pack(side="right")
        self.button_frame.bind("<Button-1>", lambda e: self.show_menu())

        # Bind the label click to the show_menu command
        self.icon_label.bind("<Button-1>", lambda e: self.show_menu())
        # To ensure the frame's width is enforced, prevent it from resizing with `propagate`
        self.button_frame.pack_propagate(False)

        # Create a menu for the dropdown
        self.projects_dropdown = tk.Menu(self.frame, tearoff=0, bg="#FFFFFF", fg="#000000", font=("Roboto", 10))

        # Bind dropdown update
        self.update_projects_dropdown()  # Initial population of dropdown menu


        frame1 = Frame(self.root, width=700, height=110, bg="#0E4772")
        frame1.place(x=0, y=230)

        # Resize the images
        self.play_icon, _ = self.resize_image('/Users/charlie/Downloads/SSTRACKApp/images/playButton.png', 70, 70, 10)
        self.pause_icon_grey, _ = self.resize_image('/Users/charlie/Downloads/SSTRACKApp/images/Pause_Icon_Grey.png', 60, 60, 10)
        self.play_icon_grey, _ = self.resize_image('/Users/charlie/Downloads/SSTRACKApp/images/Play_Icon_Grey.png', 70, 70, 10)
        self.pause_icon, _ = self.resize_image('/Users/charlie/Downloads/SSTRACKApp/images/Pause_Red.png', 60, 60, 10)
               # Create the play button
        # Create a Canvas widget to hold the images (transparent effect)
        self.canvas = tk.Canvas(frame1, width=700, height=110, bg="#0E4772", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Adjust the y-position for images to align them properly like before
        y_position = 5  # Same as you had with Button.place(y=5)

        # Add the play button to the canvas (place at x=40, y=5 like the original Button)
        self.play_button = self.canvas.create_image(40, y_position, image=self.play_icon, anchor=tk.NW)
        self.canvas.tag_bind(self.play_button, '<Button-1>', self.click_play_button)

        # Add the pause button to the canvas (place at x=100, y=10 to avoid overlap)
        self.pause_button = self.canvas.create_image(100, y_position + 8, image=self.pause_icon_grey, anchor=tk.NW)
        self.canvas.tag_bind(self.pause_button, '<Button-1>', self.click_pause_button)  # Bind the click event for the pause button

        # Lower the play button to make sure pause is on top
        self.canvas.lift(self.play_button)

        # Bind mouse enter and leave events for the play button
        self.canvas.tag_bind(self.play_button, '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind(self.play_button, '<Leave>', lambda e: self.canvas.config(cursor=''))

        # Bind mouse enter and leave events for the pause button
        self.canvas.tag_bind(self.pause_button, '<Enter>', lambda e: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind(self.pause_button, '<Leave>', lambda e: self.canvas.config(cursor=''))

        # Initially hide the pause button (like before)
        # self.canvas.itemconfig(self.pause_button, state='hidden')


        # Initially enable the play button and disable the pause button
        # self.play_button.config(state=tk.NORMAL)
        # self.pause_button.config(state=tk.DISABLED)


        tk.Label(frame1, text="Today", fg="#7ACB59", bg="#0E4772",
                 font=('Roboto', 15)).place(x=320, y=20)

        # self.dailytime_label = tk.Label(frame1, text=self.dailytime, fg="#FFFFFF", bg="#0E4772",
        #                                 font=('Roboto', 25, 'bold'))
        # self.dailytime_label.place(x=320, y=47)
                # Create Labels for hours, colon, and minutes
        self.hour_label = tk.Label(frame1, text=self.hours, fg="#FFFFFF", bg="#0E4772",
                                    font=('Roboto', 25, 'bold'))  # Fixed width
        self.colon_label = tk.Label(frame1, text=":", fg="white", bg="#0E4772",
                                    font=('Roboto', 25, 'bold'))
        self.minute_label = tk.Label(frame1, text=self.minutes, fg="#FFFFFF", bg="#0E4772",
                                    font=('Roboto', 25, 'bold'))  # Fixed width

        # Place the labels
        # self.hour_label.place(x=320, y=47)
        # self.colon_label.place(x=365, y=47)  # Adjust x based on width of hour_label
        # self.minute_label.place(x=380, y=47)  # Adjust x based on width of colon_label
        
        # Place the labels initially at arbitrary positions
        self.hour_label.place(x=320, y=47)

        # Adjust positions based on the length of hours
        if len(self.hours) == 2:  # Single-digit hour
            colon_x = 320 + 57  # Adjust for single-digit hour (add 30 pixels to x)
            minute_x = colon_x + 15  # Adjust minute label (15 pixels after colon)
        else:  # Double-digit hour
            colon_x = 320 + 60  # Adjust for double-digit hour (add 50 pixels to x)
            minute_x = colon_x + 15  # Adjust minute label (15 pixels after colon)

        # Place the colon and minute labels based on the calculated positions
        self.colon_label.place(x=colon_x, y=47)
        self.minute_label.place(x=minute_x, y=47)

        self.TIMELINE, _ = self.resize_image('/Users/charlie/Downloads/SSTRACKApp/images/timeline.png', 160, 40, 0)
        TIMELINE_label = tk.Button(frame1, image=self.TIMELINE, bg="#0E4772",
                                   border=0, command=self.view_Timeline, cursor='hand2')
        TIMELINE_label.place(x=480, y=40)
        self.python_exe = sys.executable
        self.fetch_data_lock = threading.Lock()
        # self.add_shortcut_to_startup()  # Add SSTRACK to startup

        self.check_permissions()
        threading.Thread(target=self.start_listeners, daemon=True).start()
        # Start the first update check immediately upon initialization
        self.schedule_update_check()
        self.screenshot_data_list = []
        self.sleep_mood = False
        self.exact_time = datetime.datetime.now(pytz.UTC)
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
        # self.check_newDay_lock = threading.Lock()
        
        self.updateProject_lock = threading.Lock()
        self.update_daily_time_lock = threading.Lock()
        self.click_pause_button_lock = threading.Lock()
        self.employeeSetting_lock = threading.Lock()
        # Create mouse and keyboard listeners
        # self.mouse_listener = mouse.Listener(
        #     on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        # self.keyboard_listener = keyboard.Listener(
        #     on_press=self.on_press, on_release=self.on_release)
        self.total = 0
        # Start the listeners
        self.last_mouse_position = pyautogui.position()     
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
      
      
   
    def check_permissions(self):
        if platform.system() == "Darwin":  # Check if the platform is macOS
            import ctypes
            try:
                # Load macOS Accessibility API
                AXIsProcessTrusted = ctypes.cdll.LoadLibrary(
                    "/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices"
                ).AXIsProcessTrusted
            
                # Check if permissions are granted
                if not AXIsProcessTrusted():
                    print("Accessibility permissions not granted.")
                    tkinter.messagebox.showwarning(
                        "Permissions Required",
                        "Accessibility permissions are not granted.\n\n"
                    "Please enable them in System Preferences > Security & Privacy > Accessibility."
                    )
                    # Open the System Preferences window for Accessibility
                    subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"])
                    return False
                else:
                    print("Accessibility permissions granted.")
                    return True

            except Exception as e:
                print(f"Error checking permissions: {e}")
                return False
        elif platform.system() == "Windows":
            # Optional for Windows: Inform the user to run the app as Administrator
            print("Ensure the application is running with administrator privileges.")
            return True
        else:
            print("Unsupported platform.")
            return False


   
   
        
    def start_listeners(self):
        # Start the listeners
        self.fetch_data()
        self.userProject()
        self.checkAutoLaunch()
        self.employeeSetting()
        self.fetch_projects()
        self.connect_to_server()
    
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
            response = requests.get("https://myuniversallanguages.com:9093/api/v1/timeTrack/userProject", headers=headers)
            if response.status_code == 200:
                projects_data = response.json()
                project = projects_data.get('data').get('projectId')
                description = projects_data.get('data').get('proDescription')
                if description is not None and description != 'null' and description != '':
                    self.description = description
                    self.descriptions.delete(0, tk.END)  # Clear the entry widget
                    self.descriptions.insert(0, self.description)
                if project is not None:
                    self.projectId = project.get('_id')
                    selected_project_name = project.get('name')
                    self.selected_project.set(selected_project_name)
                else:
                    self.selected_project.set("+ Project")
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
            response = requests.get("https://myuniversallanguages.com:9093/api/v1/timeTrack/getProjects", headers=headers)
            if response.status_code == 200:
                projects_data = response.json()
                project_list = projects_data.get('projects')
                for pro in project_list:
                    pro_name = pro.get('name')
                    pro_id = pro.get('_id')
                    if pro_name not in self.projects:
                        self.projects.append(pro_name)
                    self.project_map.append({'projectname': pro_name, 'projectid': pro_id})
                self.update_projects_dropdown()  # Update dropdown with new projects
            else:
                print(f"Failed to fetch projects: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error fetching projects: {e}")


    def update_projects_dropdown(self):
        try:
            # Clear existing menu options
            self.projects_dropdown.delete(0, 'end')

            # Calculate a fixed width based on the button width
            fixed_width = 15  # Set a fixed width in terms of characters

            for project in self.projects:
                # Add project with fixed length (by padding spaces)
                padded_label = project.ljust(fixed_width)  # Pad to fixed width
                self.projects_dropdown.add_command(
                    label=padded_label, command=lambda p=project: self.selected_project.set(p)
                )
                self.fixProject()

            # Update button text to selected project with ellipsis if necessary
           
        except Exception as e:
            print(f"An error occurred: {e}")

    def fixProject(self):
        selected_project_name = self.selected_project.get()
        if len(selected_project_name) > 11:
                selected_project_name = selected_project_name[:8] + '...'  # Truncate and add ellipsis
        self.button["text"] = selected_project_name 

    # def callback(self, *args):
    #     print(f"Selected project changed to: {self.selected_project.get()}")
    #     self.button["text"] = self.selected_project.get()  # Update button text when selection changes

    # Function to update projects dropdown
    # def update_projects_dropdown(self, event=None):
    #     try:
    #         # self.fetch_projects()
    #         projects_with_plus = [project for project in self.projects]
    #         max_option_width = max(len(option) for option in projects_with_plus)
    #         # self.selected_project.set(projects_with_plus[0])  # Update default selection
    #         self.projects_dropdown['menu'].delete(0, 'end')  # Clear existing menu
    #         for project in projects_with_plus:
    #             self.projects_dropdown['menu'].add_command(label=project, command=tk._setit(self.selected_project, project))
    #         self.projects_dropdown.config(width=max_option_width + 5)  # Adjust dropdown width if needed
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return None


    def callback(self, *args):
        print(f"the variable has changed to '{self.selected_project.get()}'")
        self.button["text"] = self.selected_project.get()  # Update button text when selection changes
        self.fixProject()
        self.on_project_select(self.selected_project.get())
    
    def updateProject(self):
        try:
            with self.updateProject_lock:
                data={
                        "projectId": self.projectId,
                        "projectDescription" : self.description,
                    }
                api_url = "https://myuniversallanguages.com:9093/api/v1"
                headers = {
                "Authorization": "Bearer " + self.token,
            }
                response = requests.post(
                    f"{api_url}/timetrack/updateProject",
                                    headers=headers,
                                    data=data)
                if response.ok:
                    data= response.json()
                    print("project updated", data)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    # Callback function to handle project selection
    def on_project_select(self, selected_project):
        try:
            # Remove the "+" from the project name
                # Find project ID from self.project_map
            for project in self.project_map:
                if project['projectname'] == selected_project:
                    self.projectId = project['projectid']
                    break
                else:
                    self.projectId=None
            if self.projectId:
                threading.Thread(target=self.updateProject).start()
                # self.updateProject()
                    
                # Save selected Project ID to projectId.pkl
                with open("projectId.pkl", "wb") as f:
                    pickle.dump(self.projectId, f)
                print(f"Selected Project ID: {self.projectId}")
            if self.is_timer_running:
                # self.is_timer_running = False
                self.restartTimer()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
            

    def set_placeholder(self):
        print("Setting placeholder")  # Debugging statement
        self.descriptions.delete(0, tk.END)  # Clear the entry widget
        self.descriptions.insert(0, self.placeholder)
        self.descriptions.config(fg='grey')

    def get_description_value(self, event=None):
        try:
            print("hello description value")
            value = self.descriptions.get()
            if value == self.placeholder:
                value = ""
    # Only update if the new value is different from the current description
            if value != self.description:
                self.description=value
            
                if self.description:
                    self.descriptions.delete(0, tk.END)  # Clear the entry widget
                    self.descriptions.insert(0, self.description)
                threading.Thread(target=self.updateProject).start()
                    # self.updateProject()
                    
                print(value)  # or process the value as needed
                if self.description and self.is_timer_running:
                    # self.is_timer_running = False
                    self.restartTimer()
                # Move focus to root window to avoid blinking cursor
            self.frame.focus_set()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def on_focus_in(self, event):
        print("Focus in event triggered")  # Debugging statement
        if self.descriptions.get() == self.placeholder:
            self.descriptions.delete(0, tk.END)
            self.descriptions.config(fg='#0E4772')

    def on_focus_out(self, event):
        print("Focus out event triggered")  # Debugging statement
        if not self.descriptions.get() or self.descriptions.get() == "":
            self.set_placeholder()
            
            
    def view_Timeline(self):
        url = f"https://www.sstrack.io/{self.token}"
        webbrowser.open(url, new=2)  # Open in a new tab if possible


    def employeeSetting(self):
        # Replace with the actual API URL
        try:
            with self.employeeSetting_lock:
                headers = {
                    "Content-Type": "application/json",
                }

                response = requests.get(
                    f"https://myuniversallanguages.com:9093/api/v1/superAdmin/Settings/{self.user_id}", headers=headers)
                if response.ok:
                    json_data = response.json()
                    # Use get() to handle missing keys gracefully
                    if json_data.get("employeeSettings", {}):
                        self.settings = json_data.get("employeeSettings", {})
                        print(self.settings)
                        self.updateSettings()
                else:
                    print(
                        f"Failed to get data from:/superAdmin/Settings {response.status_code} - {response.text}")
                    return "N/A"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"


    def updateSettings(self):
        try:
            print(f"effective setting {self.settings}")
            self.autoPauseenabled =   self.settings.get("autoPauseTrackingAfter", {}).get("pause")
            if self.autoPauseenabled:
                self.autoPauseTrackingAfter = self.settings.get("autoPauseTrackingAfter", {}).get("frequency")
            else:
                self.autoPauseTrackingAfter = 0    
            effectscreenshot = self.settings.get("screenshots")
            self.ssperhr = effectscreenshot.get('frequency')
            self.ssenable = effectscreenshot.get('enabled')
            self.weeklyTimeLimit = self.settings.get("weeklyTimeLimit")
            if self.weeklyTimeLimit == 0:
                self.weeklyTimeLimit='No limit'
            self.allowAddingOfflineTime = self.settings.get("allowAddingOfflineTime")
            if not self.ssenable:
                self.disabled =True
            else:
                self.disabled=False        
                
            # Extract numeric part using regular expression
            match = re.search(r'\d+', self.ssperhr)
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
            if os.path.isfile("data.pkl"):
                with open("data.pkl", "rb") as f:
                    stored_data = pickle.load(f)
                    self.token = stored_data
            # Decode the Base64-encoded parts of the token
            header, payload, signature = self.token.split('.')
            # decoded_header = base64.urlsafe_b64decode(
            #     header + '==').decode('utf-8')
            decoded_payload = base64.urlsafe_b64decode(
                payload + '==').decode('utf-8')
            self.user_info = json.loads(decoded_payload)
            self.name = self.user_info["name"]
            nameLength = len(self.name)
            # Format name based on length
            if nameLength > 19:
                self.name = self.name[:18] + "..."  # Take the first 16 characters and add "..."
            else:
                self.name = self.name  # Use the full name if it's 19 characters or less
            self.company = self.user_info["company"]
            self.user_id = self.user_info['_id']
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
        tk.Label(settings_window, text="Team settings (set by company manager)", font=title_font, bg="#F0F0F0").grid(row=0, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # First column labels and values
        tk.Label(settings_window, text="Screenshots:", font=label_font, bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="30/hr", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(settings_window, text="Auto-pause tracking:", font=label_font, bg="#F0F0F0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="40 min", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(settings_window, text="Weekly time limit:", font=label_font, bg="#F0F0F0").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="No limit", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Second column labels and values
        tk.Label(settings_window, text="Allow adding offline time:", font=label_font, bg="#F0F0F0").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="No", font=label_font, fg="#F44336", bg="#F0F0F0").grid(row=1, column=3, padx=10, pady=5, sticky="w")

        tk.Label(settings_window, text="Activity Level tracking:", font=label_font, bg="#F0F0F0").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="Yes", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=2, column=3, padx=10, pady=5, sticky="w")

        tk.Label(settings_window, text="App & URL tracking:", font=label_font, bg="#F0F0F0").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="Yes", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Add buttons at the bottom, with responsiveness
        # save_button = tk.Button(settings_window, text="Save", width=12, height=1, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief="flat", command=self.save_settings)
        # cancel_button = tk.Button(settings_window, text="Cancel", width=12, height=1, bg="#F44336", fg="white", font=("Arial", 10, "bold"), relief="flat", command=settings_window.destroy)

        # save_button.grid(row=5, column=2, pady=20, padx=20, sticky="e")
        # cancel_button.grid(row=5, column=3, pady=20, padx=20, sticky="w")

        # Make sure focus stays on the settings window
        settings_window.grab_set()



    def open_settings(self):
           # Resize the icon to a smaller size
        self.settings_icon, _ = self.resize_image('/Users/charlie/Downloads/SSTRACKApp/images/logoTray.png', 20, 20, 10)

        # Create a new Toplevel window for the popup
        settings_popup = tk.Toplevel(self.root)
        settings_popup.title("Settings")
        settings_popup.geometry("700x340")
        settings_popup.configure(bg="#0E4772")
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
            settings_popup.geometry(f"+{settings_popup.winfo_x() + dx}+{settings_popup.winfo_y() + dy}")

        settings_popup.bind("<Button-1>", start_move)
        settings_popup.bind("<ButtonRelease-1>", stop_move)
        settings_popup.bind("<B1-Motion>", on_motion)

        # Header section with title, icon, and close (X) button
        header_frame = tk.Frame(settings_popup, bg="#0E4772")
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        # Set row height for the header frame (use a smaller value)
        settings_popup.grid_rowconfigure(0, minsize=30)  # Adjust the height as needed

        # Load the resized icon
        icon_label = tk.Label(header_frame, image=self.settings_icon, bg="#0E4772")
        icon_label.grid(row=0, column=0, padx=(5, 0), sticky="w")  # Reduced padding

        # Title label with smaller font
        title_label = tk.Label(header_frame, text="Settings", font=("Arial", 10), bg="#0E4772")
        title_label.grid(row=0, column=1, padx=(2, 5), sticky="w")  # Reduced padding

        # Close button with smaller font
        close_button = tk.Button(header_frame, text="x", font=("Arial", 12, "bold"), bg="white", fg="black", relief="flat", command=settings_popup.destroy)
        close_button.grid(row=0, column=2, padx=5, sticky="e")  # Reduced padding

        # Adjust the column weights for proper alignment
        header_frame.grid_columnconfigure(0, weight=0)  # Icon column doesn't expand
        header_frame.grid_columnconfigure(1, weight=1)  # Title column expands
        header_frame.grid_columnconfigure(2, weight=0)  # Button column doesn't expand

        # Hover effect for the close button
        def on_enter(event):
            close_button['background'] = "#F44336"  # Red on hover
            close_button['foreground'] = "white"

        def on_leave(event):
            close_button['background'] = "white"  # White when not hovered
            close_button['foreground'] = "black"

        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)
    
        # Hover effect for the close button
        def on_enter(event):
            close_button['background'] = "#F44336"  # Red on hover
            close_button['foreground'] = "white"

        def on_leave(event):
            close_button['background'] = "white"  # White when not hovered
            close_button['foreground'] = "black"

        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

        # Hover effect for the close button
        def on_enter(event):
            close_button['background'] = "#F44336"  # Red on hover
            close_button['foreground'] = "white"

        def on_leave(event):
            close_button['background'] = "white"  # White when not hovered
            close_button['foreground'] = "black"

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
        tk.Label(settings_popup, text="User Settings", font=title_font, bg="#0E4772").grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # Checkboxes for launch and auto-start functionality
        tk.Checkbutton(settings_popup, text="Launch SSTRACK when I start Windows", variable=self.launch_monitor_var, bg="#0E4772").grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        tk.Checkbutton(settings_popup, text="Automatically start tracking when I launch SSTRACK", variable=self.auto_start_var, bg="#0E4772").grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Add traces to detect checkbox changes
        self.launch_monitor_var.trace("w", lambda *args: self.on_launch_monitor_change())
        self.auto_start_var.trace("w", lambda *args: self.on_auto_start_change())

        # Team Settings Section
        tk.Label(settings_popup, text="Team settings (set by company manager)", font=title_font, bg="#0E4772").grid(row=4, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # Screenshots
        tk.Label(settings_popup, text="Screenshots:", font=label_font, bg="#0E4772", anchor="e").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        tk.Label(settings_popup, text=self.ssperhr, font=label_font, fg="#4CAF50", bg="#0E4772", anchor="w").grid(row=5, column=1, padx=5, pady=2, sticky="w")

        # Auto-pause tracking
        tk.Label(settings_popup, text="Auto-pause tracking:", font=label_font, bg="#0E4772").grid(row=6, column=0, padx=5, pady=2, sticky="w")
        tk.Label(settings_popup, text=str(self.autoPauseTrackingAfter) + " min", font=label_font, fg="#4CAF50", bg="#0E4772").grid(row=6, column=1, padx=5, pady=2, sticky="w")

        # Weekly time limit
        tk.Label(settings_popup, text="Weekly time limit:", font=label_font, bg="#0E4772").grid(row=7, column=0, padx=5, pady=2, sticky="w")
        tk.Label(settings_popup, text=self.weeklyTimeLimit, font=label_font, fg="#4CAF50", bg="#0E4772").grid(row=7, column=1, padx=5, pady=2, sticky="w")

        # Allow adding offline time
        tk.Label(settings_popup, text="Allow adding offline time:", font=label_font, bg="#0E4772").grid(row=5, column=2, padx=5, pady=2, sticky="w")
        tk.Label(settings_popup, text="Yes" if self.allowAddingOfflineTime else "No", font=label_font, fg="#4CAF50", bg="#0E4772").grid(row=5, column=3, padx=5, pady=2, sticky="w")

        # Activity Level tracking
        tk.Label(settings_popup, text="Activity Level tracking:", font=label_font, bg="#0E4772").grid(row=6, column=2, padx=5, pady=2, sticky="w")
        tk.Label(settings_popup, text="Yes", font=label_font, fg="#4CAF50", bg="#0E4772").grid(row=6, column=3, padx=5, pady=2, sticky="w")

        # App & URL tracking
        tk.Label(settings_popup, text="App & URL tracking:", font=label_font, bg="#0E4772").grid(row=7, column=2, padx=5, pady=2, sticky="w")
        tk.Label(settings_popup, text="Yes", font=label_font, fg="#4CAF50", bg="#0E4772").grid(row=7, column=3, padx=5, pady=2, sticky="w")

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
        tk.Label(settings_window, text="Team settings (set by company manager)", font=title_font, bg="#F0F0F0").grid(row=0, column=0, columnspan=4, padx=20, pady=10, sticky="w")

        # First column labels and values
        tk.Label(settings_window, text="Screenshots:", font=label_font, bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="30/hr", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(settings_window, text="Auto-pause tracking:", font=label_font, bg="#F0F0F0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="40 min", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(settings_window, text="Weekly time limit:", font=label_font, bg="#F0F0F0").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="No limit", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Second column labels and values
        tk.Label(settings_window, text="Allow adding offline time:", font=label_font, bg="#F0F0F0").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="No", font=label_font, fg="#F44336", bg="#F0F0F0").grid(row=1, column=3, padx=10, pady=5, sticky="w")

        tk.Label(settings_window, text="Activity Level tracking:", font=label_font, bg="#F0F0F0").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="Yes", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=2, column=3, padx=10, pady=5, sticky="w")

        tk.Label(settings_window, text="App & URL tracking:", font=label_font, bg="#F0F0F0").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        tk.Label(settings_window, text="Yes", font=label_font, fg="#4CAF50", bg="#F0F0F0").grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Add buttons at the bottom, with responsiveness
        save_button = tk.Button(settings_window, text="Save", width=12, height=1, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief="flat", command=self.save_settings)
        cancel_button = tk.Button(settings_window, text="Cancel", width=12, height=1, bg="#F44336", fg="white", font=("Arial", 10, "bold"), relief="flat", command=settings_window.destroy)

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
        image = Image.new('RGB', (width, height), (255, 255, 255))
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
                confirm = messagebox.askyesno("App Closing", "Are you sure you want to stop the SSTRACK?")
                if confirm:
                    # self.icon = self.custom_shutdown()
                    self.click_pause_button()  # Pause tracking before exiting
                    # self.icon.stop()  # Safely remove the tray icon
                    #         # self.root.quit()  # Close the application
                    print("removed icon")
                    # Delay the process termination to allow time for the icon to be removed
                    threading.Timer(1, self.stop_process).start()  # Delay for 1 second        
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"

 
    def run_tray(self):
        # Set up the tray icon with a click event to show the window
        self.icon = Icon(
            "my_app", 
            self.icon_for_tray, 
            "SSTRACK", 
            menu=Menu(
                MenuItem('Show', self.show_window),  # Show window menu item
                MenuItem('Quit', self.on_quit)       # Quit menu item
            )
        )

        # Bind the click event to the tray icon to show the window
        self.icon._icon.visible = True  # Ensure the icon is visible
        
        # Run the system tray in a separate thread
        threading.Thread(target=self.icon.run, daemon=True).start()  


                       
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
                    with open("time_entry_id.pkl", "rb") as f:
                        timeEntryId = pickle.load(f)
                        current_time = datetime.datetime.now(pytz.UTC)
                        formatted_time = current_time.strftime("%I-%M-%S-%p_%m-%d-%Y")

                        filename = f"screenshot_{formatted_time}_{self.user_id}"
                        print(filename)
                        
                        if os.path.isfile("screenshots_data.pkl"):
                            try:
                                with open("screenshots_data.pkl", "rb") as f:
                                    try:
                                        self.screenshot_data_list = pickle.load(f)
                                    except pickle.UnpicklingError as e:
                                        # Handle the unpickling error gracefully
                                        print(f"Error while unpickling: {e}. Skipping loading screenshots data.")
                                        self.screenshot_data_list = []  # Initialize empty list or take appropriate action
                            except EOFError:
                                # Handle the case when there is no data in the file
                                self.screenshot_data_list = []  # or any other appropriate action
                                
                    screenshots_data = {"files": {"file": (f"{filename}.jpeg", screenshot_data, "image/jpeg")},
                                        "description": active_window_url,
                                        "activityPercentage": self.percentage,
                                        # "activityPercentage": 90,
                                        "startTime": self.startTime,
                                        "createdAt": current_time,
                                        "timeEntryId": timeEntryId,
                                        "disabled": self.disabled
                                        }
                    self.screenshot_data_list.append(screenshots_data)
                    with open("screenshots_data.pkl", "wb") as f:
                        pickle.dump(self.screenshot_data_list, f)
                    if len(self.trackingStart_list) > 0:
                        self.start_Timer()    
                    threading.Thread(target=self.addScreenshots).start()
                    self.startTime = datetime.datetime.now(pytz.UTC)
                    
        except Exception as e:
            print(f"An error occurred: {e}")
            # return "N/A"






    def check_activity(self):
        """Track user activity at regular intervals."""
        try:
            print("Starting activity check loop...")
            self.startTime = datetime.datetime.now(pytz.UTC)
            while self.is_timer_running:
                print("Starting new iteration of activity check.")
    
                with self.check_activity_lock:
                    print("Acquired check_activity_lock.")
    
                    # Check for mouse and keyboard activity
                    self.activity_monitor.check_mouse_activity()
                    self.activity_monitor.check_keyboard_activity()
    
                    # Log activity detection
                    print(f"Activity flag after checks: {self.activity_monitor.activity_flag}")
                    
                    # Update intervals
                    self.total_intervals += 1
    
                    if self.activity_monitor.activity_flag:  # Use the activity flag from the monitor
                        self.active_intervals += 1
                        print(f"Active intervals: {self.active_intervals}")
    
                # Calculate percentage every `activityinterval` intervals
                if self.total_intervals >= self.activityinterval:
                    if self.total_intervals > 0:
                        self.percentage = (self.active_intervals / self.total_intervals) * 100
                    else:
                        self.percentage = 0
    
                    print(f"Calculated percentage: {self.percentage}")
    
                    # Reset intervals
                    self.total_intervals = 0
                    self.active_intervals = 0
                    print("Resetting total and active intervals.")
    
                    # Handle activity based on percentage
                    threading.Thread(target=self.screenshots_data, daemon=True).start()
                    if self.percentage == 0:
                        self.total += 1
                        if self.total >= int(self.autoPauseTrackingAfter / self.frequency):
                            print("Pausing due to no activity.")
                    else:
                        self.total = 0
                        print("Activity detected, resetting total counter.")
    
                # Reset the activity flag after processing the interval
                # Only reset if no activity was detected within the last 10 seconds
                if time.time() - self.startTime.timestamp() > 10:
                    with self.lock:
                        self.activity_monitor.activity_flag = False
                        print(f"Resetting activity flag: {self.activity_monitor.activity_flag}")
    
                # Sleep for the interval duration (10 seconds)
                print("Sleeping for 10 second...")
                time.sleep(10)
    
        except Exception as e:
            print(f"An error occurred in check_activity: {e}")
    

   
   
    
    
    def addScreenshotsold(self):
        try:
            if len(self.trackingStart_list) == 0:

                if self.is_timer_running:
                    with self.screenshots_add_lock:
                        try:
                            with open("screenshots_data.pkl", "rb") as f:
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
                                        screenshot_data = self.screenshot_data_list[index]

                                        files = screenshot_data['files']
                                        timeEntryId = screenshot_data['timeEntryId']

                                        response = requests.patch(
                                            f"{api_url}/timetrack/time-entries/{timeEntryId}/screenshotss",
                                            headers=headers,
                                            files=files,
                                            data=screenshot_data
                                        )

                                        if response.ok:
                                            data = response.json()
                                            
                                            # Use get to avoid potential KeyError
                                            filename = data.get('filename')

                                            if filename and self.screenshot_data_list:
                                                # Check if filename exists in the list and remove the corresponding item
                                                for i, item in enumerate(self.screenshot_data_list):
                                                    if item.get('files', {}).get('file', ('',))[0] == filename:
                                                        # exactname = ssname[0]
                                                        # if item.get('files', {}).get('file', ('',)).name == filename:
                                                        del self.screenshot_data_list[i]
                                                        index = 0
                                                        with open("screenshots_data.pkl", "wb") as f:
                                                            pickle.dump(
                                                                self.screenshot_data_list, f)
                                                        break
                                            else:
                                                print("Failed to get filename from response.")
                                                break

                                        else:
                                            print(f"Failed to get data:/addScreenshotsold {response.status_code} - {response.text}")
                                            break

                                except requests.exceptions.RequestException as internet_error:
                                    # Handle internet-related errors, such as connection issues
                                    print("Internet issue:", internet_error)
                                    return None
                        except FileNotFoundError:
                            # Handle the case where the pickle file doesn't exist or is empty
                            print("file not found")
                            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"

        
    def addScreenshots(self):
        try:
            if len(self.trackingStart_list) == 0:

                if self.is_timer_running:
                    with self.screenshots_add_lock:
                        try:
                            with open("screenshots_data.pkl", "rb") as f:
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
                                        screenshot_data = self.screenshot_data_list[index]
                                        count = 0
                                        files = screenshot_data['files']
                                        timeEntryId = screenshot_data['timeEntryId']

                                        response = requests.patch(
                                            f"{api_url}/timetrack/time-entries/{timeEntryId}/screenshotss",
                                            headers=headers,
                                            files=files,
                                            data=screenshot_data
                                        )

                                        if response.ok:
                                            data = response.json()
                                            
                                            # Use get to avoid potential KeyError
                                            filename = data.get('filename')

                                            # Remove the first item from the list
                                            self.screenshot_data_list.pop(0)
                                            # Reset index to 0
                                            index = 0
                                            with open("screenshots_data.pkl", "wb") as f:
                                                pickle.dump(self.screenshot_data_list, f)
                                            
                                            if len(self.screenshot_data_list) == 0:
                                                self.fetch_data()
                                           
                                        else:
                                            print(f"Failed to get data:addScreenshots {response.status_code} - {response.text}")
                                            count += 1
                                            if count >= 3:
                                                # Skip this item for now and move to the next one
                                                print(f"Skipping item {index} after 3 failed attempts")
                                                count = 0  # Reset the count for the next item
                                                index += 1  # Move to the next item
                                            else:
                                                # Retry the same item
                                                print(f"Retrying item {index}, attempt {count}")
                                                self.screenshot_data_list.pop(0)
                                                index = 0

                                except requests.exceptions.RequestException as internet_error:
                                    # Handle internet-related errors, such as connection issues
                                    print("Internet issue:", internet_error)
                                    return None  # This will stop the function from continuing

                        except FileNotFoundError:
                            # Handle the case where the pickle file doesn't exist or is empty
                            print("file not found"),
                            return None  # This will stop the function from continuing
            else:
                threading.Thread(target=self.start_Timer).start()    
                   
        except Exception as e:
            print(f"An error occurred: {e}"),
            return None  # This will stop the function from continuing




    def on_activity(self):
        self.activity_flag = True
        print("Activity detected!")



    def get_active_window_hostname(self):
        try:
            if platform.system() == "Windows":
                try:
                    active_window = gw.getActiveWindow()
                    if active_window:
                        print(f"active window",active_window.title)
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
                            0].strip()
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
                        ["osascript", "-e", 'tell application "System Events" to name of first application process whose frontmost is true']).strip()
                    return active_app_name
                except subprocess.CalledProcessError:
                    pass
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"

    def resize_image(self, image_path, width, height, margin):
        img = Image.open(image_path)
        img = img.resize((width, height))
        img_with_margin = Image.new(
            "RGBA", (width + 2 * margin, height + 2 * margin), (255, 255, 255, 0))
        img_with_margin.paste(img, (margin, margin))
        return ImageTk.PhotoImage(img_with_margin), img_with_margin


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
                        self.colon_label.config(fg="white" if self.colon_label.cget("fg") == "#0E4772" else "#0E4772")
                    
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
                            self.colon_label.config(fg="#0E4772")  # Make colon invisible (background color)
                        else:
                            self.colon_label.config(fg="white")  # Make colon visible (white color)

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
                    hour = int(self.hours[:-1])
                    # Remove the last character "m" and convert to an integer
                    minute = int(self.minutes[:-1])

                    # Simulate time passing, add 1 minute in a loop
                    minute += 1

                    if minute >= 60:
                        hour += 1
                        minute -= 60

                    # Format the updated time back into the "1h 24m" format
                    self.hours = f"{hour}h"
                    self.minutes = f"{minute}m"
                    self.dailytime = f"{hour}h {minute}m"
                    # self.dailytime_label.config(text=self.dailytime)
                    print("Updated Time:", self.dailytime)
                    self.hoursLength()
                    
            except Exception as e:
                print(f"Error occured while fetching data: {e}")
                return None



    # def get_data(self):
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
                        f"{api_url}/timetrack/hours", headers=headers)
                    if response.ok:
                        json_data = response.json()
                        data = json_data["data"]
                        self.dailytime = data['totalHours']['daily']
                        
                        # Extract hours and minutes from the string (e.g., '0h 22m')
                        self.hours = self.dailytime.split(' ')[0].strip()  # Get the part before 'h' for hours
                        self.minutes = self.dailytime.split(' ')[1].strip()  # Get the part before 'm' for minutes
                        self.hoursLength()
                    else:
                        print(
                            f"Failed to get data:fetch_data {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error occured while fetching data: {e}")
            return None
            # self.root.after(300000, self.get_data)

    def hoursLength(self):
            # self.hours = '2h'
            # self.minutes = '22m'
        # Set the text of the labels accordingly
            self.hour_label.config(text=self.hours)
            self.minute_label.config(text=self.minutes)

            # Place the labels initially at arbitrary positions
            self.hour_label.place(x=320, y=47)

            if len(self.hours) == 3 and len(self.minutes)== 3:
                colon_x = 320 + 62  # Adjust for single-digit hour (add 30 pixels to x) diff 62
                minute_x = colon_x + 17  # Adjust minute label (15 pixels after colon) diff 17 
            elif len(self.hours) ==2 and len(self.minutes) == 2:
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
            self.colon_label.place(x=colon_x, y=47)
            self.minute_label.place(x=minute_x, y=47)
                        

    def schedule_update_check(self):
        # Call check_for_update to perform the update check
        self.check_for_update()
        
        # Schedule the next update check after 1 hour
        threading.Timer(3600, self.schedule_update_check).start()

    def check_for_update(self):
        with self.check_for_update_lock:
            api_url = "https://myuniversallanguages.com:9093/api/v1"
            headers = {"Content-Type": "application/json"}

            try:
                response = requests.get(f"{api_url}/timetrack/updatedFile", headers=headers)
                if response.ok:
                    json_data = response.json()
                    data = json_data["data"]
                    self.latest_v = data['version']
                    self.url = data['url']

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
            with open("SSTRACKSetup.exe", 'wb') as new_file:
                new_file.write(response.content)
                self.download = True
            print('SSTRACKSetup.exe downloaded successfully.')

            try:
                os.remove("data.pkl")
            except FileNotFoundError:
                pass

            try:
                os.remove("time_entry_id.pkl")
            except FileNotFoundError:
                pass

            # Restart the main.py script as a new process
            subprocess.Popen(["SSTRACKSetup.exe"])

        else:
            print('Failed to download SSTRACKSetup.exe.')


    def show_loading_message(self):
        self.loading_popup = tk.Toplevel(self.root)
        self.loading_popup.wm_attributes("-topmost", True)
        self.loading_popup.title("Downloading Update")
        tk.Label(self.loading_popup, text="Please wait while we downloading your file...").pack(
            padx=40, pady=40)


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
                if os.path.isfile('trackingStart_list.pkl'):
                    with open("trackingStart_list.pkl", "rb") as f:
                        self.trackingStart_list = pickle.load(f)

                        if len(self.trackingStart_list) > 0:
                            index=0
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

                                if response.ok:
                                    
                                    data = response.json()
                                    print("timer start")
                                    timeEntry = data["data"]["timeEntries"][-1]
                                    timeentryid = timeEntry["_id"]
                                    # delete index from start timer list 
                                    # Remove the first item from the list
                                    self.trackingStart_list.pop(0)
                                    # Reset index to 0
                                    index = 0
                                    
                                    with open("trackingStart_list.pkl", "wb") as f:
                                        pickle.dump(self.trackingStart_list, f)
                                    # Checking if the pickle file exists
                                    
                                    if os.path.isfile("time_entry_id.pkl"):
                                            # Loading the previous time entry ID from the pickle file
                                        with open("time_entry_id.pkl", "rb") as f:
                                            previousTimeEntryId = pickle.load(f)
                                            
                                            # Checking if the previous time entry ID matches the current one
                                        if previousTimeEntryId == uniqueId:
                                                # Writing the current time entry ID to the pickle file
                                            with open("time_entry_id.pkl", "wb") as f:
                                                pickle.dump(timeentryid, f)

                                    
                                    # ======== read screenshots data and replace id =========== #
                                    if os.path.isfile("screenshots_data.pkl"):
                                        with open("screenshots_data.pkl", "rb") as f:
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
                                            with open("screenshots_data.pkl", "wb") as f:
                                                pickle.dump(screenshotsData, f)

                                    # ========= read stop Timer list data and replace id =========== #
                                    if os.path.isfile("trackingStop_list.pkl"):
                                        with open("trackingStop_list.pkl", "rb") as f:
                                            trackerStopList = pickle.load(f)

                                        if trackerStopList:
                                            for stop in trackerStopList:
                                                timeEntry = stop.get('timeEntryId')  
                                                if timeEntry == uniqueId:

                                                    # Replace timeEntry with timeEntryId
                                                    stop['timeEntryId'] = timeentryid

                                            with open("trackingStop_list.pkl", "wb") as f:
                                                pickle.dump(trackerStopList, f)


        except Exception as error:
            print("error", error) 
            return None

# 
# 
# 

    # # Modify the click_play_button method to accept the event argument
    #     def click_play_button(self, event=None):
    #         print("play button")
    #         # Change the icon to indicate the running state
    #         # self.root.iconphoto(True, self.official_icon)
    #         self.root.wm_iconbitmap("images/animatedlogo.ico")
    #         # self.set_icon("images/animatedlogo.ico")
    #         if self.updated:
    #             confirmation = messagebox.askyesno(
    #                 "Confirm Update", "A new version is available. Do you want to update?"
    #             )
    #             if confirmation:
    #                 self.download_new_version()
    #                 if self.download:
    #                     os.system("taskkill /f /im SSTRACK.exe")
    #             else:
    #                 # Destroy the current window
    #                 self.root.destroy()
    #                 # Restart the main.py script as a new process
    #                 subprocess.Popen([self.python_exe, "main.py"])
    #             return    
    #         else:
    #             print("No update required, starting tracking")

    #             if not self.updated:
    #                 self.exact_time = datetime.datetime.now(pytz.UTC)
    #                 playTime = datetime.datetime.now(pytz.UTC)
    #                 self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    #                 if not self.is_timer_running:
    #                     self.is_timer_running = True
    #                     self.total = 0
    #                     threading.Thread(
    #                         target=self.update_time).start()

    #                     # self.play_button.config(state=tk.DISABLED)
    #                     # self.pause_button.config(state=tk.NORMAL)
    #                     # Change play button image to play_icon_grey
    #                     self.canvas.itemconfig(self.play_button, image=self.play_icon_grey)
                    
    #                     # Change pause button image to pause_icon
    #                     self.canvas.itemconfig(self.pause_button, image=self.pause_icon)
    #                     self.canvas.lift(self.pause_button)
    #                     # Unbind the click event for the play button to simulate disabling it
    #                     self.canvas.tag_unbind(self.play_button, '<Button-1>')
    #                     self.canvas.tag_bind(self.pause_button, '<Button-1>', self.click_pause_button)

    #                     # Other logic for starting the timer or performing actions goes here, 40, 10)  # Move pause button up to play position (e.g., x=40, y=5)

    #                     # Continue with the rest of your logic
    #                     self.current_date = datetime.date.today()
    #                     # Run the system tray in a separate thread
    #                     threading.Thread(target=self.run_tray, daemon=True).start()
    #                     # threading.Thread(
    #                     #     target=self.employeeSetting).start()
    #                     threading.Thread(
    #                         target=self.handle_sleep_mode).start()
    #                     threading.Thread(
    #                     target=self.check_activity).start()
    #                     self.total_intervals = 0
    #                     self.active_intervals = 0
    #                     # self.get_data()
    #                     threading.Thread(target=self.stop_Timer).start()
                
    #                 # Check if the file exists before reading from it
    #                     # Check if the file exists
    #                     if os.path.isfile('trackingStart_list.pkl'):
    #                         # Check if the file is empty
    #                         if os.path.getsize('trackingStart_list.pkl') > 0:
    #                             with open("trackingStart_list.pkl", "rb") as f:
    #                                 # Load trackingStart_list from the file
    #                                 self.trackingStart_list = pickle.load(f)
    #                         else:
    #                             # If the file is empty, initialize trackingStart_list as an empty list
    #                             self.trackingStart_list = []
    #                     else:
    #                         # If the file doesn't exist, initialize trackingStart_list as an empty list
    #                         self.trackingStart_list = []

    #                     unique_id = str(uuid.uuid4())
    #                     # unique_id='b9dd81d6-a959-4916-b628-d80223e5cb70'
    #                     playTime = datetime.datetime.now(pytz.UTC)

    #                     trackingstart = {
    #                         "projectId": self.projectId,
    #                         "description": self.description,
    #                         "startTime": playTime,
    #                         "userId": self.user_id,
    #                         "timeEntryId": unique_id
    #                     }

    #                     try:
    #                         # Append tracking start data to the list
    #                         self.trackingStart_list.append(trackingstart)

    #                         # Save the updated list to the file
    #                         with open("trackingStart_list.pkl", "wb") as f:
    #                             pickle.dump(self.trackingStart_list, f)

    #                         # Save the time entry ID to a separate file
    #                         with open("time_entry_id.pkl", "wb") as f:
    #                             pickle.dump(unique_id, f)

    #                         # Start the timer in a separate thread
    #                         threading.Thread(target=self.start_Timer).start()
                        
    #                         print("Tracking start data saved successfully.")
    #                         self.minimize_window()
                        
    #                     except Exception as e:
    #                         print("Failed to save tracking start data:", e)
    #                         return None
    
    
    # Modify the click_play_button method to accept the event argument
    def click_play_button(self, event=None):
        print("Starting click_play_button")
    
        # Update icon (run on the main thread)
        self.root.wm_iconbitmap("/Users/charlie/Downloads/SSTRACKApp/images/animatedlogo.ico")
    
        if self.updated:
            confirmation = messagebox.askyesno(
                "Confirm Update", "A new version is available. Do you want to update?"
            )
            if confirmation:
                self.download_new_version()
                if self.download:
                    os.system("taskkill /f /im SSTRACK.exe")
            else:
                self.root.destroy()
                subprocess.Popen([self.python_exe, "main.py"])
            return  # Return early if updating to avoid further execution
        else:
            print("No update required, starting tracking")

        # Check if timer is already running
        if not self.is_timer_running:
            print("Timer not running, starting now")
            self.is_timer_running = True
            self.total = 0
            threading.Thread(target=self.update_time, daemon=True).start()  # Update time in the background

            # Update button states (running on main thread)
            self.canvas.itemconfig(self.play_button, image=self.play_icon_grey)
            self.canvas.itemconfig(self.pause_button, image=self.pause_icon)
            self.canvas.lift(self.pause_button)
            self.canvas.tag_unbind(self.play_button, '<Button-1>')
            self.canvas.tag_bind(self.pause_button, '<Button-1>', self.click_pause_button)
        
            # Background thread setup for other functions
            print("Starting other background threads")
            threading.Thread(target=self.handle_sleep_mode, daemon=True).start()
            threading.Thread(target=self.check_activity, daemon=True).start()
        
            # Check if the tracking start list exists and load asynchronously
            threading.Thread(target=self.load_tracking_start_list, daemon=True).start()
        
            # Save start tracking data to file
            unique_id = str(uuid.uuid4())
            playTime = datetime.datetime.now(pytz.UTC)
            trackingstart = {
                "projectId": self.projectId,
                "description": self.description,
                "startTime": playTime,
                "userId": self.user_id,
                "timeEntryId": unique_id
            }
            self.save_tracking_start_data(trackingstart, unique_id)  # Save asynchronously

            print("click_play_button completed")

    def load_tracking_start_list(self):
        try:
            if os.path.exists("tracking_start.pkl") and os.path.getsize("tracking_start.pkl") > 0:
                with open("tracking_start.pkl", "rb") as f:
                    self.trackingStart_list = pickle.load(f)
                    print("Tracking start list loaded successfully.")
            else:
                print("tracking_start.pkl is empty or missing. Initializing empty list.")
                self.trackingStart_list = []  # Initialize as an empty list
        except (EOFError, FileNotFoundError, pickle.UnpicklingError) as e:
            print(f"Error loading tracking start list: {e}")
            self.trackingStart_list = []

    def save_tracking_start_data(self, trackingstart, unique_id):
        # Append tracking start data to list and save asynchronously
        print("Saving tracking start data")
        self.trackingStart_list.append(trackingstart)
        with open("trackingStart_list.pkl", "wb") as f:
            pickle.dump(self.trackingStart_list, f)
    
        # Save the time entry ID to a separate file
        with open("time_entry_id.pkl", "wb") as f:
            pickle.dump(unique_id, f)
        print("Tracking start data saved successfully")



# 
# 
# 
    def stop_Timer(self):
        try:
            with self.stop_timer_lock:
                if os.path.isfile('trackingStop_list.pkl'):
                    with open("trackingStop_list.pkl", "rb") as f:
                        self.trackingStop_list = pickle.load(f)

                if self.trackingStop_list:
                    index = 0
                    while index < len(self.trackingStop_list):
                        stoptracking = self.trackingStop_list[index]
                        entryId = stoptracking['timeEntryId']

                        api_url = "https://myuniversallanguages.com:9093/api/v1"

                        headers = {
                            "Authorization": "Bearer " + self.token,
                        }


                        response = requests.patch(
                            f"{api_url}/timetrack/edit/{entryId}",
                            headers=headers,
                            data=stoptracking  # Use the json parameter to send JSON data in the request body
                        )
                        if response.ok:
                            if self.trackingStop_list:
                                del self.trackingStop_list[0]
                                index = 0
                                with open("trackingStop_list.pkl", "wb") as f:
                                    pickle.dump(self.trackingStop_list, f)
                            data = response.json()
                            print("Timer stopped:")
                        else:
                            print("Failed to stop the timer")
                            break

        except Exception as error:
            print(error)
            return None



    def click_pause_button(self, event=None):
        try:
            # Update application icon on the main thread
            print("Pausing the timer...")
            self.root.wm_iconbitmap("/Users/charlie/Downloads/SSTRACKApp/images/pauseico.ico")

            with self.click_pause_button_lock:
                if self.is_timer_running:
                    self.is_timer_running = False

                    # Safely stop the tray icon
                    if hasattr(self, 'icon') and isinstance(self.icon, Icon):
                        self.icon.stop()
                        print("Tray icon removed.")
                    else:
                        print("Tray icon is not initialized or not of type 'Icon'")

                    # Load the time entry ID (handle missing file gracefully)
                    try:
                        with open("time_entry_id.pkl", "rb") as f:
                            timeEntryId = pickle.load(f)
                    except FileNotFoundError:
                        print("time_entry_id.pkl not found. Cannot pause without a previous play.")
                        return

                    # Load or initialize the stop tracking list
                    self.trackingStop_list = []
                    if os.path.isfile('trackingStop_list.pkl'):
                        try:
                            with open("trackingStop_list.pkl", "rb") as f:
                                self.trackingStop_list = pickle.load(f)
                        except (FileNotFoundError, EOFError):
                            print("Failed to load trackingStop_list.pkl. Initializing as empty.")

                    # Determine the stop time
                    current_time = self.exact_time if self.sleep_mood else datetime.datetime.now(pytz.UTC)

                    # Add a new stop entry
                    trackingstop = {"endTime": current_time, "timeEntryId": timeEntryId}
                    self.trackingStop_list.append(trackingstop)

                    # Save the updated stop list asynchronously
                    threading.Thread(target=self.save_tracking_stop_list, args=(self.trackingStop_list,)).start()

                    # Update UI components on the main thread
                    self.update_ui_after_pause()

                    # Reset activity tracking
                    self.total_intervals = 0
                    self.active_intervals = 0

                    # Stop timer in a separate thread
                    threading.Thread(target=self.stop_Timer, daemon=True).start()

        except Exception as e:
            print(f"Error in click_pause_button: {e}")

    
    
    def save_tracking_stop_list(self, stop_list):
        try:
            with open("trackingStop_list.pkl", "wb") as f:
                pickle.dump(stop_list, f)
            print("Tracking stop list saved successfully.")
        except Exception as e:
            print(f"Failed to save tracking stop list: {e}")

    
    
    
    def update_ui_after_pause(self):
        print("Updating UI after pause...")
        # Change play button image back to play_icon
        self.canvas.itemconfig(self.play_button, image=self.play_icon)
    
        # Change pause button image back to pause_icon_grey
        self.canvas.itemconfig(self.pause_button, image=self.pause_icon_grey)
        self.canvas.tag_unbind(self.pause_button, '<Button-1>')
        self.canvas.tag_bind(self.play_button, '<Button-1>', self.click_play_button)

        # Lower the play button to make sure pause is on top
        self.canvas.lift(self.play_button)



    def restartTimer(self):
        try:
            with open("time_entry_id.pkl", "rb") as f:
                timeEntryId = pickle.load(f)

            self.trackingStop_list = []
            if os.path.isfile('trackingStop_list.pkl'):
                with open("trackingStop_list.pkl", "rb") as f:
                    self.trackingStop_list = pickle.load(f)

            if self.sleep_mood:
                current_time = self.exact_time
            else:
                current_time = datetime.datetime.now(pytz.UTC)
            trackingstop = {"endTime": current_time,
                        "timeEntryId": timeEntryId}
            self.trackingStop_list.append(trackingstop)
            with open("trackingStop_list.pkl", "wb") as f:
                pickle.dump(self.trackingStop_list, f)
                    
            
            ############## Timer Start
            unique_id = str(uuid.uuid4())
            # unique_id='b9dd81d6-a959-4916-b628-d80223e5cb70'
            playTime = datetime.datetime.now(pytz.UTC)

            trackingstart = {
                "projectId": self.projectId,
                "description": self.description,
                "startTime": playTime,
                "userId": self.user_id,
                "timeEntryId": unique_id
            }

            # Append tracking start data to the list
            self.trackingStart_list.append(trackingstart)

            # Save the updated list to the file
            with open("trackingStart_list.pkl", "wb") as f:
                pickle.dump(self.trackingStart_list, f)

            # Save the time entry ID to a separate file
            with open("time_entry_id.pkl", "wb") as f:
                pickle.dump(unique_id, f)

            # Start the timer in a separate thread
            threading.Thread(target=self.start_Timer).start()
        except Exception as e:
            print(f"An error occurred: {e}")
            return "N/A"
        
        
    def on_closing(self):
        try:
            if self.is_timer_running:
                confirm = messagebox.askyesno("App Closing", "Are you sure you want to stop the SSTRACK?")
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
            print(f"An error occurred: {e}")
            return "N/A"


    def logout(self):
        """Logout and transition to the login screen."""
        # Stop the timer if running
        if self.is_timer_running:
            self.click_pause_button()
    
        # Clear the stored data
        try:
            os.remove("data.pkl")
        except FileNotFoundError:
            pass
        
        try:
            os.remove("time_entry_id.pkl")
        except FileNotFoundError:
            pass
        
        # Destroy the current Tkinter root window
        self.root.destroy()
    
        # Restart the application by launching main.py
        python_executable = sys.executable  # Get the Python interpreter currently in use
        main_script_path = os.path.abspath("main.py")  # Adjust the path if necessary
    
        # Use subprocess to launch main.py and terminate the current process
        subprocess.Popen([python_executable, main_script_path])
    
        # Forcefully terminate the current process to ensure it's closed
        os._exit(0)
    


    def handle_sleep_mode(self):
        while self.is_timer_running:
            with self.handle_sleep_mode_lock:
                currenttime = datetime.datetime.now(pytz.UTC)
                print(self.exact_time, currenttime)
                three_minutes_ago = currenttime - datetime.timedelta(minutes=3)
                
                # Check if dates are from the same day
                # if self.exact_time.date() == currenttime.date():
                time_difference = currenttime - self.exact_time
                if self.exact_time < three_minutes_ago:
                    self.sleep_mood = True
                    print("Computer is in sleep mode")
                    threading.Thread(target=self.click_pause_button).start()
                    if time_difference.total_seconds() <= 2 * 60 * 60:  # Check if time difference is less than 2 hours
                        tkinter.messagebox.showinfo("SSTRACK Paused", "Your SStrack has been paused due to Sleep Mode.\nPlease start again!")
                    
                # If dates are not from the same day, update exact_time to currenttime
                self.exact_time = currenttime
            time.sleep(1 - time.time() % 1)

#### socket 

    def connect_to_server(self):
        print("Connecting to server...")
        try:
            self.sio.connect('https://myuniversallanguages.com:9093', namespaces=['/'])  # Adjust namespaces as per your server configuration
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return None

        @self.sio.event
        def connect():
            print('Connected to server')

        @self.sio.event
        def message(data):
            print(f"Received from server: {data}")

        @self.sio.event
        def disconnect():
            print('Disconnected from server')
                
        @self.sio.event
        def profile_update(data):
            print(f"Received profile update: {data}")
            if self.user_id == data.get("user", {}).get("_id"):
                self.token=data.get("token")
                with open("data.pkl", "wb") as f:
                    pickle.dump(self.token, f)
                    # Decode the Base64-encoded parts of the token
                    header, payload, signature = self.token.split('.')
                    decoded_payload = base64.urlsafe_b64decode(
                        payload + '==').decode('utf-8')
                    self.user_info = json.loads(decoded_payload)
                    self.name = self.user_info["name"]
                    nameLength = len(self.name)
                    self.company = self.user_info["company"]
                    self.username.config(text=self.name)  # Assuming 'self.username' is the tkinter Label widget
            # Process the received data here
            
            
        @self.sio.event
        def user_setting(data):
            userId = data.get("userId")
            if self.user_id == userId:
                self.settings= data
                self.updateSettings()
                
                
        @self.sio.event
        def users_settings(data):
            for setting in data:
                if self.user_id == setting.get("userId"):
                    self.settings = setting
                    self.updateSettings()
                
        
        @self.sio.event
        def user_archive(data):
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
                        
                                           
        @self.sio.event
        def role_update(data):
            if self.user_id == data.get("user", {}).get("_id"):
                self.token=data.get("token")
                with open("data.pkl", "wb") as f:
                    pickle.dump(self.token, f)
                # self.user_Data()
                # Decode the Base64-encoded parts of the token
                    header, payload, signature = self.token.split('.')
                    decoded_payload = base64.urlsafe_b64decode(
                        payload + '==').decode('utf-8')
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
          
          
    def get_user_startup_path(self):
        # Get the current username
        current_user = os.getlogin()
        
        # Build the paths dynamically based on the current user's name
        startup_folder = os.path.join(
            r"C:\Users", current_user, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        )
        shortcut_source = os.path.join(
            r"C:\Users", current_user, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "SSTRACK.lnk"
        )
        
        return shortcut_source, startup_folder

    def add_shortcut_to_startup(self):
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
            except Exception as e:
                print(f"Failed to add SSTRACK to startup: {e}")
        else:
            print("SSTRACK shortcut not found.")

    def remove_shortcut_from_startup(self):
        # Get the dynamically generated paths
        _, startup_folder = self.get_user_startup_path()
        shortcut_path = os.path.join(startup_folder, "SSTRACK.lnk")
        
        # Check if the shortcut exists and remove it
        if os.path.exists(shortcut_path):
            try:
                os.remove(shortcut_path)
                print("SSTRACK has been removed from startup.")
            except Exception as e:
                print(f"Failed to remove SSTRACK from startup: {e}")
        else:
            print("SSTRACK shortcut not found in startup folder.")

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
        if self.auto_start_var.get():
            self.autoLaunch=True
            with open("autoLaunch.pkl", "wb") as f:
                pickle.dump(self.autoLaunch, f)
            
        # Logic for auto-start
            print("Auto-start enabled")
        else:
        # Logic for auto-start off
            print("Auto-start disabled")
            os.remove("autoLaunch.pkl")
            
            
    def checkAutoLaunch(self):
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
            
            
    def minimize_window(self):
        # Minimize the window
        # self.root.iconify()

                # Once the window is small enough, minimize it
        self.root.iconify()

        
def main():
    root = tk.Tk()
    app = GUIApp(root)
    # Bind the protocol method to the window closing event
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
