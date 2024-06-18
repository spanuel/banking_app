from tkinter import simpledialog,  Toplevel
import ttkbootstrap as ttk
from banking_app.transaction_utils import deposit_funds, withdraw_funds, transfer_funds, generate_statement
from banking_app.utils import get_user_transactions

def create_account_management_screen(root, username):
    frame = ttk.Frame(root)
    frame.pack(pady=20)

    def handle_deposit():
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None:
            deposit_funds(username, amount)

    def handle_withdraw():
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            withdraw_funds(username, amount)

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
            amount = float(amount_entry.get())
            transfer_funds(username, recipient, amount)
            transfer_window.destroy()

        transfer_button = ttk.Button(transfer_window, text="Transfer", command=execute_transfer)
        transfer_button.pack(pady=10)

    def handle_print_statement():
        months = simpledialog.askinteger("Statement", "Enter number of months (1-3):")
        if months in [1, 2, 3]:
            generate_statement(username, months)

    def handle_logout():
        from banking_app.ui_login import create_signin_screen
        frame.destroy()
        create_signin_screen(root)

    ttk.Button(frame, text="Deposit", command=handle_deposit).pack(pady=10)
    ttk.Button(frame, text="Withdraw", command=handle_withdraw).pack(pady=10)
    ttk.Button(frame, text="Transfer", command=handle_transfer).pack(pady=10)
    ttk.Button(frame, text="Print Statement", command=handle_print_statement).pack(pady=10)
    ttk.Button(frame, text="Logout", command=handle_logout).pack(pady=10)
