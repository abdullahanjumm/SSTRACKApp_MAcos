import pyautogui
import threading
import time
import Quartz

class ActivityMonitor:
    def __init__(self):
        self.activity_flag = False
        self.last_mouse_position = pyautogui.position()
        self.stop_flag = False
        self.keyboard_thread_started = False
        self.lock = threading.Lock()  # Lock for thread safety

    def check_mouse_activity(self):
        """Check for mouse movement."""
        try:
            current_mouse_position = pyautogui.position()
            if current_mouse_position != self.last_mouse_position:
                with self.lock:
                    self.activity_flag = True
                print("Mouse activity detected.")
                self.last_mouse_position = current_mouse_position
            else:
                print("No mouse activity detected.")
        except Exception as e:
            print(f"Error in mouse activity detection: {e}")

    def on_key_press(self, proxy, type, event, refcon):
        """Callback for key press events."""
        try:
            keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
            # print(f"Key pressed. Keycode: {keycode}")
            with self.lock:
                self.activity_flag = True  # Set activity flag to True when key is pressed
            # print(f"Activity flag set to: {self.activity_flag}")     
        except Exception as e:
            print(f"Error in key press callback: {e}")
        return event

    def monitor_keyboard(self):
        """Monitor keyboard activity using Quartz."""
        try:
            event_tap = Quartz.CGEventTapCreate(
                Quartz.kCGSessionEventTap,
                Quartz.kCGHeadInsertEventTap,
                Quartz.kCGEventTapOptionDefault,
                Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown),
                self.on_key_press,
                None
            )

            if not event_tap:
                print("Failed to create event tap. Check permissions.")
                return

            # Create a run loop source
            run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, event_tap, 0)
            Quartz.CFRunLoopAddSource(Quartz.CFRunLoopGetCurrent(), run_loop_source, Quartz.kCFRunLoopCommonModes)

            # Enable the event tap
            Quartz.CGEventTapEnable(event_tap, True)

            print("Starting keyboard monitoring...")
            while not self.stop_flag:
                Quartz.CFRunLoopRunInMode(Quartz.kCFRunLoopDefaultMode, 0.1, True)
        except Exception as e:
            print(f"Error in keyboard monitoring: {e}")

    def start_keyboard_monitoring(self):
        """Start keyboard monitoring in a separate thread."""
        if not self.keyboard_thread_started:
            keyboard_thread = threading.Thread(target=self.monitor_keyboard, daemon=True)
            keyboard_thread.start()
            self.keyboard_thread_started = True
            print("Keyboard monitoring thread started.")

    def start_monitoring(self):
        """Start monitoring mouse and keyboard activity."""
        self.start_keyboard_monitoring()

        try:
            last_activity_time = time.time()  # Track last activity time

            while not self.stop_flag:
                # Check for mouse and keyboard activity
                self.check_mouse_activity()
                self.check_keyboard_activity()

                # Log current activity flag state
                with self.lock:
                    print(f"Activity flag after checks activity monitor: {self.activity_flag}")

                # If activity was detected, update the time
                if self.activity_flag:
                    last_activity_time = time.time()

                # Reset the flag if no activity for a certain period (e.g., 10 seconds)
                if time.time() - last_activity_time > 10:
                    with self.lock:
                        self.activity_flag = False
                    print(f"Activity flag reset to: {self.activity_flag}")

                time.sleep(1)  # Shorter sleep interval to ensure timely activity flag reset
        except KeyboardInterrupt:
            self.stop_flag = True
            print("Monitoring stopped.")

    def check_keyboard_activity(self):
        """Ensure keyboard monitoring thread is running."""
        if not self.keyboard_thread_started:
            self.start_keyboard_monitoring()
        print("Keyboard activity checked (thread running).")

# Running the monitoring system
if __name__ == "__main__":
    monitor = ActivityMonitor()
    monitor.start_monitoring()
