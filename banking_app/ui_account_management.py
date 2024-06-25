from tkinter import simpledialog, Toplevel, messagebox
import ttkbootstrap as ttk
from banking_app.transaction_utils import deposit_funds, withdraw_funds, transfer_funds, generate_statement, get_balance, update_balance
from banking_app.utils import account_exists, add_beneficiary_to_username_list, create_beneficiary_file, get_account_number, load_beneficiaries, user_exists

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
                # Update balance display
                balance_label.config(text=f"Balance: R {get_balance(username)}")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")

    # Doing withdrawal transactions
    def handle_withdraw():
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            try:
                withdraw_funds(username, amount)
                update_balance(username, get_balance(username) - amount)
                # Update balance display
                balance_label.config(text=f"Balance: R {get_balance(username)}")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")

    # Doing transfer transactions
    def handle_transfer():
        beneficiaries = load_beneficiaries(username)
        if not beneficiaries:
            # Create the file if it does not exist
            create_beneficiary_file(username)  
            beneficiaries = load_beneficiaries(username)

        transfer_window = Toplevel(root)
        transfer_window.title("Transfer")

        balance = get_balance(username)
        ttk.Label(transfer_window, text=f"Balance: R {balance}").pack(pady=5)

        quick_pay_frame = ttk.Frame(transfer_window)
        quick_pay_frame.pack(pady=5)

        ttk.Label(quick_pay_frame, text="Quick Pay").pack(side="left")
        quick_pay_button = ttk.Button(quick_pay_frame, text="Pay with Cell Number", command=lambda: quick_pay_transfer(transfer_window, username))
        quick_pay_button.pack(side="left", padx=10)

        add_beneficiary_frame = ttk.Frame(transfer_window)
        add_beneficiary_frame.pack(pady=5)

        ttk.Label(add_beneficiary_frame, text="Add Beneficiary").pack(side="left")
        add_beneficiary_button = ttk.Button(add_beneficiary_frame, text="Add", command=lambda: add_beneficiary(transfer_window, username, beneficiary_list))
        add_beneficiary_button.pack(side="left", padx=10)

        beneficiary_list_frame = ttk.Frame(transfer_window)
        beneficiary_list_frame.pack(pady=5)

        beneficiary_list = ttk.Treeview(beneficiary_list_frame, columns=("full_name",), show="headings")
        beneficiary_list.heading("full_name", text="Full Name")
        beneficiary_list.pack(side="left", fill="both", expand=True)

        # Load existing beneficiaries
        beneficiaries = load_beneficiaries(username)
        for beneficiary in beneficiaries:
            beneficiary_list.insert("", "end", values=(beneficiary["Full Name"],))

        def select_beneficiary():
            selected_beneficiary = beneficiary_list.item(beneficiary_list.selection()[0], "values")[0]
            transfer_to_beneficiary(transfer_window, username, selected_beneficiary)

        select_button = ttk.Button(beneficiary_list_frame, text="Select", command=select_beneficiary)
        select_button.pack(side="right", padx=10)

    def quick_pay_transfer(transfer_window, username):
        quick_pay_window = Toplevel(transfer_window)
        quick_pay_window.title("Quick Pay")

        ttk.Label(quick_pay_window, text="Full Name:").pack(pady=5)
        full_name_entry = ttk.Entry(quick_pay_window)
        full_name_entry.pack(pady=5)

        ttk.Label(quick_pay_window, text="Phone Number:").pack(pady=5)
        cell_number_entry = ttk.Entry(quick_pay_window)
        cell_number_entry.pack(pady=5)

        ttk.Label(quick_pay_window, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(quick_pay_window)
        amount_entry.pack(pady=5)

        def execute_quick_pay():
            full_name = full_name_entry.get()
            cell_number = cell_number_entry.get()
            amount = float(amount_entry.get())
            # Check if user exists
            if user_exists(cell_number):
                # Make quick pay transfer
                transfer_funds(username, cell_number, amount, immediate=True)
                quick_pay_window.destroy()
            else:
                messagebox.showerror("Error", "User does not exist, are you sure they have an account")

        quick_pay_button = ttk.Button(quick_pay_window, text="Pay", command=execute_quick_pay)
        quick_pay_button.pack(pady=10)

    def add_beneficiary(transfer_window, username, beneficiary_list):
        add_beneficiary_window = Toplevel(transfer_window)
        add_beneficiary_window.title("Add Beneficiary")

        ttk.Label(add_beneficiary_window, text="Full Name:").pack(pady=5)
        full_name_entry = ttk.Entry(add_beneficiary_window)
        full_name_entry.pack(pady=5)

        ttk.Label(add_beneficiary_window, text="Account Number:").pack(pady=5)
        account_number_entry = ttk.Entry(add_beneficiary_window)
        account_number_entry.pack(pady=5)

        def add_beneficiary_to_list():
            full_name = full_name_entry.get()
            account_number = account_number_entry.get()
    
            if full_name and account_number:
                # Check if account exists
                if account_exists(account_number):
                    # Add beneficiary to list
                    add_beneficiary_to_username_list(username, full_name, account_number)
                    add_beneficiary_window.destroy()

                    # Update the Treeview widget
                    beneficiary_list.delete(*beneficiary_list.get_children())
                    updated_beneficiaries = load_beneficiaries(username)
                    for beneficiary in updated_beneficiaries:
                        beneficiary_list.insert("", "end", values=(beneficiary["Full Name"],))
                        
                    messagebox.showinfo("Success", "Beneficiary added successfully")
                else:
                    messagebox.showerror("Error", "Account does not exist")
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        add_button = ttk.Button(add_beneficiary_window, text="Add", command=add_beneficiary_to_list)
        add_button.pack(pady=10)

    def transfer_to_beneficiary(transfer_window, username, beneficiary_full_name):
        transfer_window.destroy()
        transfer_window = Toplevel(transfer_window)
        transfer_window.title("Transfer to Beneficiary")

        ttk.Label(transfer_window, text=f"Full Name: {beneficiary_full_name}").pack(pady=5)
        ttk.Label(transfer_window, text="Account Number:").pack(pady=5)
        account_number_label = ttk.Label(transfer_window, text=get_account_number(beneficiary_full_name))
        account_number_label.pack(pady=5)

        ttk.Label(transfer_window, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(transfer_window)
        amount_entry.pack(pady=5)

        def execute_transfer():
            amount = float(amount_entry.get())
            # Make transfer
            transfer_funds(username, beneficiary_full_name, amount)
            transfer_window.destroy()

        transfer_button = ttk.Button(transfer_window, text="Transfer", command=execute_transfer)
        transfer_button.pack(pady=10)

        immediate_payment_frame = ttk.Frame(transfer_window)
        immediate_payment_frame.pack(pady=5)

        ttk.Label(immediate_payment_frame, text="Immediate Payment").pack(side="left")
        immediate_payment_button = ttk.Button(immediate_payment_frame, text="Pay", command=lambda: execute_transfer())
        immediate_payment_button.pack(side="left", padx=10)

    deposit_button = ttk.Button(frame, text="Deposit", command=handle_deposit)
    deposit_button.pack(pady=5)

    withdraw_button = ttk.Button(frame, text="Withdraw", command=handle_withdraw)
    withdraw_button.pack(pady=5)

    transfer_button = ttk.Button(frame, text="Transfer", command=handle_transfer)
    transfer_button.pack(pady=5)

    statement_button = ttk.Button(frame, text="Generate Statement", command=lambda: generate_statement(username))
    statement_button.pack(pady=5)

    logout_button = ttk.Button(frame, text="Logout", command=create_signin_screen)
    logout_button.pack(pady=5)

