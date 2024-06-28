import datetime
import ttkbootstrap as ttk
from ttkbootstrap import DateEntry
from tkinter import BooleanVar, messagebox, simpledialog
from ttkbootstrap.constants import *
from banking_app.utils import center_window, generate_random_password, update_balance, validate_email, validate_id_number, generate_account_number, validate_phone_number
from banking_app.email_utils import send_email
from banking_app.auth import login_user
from banking_app.ui_account_management import create_account_management_screen
from banking_app.navigator import navigate_to

def toggle_password(password_entry, toggle_var):
    if toggle_var.get():
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

# Login user interface
def create_signin_screen(root, navigate):
    root.geometry("600x500")
    center_window(root, 600, 500)
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
    
    toggle_var = BooleanVar()
    show_password_check = ttk.Checkbutton(frame, text="Show Password", variable=toggle_var, command=lambda: toggle_password(password_entry, toggle_var))
    show_password_check.pack(pady=5)
    
    def on_signin():
        try:
            if login_user(username_entry.get(), password_entry.get()):
                navigate_to(create_account_management_screen, root, username_entry.get(), navigate_to, create_signin_screen)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred. Please try again.")
    
    signin_button = ttk.Button(frame, text="Sign In", style="TButton", command=on_signin)
    signin_button.pack(pady=10)
    
    forgot_password_button = ttk.Button(frame, text="Forgot Password?", style="TButton")
    forgot_password_button.pack()

# Registration user interface
def create_registration_screen(root, navigate,create_signin_screen):
    root.geometry("600x800")
    center_window(root, 600, 800)
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Register")

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True,fill='both')

    details = [
        "Full Name", "Date of Birth", "ID Number", "Email Address", "Phone Number", "Username", "Password"
    ]

    entries = {}
    for detail in details:
        ttk.Label(frame, text=detail + ":").pack(pady=5)
        if detail == "Date of Birth":
            entry = DateEntry(frame)
        else:
            entry = ttk.Entry(frame)
            entry.insert(0, f"Enter your {detail.lower()}")  # Adding placeholders
            if detail == "Password":
                entry.config(show="*", state='readonly')
        entry.pack(pady=5)
        entries[detail] = entry

    def generate_password():
        password = generate_random_password()
        entries["Password"].config(state='normal')
        entries["Password"].delete(0, 'end')
        entries["Password"].insert(0, password)
        entries["Password"].config(state='readonly')

    generate_password_button = ttk.Button(frame, text="Generate Password", command=generate_password)
    generate_password_button.pack(pady=5)

    def handle_registration(root,user_details):
        registration_label = ttk.Label(root, text="Registering...", font=('Helvetica', 20, 'bold'))
        registration_label.pack(pady=10)
        root.update_idletasks()  # Update the GUI to show the label

        try:
            user_details = {}
            for detail, entry in entries.items():
                if isinstance(entry, DateEntry):
                    user_details[detail] = entry.entry.get()
                else:
                    user_details[detail] = entry.get()

            #Error handling and input validation
            try:
                if not user_details["Full Name"]:
                    messagebox.showerror("Error", "Full name is required")
                    return
                
                if int(user_details["Date of Birth"].split('/')[-1])> (datetime.datetime.now().year - 16):
                    messagebox.showerror("Error", "User must be at least 16 years old to register")
                    return

                if not validate_id_number(user_details["ID Number"], user_details["Date of Birth"]):
                    messagebox.showerror("Error", "ID number and date of birth do not match")
                    return
                
                if not user_details["Email Address"] or not validate_email(user_details["Email Address"]):
                    messagebox.showerror("Error", "Invalid email address")
                    return

                if not user_details["Phone Number"] or not validate_phone_number(user_details["Phone Number"]):
                    messagebox.showerror("Error", "Invalid phone number")
                    return

                if not user_details["Username"]:
                    messagebox.showerror("Error", "Username is required")
                    return
               
                account_number = generate_account_number()
                password = user_details["Password"]
                from banking_app.auth import save_user
                save_user(user_details["Full Name"], user_details["Date of Birth"], user_details["ID Number"], user_details["Email Address"], user_details["Phone Number"], user_details["Username"], password, account_number)

                email_body = f"""Welcome to Tech Junkies Bank\n\nDear {'Mr' if int(user_details['ID Number'][6:10]) >= 5000 else 'Ms'} {user_details["Full Name"]},
                            \nCongratulations and welcome to Tech Junkies Bank! We're excited to have you as a new customer.
                            \nYour new savings account has been opened successfully. Please find your new account details below:
                            \nAccount name: {user_details['Full Name']}
                            \nAccount Number: {account_number}
                            \nPassword: {password}
                            \nYou can use this account number to set up direct deposit, transfer funds, make payments, and more.
                            \nThank you for choosing Tech Junkies Bank. We look forward to serving your financial needs. 
                            \nPlease let us know if you have any other questions.
                            \n\nSincerely,
                            \nThe Tech Junkies Bank Team
                        """
                send_email(user_details["Email Address"], "Welcome to Our Bank", email_body)
                messagebox.showinfo("Success", "Registration successful! Your bank account details have been sent to your email.")
        
                response = messagebox.askyesno("Deposit Funds", "Would you like to deposit funds to your account?")
                if response:
                    while True:
                        password = simpledialog.askstring("Enter Password", "Enter your password", parent=root, show="*")
                        if password == user_details["Password"]:
                            amount = simpledialog.askfloat("Enter Amount", "Enter the amount to deposit", parent=root)
                            if amount:
                                from banking_app.ui_account_management import create_account_management_screen
                                # Logic to update account balance with deposited amount
                                update_balance(user_details["Username"], amount)
                                messagebox.showinfo("Success", f"Deposit of R {amount} successful!")
                                # Navigate to the account management screen
                                navigate_to(create_account_management_screen, root, user_details["Username"], navigate, create_signin_screen)
                                break
                            else:
                                messagebox.showerror("Error", "Invalid amount")
                        else:
                            messagebox.showerror("Error", "Incorrect password. Please try again.")
                else:
                    # Navigate to the signin screen
                    navigate_to(create_signin_screen, root, navigate)

            except Exception as e:
                messagebox.showerror("Error", str(e))
            
        except Exception as e:
            registration_label.config(text="Error: " + str(e))
            root.update_idletasks()  # Update the GUI to show the error message


    register_button = ttk.Button(frame, text="Register", command=lambda: handle_registration(root, {}), style="TButton")
    register_button.pack(pady=10)
    register_button.config(state='disabled')

    def check_fields_filled():
        for detail, entry in entries.items():
            if isinstance(entry, DateEntry):
                if not entry.entry.get():
                    register_button.config(state='disabled')
                    return
            else:
                if not entry.get() or entry.get() == f"Enter your {detail.lower()}":
                    register_button.config(state='disabled')
                    return
        register_button.config(state='normal')
    
    for entry in entries.values():
        if isinstance(entry, DateEntry):
            entry.bind("<<DateEntrySelected>>", lambda event: check_fields_filled())
        else:
            entry.bind("<KeyRelease>", lambda event: check_fields_filled())
            entry.bind("<FocusIn>", lambda event, e=entry: e.delete(0, 'end') if e.get().startswith("Enter your") else None)

    check_fields_filled()  # Initial check
