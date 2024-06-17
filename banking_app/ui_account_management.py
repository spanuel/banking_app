import tkinter as tk
import ttkbootstrap as ttk
from tkinter import simpledialog, messagebox
from ttkbootstrap.constants import *
from banking_app.utils import center_window, get_user_transactions, get_user_details, log_transaction, log_error
from banking_app.email_utils import send_email
from banking_app.transaction_utils import deposit_funds, withdraw_funds, transfer_funds
from datetime import datetime

def create_account_management_screen(root, username, navigate):
    root.geometry("600x400")
    center_window(root, 600, 400)
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True, fill='both')

    label = ttk.Label(frame, text="Account Management", font=('Helvetica', 20, 'bold'))
    label.pack(pady=10)

    def handle_deposit():
        try:
            amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
            if amount:
                deposit_funds(username, amount)
                messagebox.showinfo("Deposit Successful", f"R{amount} deposited successfully.")
        except Exception as e:
            log_error(str(e), username)
            messagebox.showerror("Error", "An error occurred while depositing funds.")

    deposit_button = ttk.Button(frame, text="Deposit", style="TButton", command=handle_deposit)
    deposit_button.pack(pady=5)

    def handle_withdraw():
        try:
            amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
            if amount:
                withdraw_funds(username, amount)
                messagebox.showinfo("Withdrawal Successful", f"R{amount} withdrawn successfully.")
        except Exception as e:
            log_error(str(e), username)
            messagebox.showerror("Error", "An error occurred while withdrawing funds.")

    withdraw_button = ttk.Button(frame, text="Withdraw", style="TButton", command=handle_withdraw)
    withdraw_button.pack(pady=5)

    def handle_transfer():
        try:
            recipient = simpledialog.askstring("Transfer", "Enter recipient account number:")
            amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
            if recipient and amount:
                transfer_funds(username, recipient, amount)
                messagebox.showinfo("Transfer Successful", f"R{amount} transferred successfully.")
        except Exception as e:
            log_error(str(e), username)
            messagebox.showerror("Error", "An error occurred while transferring funds.")

    transfer_button = ttk.Button(frame, text="Transfer", style="TButton", command=handle_transfer)
    transfer_button.pack(pady=5)

    def handle_print_statement():
        try:
            months = simpledialog.askinteger("Statement Duration", "Select number of months (1-3):", minvalue=1, maxvalue=3)
            if months:
                transactions = get_user_transactions(username)
                if transactions:
                    statement_header = (
                        f"Tech Junkies Bank\n\n"
                        f"Bank Statement\n"
                        f"From Date: {transactions[0]['date']}\n"
                        f"To Date: {transactions[-1]['date']}\n"
                        f"Print Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
                        f"Personal Details\n"
                        f"{transactions[0]['full_name']}\n"
                        f"Account Number: {transactions[0]['account_number']}\n\n"
                        f"Transaction Date\tDescription\tMoney In (R)\tMoney Out (R)\tBalance (R)\n"
                    )
                    statement_body = statement_header
                    for transaction in transactions[-months:]:
                        statement_body += (
                            f"{transaction['date']}\t{transaction['description']}\t"
                            f"{transaction['money_in']}\t{transaction['money_out']}\t"
                            f"{transaction['balance']}\n"
                        )
                    email = transactions[0]['email']
                    send_email(email, "Your Bank Statement", statement_body)
                    messagebox.showinfo("Statement Sent", "Your bank statement has been sent to your email.")
                else:
                    messagebox.showerror("Error", "Failed to generate bank statement.")
        except Exception as e:
            log_error(str(e), username)
            messagebox.showerror("Error", "An error occurred while sending the statement.")

    print_statement_button = ttk.Button(frame, text="Print Statement", style="TButton", command=handle_print_statement)
    print_statement_button.pack(pady=5)

    def handle_logout():
        navigate(root)

    logout_button = ttk.Button(frame, text="Logout", style="TButton", command=handle_logout)
    logout_button.pack(pady=20)
