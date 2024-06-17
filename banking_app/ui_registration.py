import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
from banking_app.utils import center_window, generate_password, validate_id_number, generate_account_number, save_user, log_error
from banking_app.email_utils import send_email

def create_open_account_screen(root, navigate):
    root.geometry("600x650")
    center_window(root, 600, 650)
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True, fill='both')

    label = ttk.Label(frame, text="Open Account", font=('Helvetica', 20, 'bold'))
    label.pack(pady=10)

    fields = ["Full Name", "Date of Birth", "ID Number", "Email Address", "Phone Number", "Username", "Password"]
    entries = {}

    for field in fields:
        frame_inner = ttk.Frame(frame)
        frame_inner.pack(fill='x', pady=5)
        label = ttk.Label(frame_inner, text=field)
        label.pack(side='left', padx=5)
        entry = ttk.Entry(frame_inner)
        entry.pack(side='left', fill='x', expand=True)
        entries[field] = entry

    def generate_password_click():
        password = generate_password()
        entries["Password"].delete(0, tk.END)
        entries["Password"].insert(0, password)

    generate_password_button = ttk.Button(frame, text="Generate Password", style="TButton", command=generate_password_click)
    generate_password_button.pack(pady=10)

    def open_account_click():
        try:
            full_name = entries["Full Name"].get()
            dob = entries["Date of Birth"].get()
            id_number = entries["ID Number"].get()
            email = entries["Email Address"].get()
            phone = entries["Phone Number"].get()
            username = entries["Username"].get()
            password = entries["Password"].get()

            if not validate_id_number(id_number, dob):
                messagebox.showerror("Error", "Invalid ID Number or Date of Birth.")
                return

            account_number = generate_account_number()
            save_user(full_name, dob, id_number, email, phone, username, password, account_number)
            
            account_details = (
                f"Dear {full_name},\n\n"
                f"Thank you for registering with our bank. Your account details are as follows:\n\n"
                f"Account Number: {account_number}\n"
                f"Password: {password}\n\n"
                f"Please keep your account details secure and do not share them with anyone.\n\n"
                f"Best regards,\nYour Bank"
            )
            send_email(email, "Account Created Successfully", account_details)

            messagebox.showinfo("Success", "Account created successfully!")
            navigate(root)
        except Exception as e:
            log_error(str(e), username)
            messagebox.showerror("Error", "An error occurred while creating the account.")

    open_account_button = ttk.Button(frame, text="Open Account", style="TButton", command=open_account_click)
    open_account_button.pack(pady=20)
