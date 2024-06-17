import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from banking_app.utils import center_window
from banking_app.auth import login_user
from banking_app.ui_account_management import create_account_management_screen

def toggle_password(password_entry, toggle_var):
    if toggle_var.get():
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

def create_signin_screen(root, navigate):
    root.geometry("600x400")
    center_window(root, 600, 400)
    for widget in root.winfo_children():
        widget.destroy()
    
    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True, fill='both')
    
    top_frame = ttk.Frame(frame, padding="10", style="primary.TFrame")
    top_frame.pack(fill='x')
    greeting = ttk.Label(top_frame, text="Hello", font=('Helvetica', 30, 'bold'), style="primary.Inverse.TLabel")
    greeting.pack(pady=10)
    
    username_label = ttk.Label(frame, text="Username:")
    username_label.pack(pady=5)
    username_entry = ttk.Entry(frame)
    username_entry.pack(pady=5)
    
    password_label = ttk.Label(frame, text="Password:")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(frame, show="*")
    password_entry.pack(pady=5)
    
    toggle_var = tk.BooleanVar()
    show_password_check = ttk.Checkbutton(frame, text="Show Password", variable=toggle_var, command=lambda: toggle_password(password_entry, toggle_var))
    show_password_check.pack(pady=5)
    
    def on_signin():
        try:
            if login_user(username_entry.get(), password_entry.get()):
                navigate(create_account_management_screen)
            else:
                tk.messagebox.showerror("Login Failed", "Invalid username or password.")
        except Exception as e:
            
            tk.messagebox.showerror("Error", "An error occurred. Please try again.")
    
    signin_button = ttk.Button(frame, text="Sign In", style="TButton", command=on_signin)
    signin_button.pack(pady=10)
    
    forgot_password_button = ttk.Button(frame, text="Forgot Password?", style="TButton")
    forgot_password_button.pack()
