import datetime
from tkinter import messagebox, Toplevel, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap import DateEntry
from banking_app.utils import update_balance, validate_id_number, generate_password, generate_account_number
from banking_app.email_utils import send_email

def create_registration_screen(root, navigate):
    registration_window = Toplevel(root)
    registration_window.title("Register")

    frame = ttk.Frame(registration_window)
    frame.pack(pady=20)

    details = [
        "Full Name", "Date of Birth", "ID Number", "Email Address", "Phone Number", "Username", "Password", "Confirm Password"
    ]

    entries = {}
    for detail in details:
        ttk.Label(frame, text=detail + ":").pack(pady=5)
        if detail == "Date of Birth":
            entry = DateEntry(frame)
        else:
            entry = ttk.Entry(frame)
            entry.insert(0, f"Enter your {detail.lower()}")  # Adding placeholders
            if detail == "Password" or detail == "Confirm Password":
                entry.config(show="*")
        entry.pack(pady=5)
        entries[detail] = entry

    def check_fields_filled():
        if all(entry.get() for entry in entries.values()):
            register_button.config(state='normal')
        else:
            register_button.config(state='disabled')

    for entry in entries.values():
        entry.bind("<KeyRelease>", lambda event: check_fields_filled())



    def handle_registration():
        user_details = {detail: entry.get() for detail, entry in entries.items()}
        if not validate_id_number(user_details["ID Number"], user_details["Date of Birth"]):
            messagebox.showerror("Error", "ID number and date of birth do not match")
            return

        if int(user_details["Date of Birth"][:4]) > (datetime.datetime.now().year - 16):
            messagebox.showerror("Error", "User must be at least 16 years old to register")
            return

        if user_details["Password"] != user_details["Confirm Password"]:
            messagebox.showerror("Error", "Passwords do not match")
            return

        account_number = generate_account_number()
        if len(user_details["Password"]) < 5:
            messagebox.showerror("Error", "Password must be at least 5 characters")
            return

        password = user_details["Password"] if user_details["Password"] else generate_password()
        from banking_app.auth import save_user
        save_user(user_details["Full Name"], user_details["Date of Birth"], user_details["ID Number"], user_details["Email Address"], user_details["Phone Number"], user_details["Username"], password, account_number)

        email_body = f"""Welcome to Tech Junkies Bank\nDear {'Mr' if int(user_details['ID Number'][6:10]) >= 5000 else 'Ms'} {user_details["Full Name"]},
                        \nCongratulations and welcome to Tech Junkies Bank!We're excited to have you as a new customer.
                        \nYour new savings account has been opened successfully. Please find your new account details below:
                        \nAccount name:{user_details['Full Name']}
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
            amount = simpledialog.askfloat("Deposit Amount", "Enter the amount to deposit:")
            if amount:
                # Logic to update account balance with deposited amount
                 update_balance(account_number, amount)
            pass

        registration_window.destroy()
        navigate("ui_account_management")

    check_fields_filled()  # Initial check

    register_button = ttk.Button(frame, text="Register", command=handle_registration)
    register_button.pack(pady=10)
    register_button.config(state='disabled')

    check_fields_filled()  # Initial check

