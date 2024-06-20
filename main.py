import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from banking_app.utils import center_window
from banking_app.navigator import navigate_to
from banking_app.screens import create_signin_screen, create_registration_screen

def create_main_screen(root, navigate,create_signin_screen, create_registration_screen):
    root.geometry("600x300")
    center_window(root, 600, 300)
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
    
    signin_button = ttk.Button(button_frame, text="Sign In", command=lambda: navigate(create_signin_screen, root), style="TButton")
    signin_button.pack(side=LEFT, padx=10)
    
    open_account_button = ttk.Button(button_frame, text="Open an Account", command=lambda: navigate(create_registration_screen, root), style="TButton")
    open_account_button.pack(side=LEFT, padx=10)

    

# Main Application Window
root = ttk.Window(themename="darkly")
root.title("Bank App")

create_main_screen(root, navigate_to, create_signin_screen, create_registration_screen)
root.mainloop()
