from tkinter import simpledialog,  Toplevel, messagebox
import ttkbootstrap as ttk
from banking_app.transaction_utils import deposit_funds, withdraw_funds, transfer_funds, generate_statement,get_balance,update_balance

# Acoount management user interface
def create_account_management_screen(root, username, navigate, create_signin_screen):
    root.title("Account Management") 
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True, fill='both')

    top_frame = ttk.Frame(frame, padding="10", style="primary.TFrame")
    top_frame.pack(fill='x')

    greeting = ttk.Label(top_frame, text=f"Hello {username}", font=('Helvetica', 30, 'bold'), style="primary.Inverse.TLabel")
    greeting.pack(pady=10)

    # Get the user's balance from the file BankData
    balance = get_balance(username) 

    balance_label = ttk.Label(frame, text=f"Balance: R {balance}", font=('Helvetica', 20, 'bold'))
    balance_label.pack(pady=10)

    # Doing deposit transactions
    def handle_deposit():
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None:
            try:
                deposit_funds(username, amount)
                update_balance(username, get_balance(username) + amount)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")

    # Doing withdrawal transactions
    def handle_withdraw():
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            try:
                withdraw_funds(username, amount)
                update_balance(username, get_balance(username) + amount)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")

    # Doing transfer transactions
    def handle_transfer():
        transfer_window = Toplevel(root)
        transfer_window.title("Transfer")

        ttk.Label(transfer_window, text="Recipient Username:").pack(pady=5)
        recipient_entry = ttk.Entry(transfer_window)
        recipient_entry.pack(pady=5)

        ttk.Label(transfer_window, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(transfer_window)
        amount_entry.pack(pady=5)

        def execute_transfer():
            recipient = recipient_entry.get()
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                else:
                    transfer_funds(username, recipient, amount)
                    transfer_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")

        transfer_button = ttk.Button(transfer_window, text="Transfer", command=execute_transfer)
        transfer_button.pack(pady=10)

    # Printing statement
    def handle_print_statement():
        months = simpledialog.askinteger("Statement", "Enter number of months (1-3):")
        if months in [1, 2, 3]:
            generate_statement(username, months)
        else:
            messagebox.showinfo("Error", "Invalid input. Maximum number of months allowed is 3.")

    # logout
    def handle_logout():
        navigate(lambda root, navigate: create_signin_screen(root, navigate), root, navigate)
        frame.destroy()
        frame.destroy()

    ttk.Button(frame, text="Deposit", command=handle_deposit).pack(pady=10)
    ttk.Button(frame, text="Withdraw", command=handle_withdraw).pack(pady=10)
    ttk.Button(frame, text="Transfer", command=handle_transfer).pack(pady=10)
    ttk.Button(frame, text="Print Statement", command=handle_print_statement).pack(pady=10)
    ttk.Button(frame, text="Logout", command=handle_logout).pack(pady=10)
