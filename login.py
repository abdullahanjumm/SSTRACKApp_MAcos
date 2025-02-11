import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pickle
import webbrowser
import os
import sys
from customized import GUIApp
import tempfile


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LOGIN")
        self.root.geometry("700x500")
        self.root.configure(bg="#0E4772")
        self.root.resizable(False, False)

        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (700 / 2))
        y_coordinate = int((screen_height / 2) - (500 / 2))
        self.root.geometry(f"700x500+{x_coordinate}+{y_coordinate}")

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        # Load icons
        # self.play_icon = PhotoImage(file='images/sstracklogo.png')
        self.play_icon = PhotoImage(file=os.path.join(base_path, 'images', 'sstracklogo.png'))
        # self.email_icon = PhotoImage(file='images/email.png')
        self.email_icon = PhotoImage(file=os.path.join(base_path, 'images', 'email.png'))
        # self.password_icon = PhotoImage(file='images/password.png')
        self.password_icon = PhotoImage(file=os.path.join(base_path, 'images', 'password.png'))
        # official_icon = self.resize_image('images/logopause.ico', 100, 100)
        official_icon = self.resize_image(LoginApp.resource_path('images/logopause.ico'), 100, 100)

        self.root.iconphoto(True, official_icon)

        # Logo Frame
        frame1 = Frame(self.root, width=350, height=50, bg="#0E4772")
        frame1.place(x=20, y=15)
        play_label = Label(frame1, image=self.play_icon, bg="#0E4772")
        play_label.place(x=0, y=-4)

        # Main Frame for login
        frame = Frame(self.root, width=350, height=450, bg="#0E4772")
        frame.place(x=172, y=70)

        # Heading
        heading = Label(frame, text="Access your Account", fg="#FFFFFF", bg="#0E4772", font=('Arial', 20, 'bold'))
        heading.place(x=50, y=20)

        # Email Entry
        email_label = Label(frame, image=self.email_icon, bg="#0E4772")
        email_label.place(x=20, y=70)
        self.email = Entry(frame, width=25, fg="#FFFFFF", border=0, bg="#0E4772", font=('Arial', 12), highlightthickness=0)
        self.email.insert(0, 'Enter your email')
        self.email.bind("<FocusIn>", self.clear_placeholder)
        self.email.bind("<FocusOut>", self.add_placeholder)
        self.email.place(x=55, y=75)
        Frame(frame, width=295, height=2, bg='#FFFFFF').place(x=20, y=100)

        # Password Entry
        password_label = Label(frame, image=self.password_icon, bg="#0E4772")
        password_label.place(x=20, y=120)
        self.Password = Entry(frame, width=25, fg="#FFFFFF", border=0, bg="#0E4772", font=('Arial', 12), show="*", highlightthickness=0)
        self.Password.insert(0, 'Enter your password')
        self.Password.bind("<FocusIn>", self.clear_placeholder_password)
        self.Password.bind("<FocusOut>", self.add_placeholder_password)
        self.Password.place(x=55, y=125)
        Frame(frame, width=295, height=2, bg='#FFFFFF').place(x=20, y=150)

        # Check for data in pickle file
        self.check_and_load_data()


        # Forget Password Label acting as a button
        forgetpassword = Label(frame, text="Forget Password", fg="#7ACB59", bg="#0E4772", cursor="hand2",
                       font=('Arial', 10, 'bold'))
        forgetpassword.place(x=190, y=170)
        forgetpassword.bind("<Button-1>", lambda e: self.open_forget_password())
        
        # Login Label acting as a button
        login_button = Label(frame, text="Login", fg="#FFFFFF", bg="#3CB371", cursor="hand2",
                     font=('Arial', 12, 'bold'), width=36, pady=7)
        login_button.place(x=20, y=210)
        login_button.bind("<Button-1>", lambda e: self.perform_login())

        # Google Sign-Up Button
        google_signup = Label(frame, text="Sign up with Google", fg="#FFFFFF", bg="#DB4437", cursor="hand2",
                     font=('Arial', 12, 'bold'), width=36, pady=7)
        google_signup.place(x=20, y=260)
        google_signup.bind("<Button-1>", lambda e: self.signup_with_google())
        
        # Microsoft Sign-Up Button
        microsoft_signup = Label(frame, text="Sign up with Microsoft", fg="#FFFFFF", bg="#0078D4", cursor="hand2",
                     font=('Arial', 12, 'bold'), width=36, pady=7)
                                
        microsoft_signup.place(x=20, y=310)
        microsoft_signup.bind("<Button-1>", lambda e: self.signup_with_microsoft())

        # Sign Up Label
        label = Label(frame, text="Don't have an account?", fg="#FFFFFF", bg="#0E4772", font=('Arial', 10))
        label.place(x=70, y=360)

        # Traditional Sign Up Button
        signup = Label(frame, text="Sign up", fg="#7ACB59", bg="#0E4772", cursor="hand2",
                        font=('Arial', 10, 'bold'))
        signup.place(x=180, y=360)

        # Bind Enter key to login function
        self.root.bind("<Return>", self.perform_login)
    
    
    @staticmethod
    def get_app_dir():
        """Get the directory where the executable is running."""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)  # Running as an executable
        return os.path.dirname(os.path.abspath(__file__))  # Running as a script
    def resource_path(relative_path):
        """ Get absolute path to resource, works for development and PyInstaller """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # PyInstaller bundle path
        else:
            base_path = os.path.abspath(".")  # Normal script path

        path = os.path.join(base_path, relative_path)

        # Debugging: Print the path to check if it exists
        print(f"Loading file: {path}")

        if not os.path.exists(path):
            print(f"Error: {path} not found!")

        return path

    def resize_image(self, file_path, width, height):
        image = Image.open(file_path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def signup_with_google(self):
        url = "https://myuniversallanguages.com:9093/api/v1/auth/google"
        webbrowser.open(url, new=2)

    def signup_with_microsoft(self):
        url = "https://myuniversallanguages.com:9093/api/v1/auth/microsoft"
        webbrowser.open(url, new=2)

    def clear_placeholder(self, event):
        if self.email.get() == 'Enter your email':
            self.email.delete(0, 'end')
            self.email.config(fg="#FFFFFF")

    def add_placeholder(self, event):
        if self.email.get() == '':
            self.email.insert(0, 'Enter your email')
            self.email.config(fg="#CCCCCC")

    def clear_placeholder_password(self, event):
        if self.Password.get() == 'Enter your password':
            self.Password.delete(0, 'end')
            self.Password.config(fg="#FFFFFF", show="*")

    def add_placeholder_password(self, event):
        if self.Password.get() == '':
            self.Password.config(fg="#CCCCCC", show="")
            self.Password.insert(0, 'Enter your password')

    def check_and_load_data(self):
        data_path = os.path.join(LoginApp.get_app_dir(), "new_data.pkl")
        if os.path.exists(data_path):
            try:
                with open(data_path, "rb") as file:
                    data = pickle.load(file)
                    print(f"Email: {data.get('email', 'No email found')}")
                    print(f"Password: {data.get('password', 'No password found')}")
            except Exception as e:
                print(f"Error loading data: {e}")

    def open_forget_password(self):
        messagebox.showinfo("Forgot Password", "Forgot password functionality is under construction.")

    def open_signup(self):
        messagebox.showinfo("Sign Up", "Sign up functionality is under construction.")


    def perform_login(self, event=None):
     email_value = self.email.get()
     password = self.Password.get()

     api_url = "https://myuniversallanguages.com:9093/api/v1/signin"
     model = {
        "email": email_value,
        "password": password
     }

     headers = {
        "Content-Type": "application/json",
     }

     try:
        response = requests.post(api_url, json=model, headers=headers)
        data = response.json()
        if "message" in data:
            # If there's an error message returned from the API
            messagebox.showerror("Error", data["message"])
        else:
            # Login successful
            data_file = os.path.join(LoginApp.get_app_dir(), "data.pkl")
            new_data_file = os.path.join(LoginApp.get_app_dir(), "new_data.pkl")
            token = data["token"]
            with open(data_file, "wb") as f:
                pickle.dump(token, f)
                # Save email and password to new_data.pkl
            login_data = {"email": email_value, "password": password}
            with open(new_data_file, "wb") as f:
                pickle.dump(login_data, f)
            self.root.destroy()
            second_page = GUIApp(Tk())
            second_page.root.mainloop()

     except requests.exceptions.RequestException as e:
        # Handle connection or request error
        messagebox.showerror("Error", "An error occurred while connecting to the server")


# Create the Tkinter window
def main():
    root = Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
