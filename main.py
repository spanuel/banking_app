import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from banking_app.utils import center_window
from banking_app.navigator import navigate_to
from banking_app.screens import create_signin_screen, create_registration_screen
import logging

# Setting up logging to a file
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

# Function to handle errors and log them
def handle_error(error_msg):
    logging.error(error_msg)
    # You can add more error handling logic here

# Main user interface
def create_main_screen(root, navigate, create_signin_screen, create_registration_screen):
    try:
        root.geometry("600x300")
        center_window(root, 600, 300)
        
        # Clear existing widgets
        for widget in root.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(root, padding="20")
        frame.pack(expand=True, fill='both')
        
        top_frame = ttk.Frame(frame, padding="10", style="primary.TFrame")
        top_frame.pack(fill='x')
        greeting = ttk.Label(top_frame, text="Hello", font=('Helvetica', 30, 'bold'), style="primary.Inverse.TLabel")
        greeting.pack(pady=10)
        
        question = ttk.Label(frame, text="What would you like to do?", font=('Helvetica', 14))
        question.pack(pady=10)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        # Sign In button
        signin_button = ttk.Button(button_frame, text="Sign In", command=lambda: navigate(create_signin_screen, root, navigate_to), style="TButton")
        signin_button.pack(side=LEFT, padx=10)
        
        # Open an Account button
        open_account_button = ttk.Button(button_frame, text="Open an Account", command=lambda: navigate(create_registration_screen, root, navigate_to, create_signin_screen), style="TButton")
        open_account_button.pack(side=LEFT, padx=10)
    
    except tk.TclError as tcl_error:
        handle_error(f"A TclError occurred in create_main_screen: {str(tcl_error)}")
    except Exception as e:
        handle_error(f"An error occurred in create_main_screen: {str(e)}")

# Main Application Window
root = ttk.Window(themename="darkly")
root.title("Bank App")

try:
    create_main_screen(root, navigate_to, create_signin_screen, create_registration_screen)
    root.mainloop()
except tk.TclError as tcl_error:
    handle_error(f"A TclError occurred in main application: {str(tcl_error)}")
except Exception as e:
    handle_error(f"An error occurred in main application: {str(e)}")