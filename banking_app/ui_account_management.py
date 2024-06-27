from calendar import month_name
from tkinter import BooleanVar, simpledialog, Toplevel, messagebox
import ttkbootstrap as ttk
from banking_app.transaction_utils import deposit_funds, withdraw_funds, transfer_funds, generate_statement, get_balance
from banking_app.utils import account_exists, add_beneficiary_to_username_list, center_window, load_beneficiaries, log_transaction, user_exists

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
    def update_balance_display():
        balance = get_balance(username)  # Fetch balance from data file
        balance_label.config(text=f"Balance: R {balance}") 

    # define balance_label before calling update_balance_display
    balance = get_balance(username)  # Fetch initial balance
    balance_label = ttk.Label(frame, text=f"Balance: R {balance}", font=('Helvetica', 20, 'bold'))
    balance_label.pack(pady=10)

    # call update_balance_display to update the balance label
    update_balance_display()

    # doing deposit transactions
    def handle_deposit():
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None:
            if deposit_funds(username, amount):
                update_balance_display()
                messagebox.showinfo("Success", f" Deposit of R {amount} Successful")
            else:
                messagebox.showerror("Error", "Deposit Failed")

    # doing withdrawal transactions
    def handle_withdraw():
        amount = simpledialog.askfloat("Withdrawal", "Enter amount to withdraw:")
        if amount is not None:
            if withdraw_funds(username, amount):
                update_balance_display()
                messagebox.showinfo("Success", f"Withdrawal of R {amount}  Successful")
            else:
                messagebox.showerror("Error", "Withdrawal Failed")

    # doing transfer transactions
    def handle_transfer():
        beneficiaries = load_beneficiaries(username)
        if not beneficiaries:
            beneficiaries = []  # Initialize an empty list

        transfer_window = Toplevel(root)
        transfer_window.title("Transfer")
        center_window(transfer_window, 400, 450)      

        balance = get_balance(username)
        balance_label = ttk.Label(transfer_window, text=f"Balance: R {balance}", font=('Helvetica', 12, 'bold'))
        balance_label.pack(pady=10, fill='x')

        # Create a notebook with two tabs: Quick Pay and Beneficiaries
        notebook = ttk.Notebook(transfer_window)
        notebook.pack(pady=10, fill='both', expand=True)

        quick_pay_tab = ttk.Frame(notebook)
        notebook.add(quick_pay_tab, text="Quick Pay")

        beneficiaries_tab = ttk.Frame(notebook)
        notebook.add(beneficiaries_tab, text="Beneficiaries")

        # Quick Pay tab
        ttk.Label(quick_pay_tab, text="Full Name:").pack(pady=5)
        full_name_entry = ttk.Entry(quick_pay_tab)
        full_name_entry.pack(pady=5)

        ttk.Label(quick_pay_tab, text="Phone Number:").pack(pady=5)
        cell_number_entry = ttk.Entry(quick_pay_tab)
        cell_number_entry.pack(pady=5)

        ttk.Label(quick_pay_tab, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(quick_pay_tab)
        amount_entry.pack(pady=5)

        def execute_quick_pay():
            full_name = full_name_entry.get()
            cell_number = cell_number_entry.get()
            amount = float(amount_entry.get())
            # check if user exists
            if user_exists(cell_number):
                # make quick pay transfer (immediate by default)
                if transfer_funds(username, cell_number, amount, 0):
                    update_balance_display()
                    messagebox.showinfo("Success", f" Payment of R {amount}  successful!")
                    transfer_window.destroy()
                else:
                    messagebox.showerror("Error", "Transfer Failed")
            else:
                messagebox.showerror("Error", "User does not exist, are you sure they have an account?")


        quick_pay_button = ttk.Button(quick_pay_tab, text="Pay", command=execute_quick_pay)
        quick_pay_button.pack(pady=10)

        # Beneficiaries tab
        beneficiary_list_frame = ttk.Frame(beneficiaries_tab)
        beneficiary_list_frame.pack(pady=5, fill='both', expand=True)

        beneficiary_list = ttk.Treeview(beneficiary_list_frame, columns=("full_name"), show="headings")
        beneficiary_list.heading("full_name", text="My Beneficiaries")
        beneficiary_list.pack(side="left", fill="both", expand=True)

        # Load existing beneficiaries
        beneficiaries = load_beneficiaries(username)
        for beneficiary in beneficiaries:
            beneficiary_list.insert("", "end", values=(beneficiary["Full Name"],))

        def select_beneficiary():
            selected_item = beneficiary_list.selection()[0]
            selected_full_name = beneficiary_list.item(selected_item, "values")[0]
            transfer_to_beneficiary(username, selected_full_name)

        select_button = ttk.Button(beneficiary_list_frame, text="Select", command=select_beneficiary)
        select_button.pack(side="right", padx=10)

        add_beneficiary_button = ttk.Button(beneficiaries_tab, text="Add Beneficiary", command=lambda: add_beneficiary(transfer_window, username, beneficiary_list))
        add_beneficiary_button.pack(pady=10)


    def add_beneficiary(transfer_window, username, beneficiary_list):
        add_beneficiary_window = Toplevel(transfer_window)
        center_window(add_beneficiary_window, 350, 250)
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
                    # Check if beneficiary already exists
                    if not any(beneficiary["Full Name"] == full_name and beneficiary["Account Number"] == account_number for beneficiary in load_beneficiaries(username)):
                        # Add beneficiary to list
                        add_beneficiary_to_username_list(username, full_name, account_number)
                        # Update the Treeview widget
                        beneficiary_list.delete(*beneficiary_list.get_children())
                        updated_beneficiaries = load_beneficiaries(username)
                        for beneficiary in updated_beneficiaries:
                            beneficiary_list.insert("", "end", values=(beneficiary["Full Name"],))
                        
                        messagebox.showinfo("Success", "Beneficiary added successfully")
                        add_beneficiary_window.destroy()
                    else:
                        messagebox.showerror("Error", "Beneficiary already exists")
                else:
                    messagebox.showerror("Error", "Account does not exist")
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        add_button = ttk.Button(add_beneficiary_window, text="Add", command=add_beneficiary_to_list)
        add_button.pack(pady=10)

    def transfer_to_beneficiary(username, selected_full_name):
        # Load beneficiaries using username
        beneficiaries = load_beneficiaries(username)
        for beneficiary in beneficiaries:
            if beneficiary["Full Name"] == selected_full_name:
                account_number = beneficiary["Account Number"]
                open_transfer_window(username, account_number,selected_full_name)
                return 
        return None  # Account not found

    def open_transfer_window(username, account_number,selected_full_name):
        transfer_window = Toplevel(root)
        transfer_window.title("Transfer to Beneficiary")
        center_window(transfer_window, 400, 300)

        ttk.Label(transfer_window, text=f"Full Name: {selected_full_name}").pack(pady=5)  # Assuming account number is displayed
        ttk.Label(transfer_window, text="Account Number:").pack(pady=5)
        account_number_label = ttk.Label(transfer_window, text=account_number)
        account_number_label.pack(pady=5)

        ttk.Label(transfer_window, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(transfer_window)
        amount_entry.pack(pady=5)

        immediate_payment_var = BooleanVar()
        immediate_payment_checkbox = ttk.Checkbutton(transfer_window, text="Immediate Payment", variable=immediate_payment_var)
        immediate_payment_checkbox.pack(pady=5)

        def execute_transfer():
            # Get the values from the UI fields
            amount = float(amount_entry.get())
            is_express = immediate_payment_var.get()

            if get_balance(username) >= amount:
                # Call do_transfer with retrieved account number
                if transfer_funds(username, account_number, amount, 1, is_express):
                    update_balance_display()
                    messagebox.showinfo("Success",f" Transfer of R {amount} successful!")
                    transfer_window.destroy()
                else:
                    messagebox.showerror("Error", "Transfer Failed")  # Handle transfer failure from do_transfer
            else:
                log_transaction(username, "Transfer Declined", 3, get_balance(username))  # Log declined transaction

        transfer_button = ttk.Button(transfer_window, text="Transfer", command=execute_transfer)
        transfer_button.pack(pady=10)

    # Generate Statement section
    generate_statement_frame = ttk.Frame(frame)
    generate_statement_frame.pack(pady=10, fill='x')

    def generate_statement_with_months():
        months = simpledialog.askinteger("Generate Statement", "Enter number of months 1-3", parent=root, minvalue=1, maxvalue=3)
        if months is None:
            return  # user cancelled the dialog
        elif months < 1:
            messagebox.showerror("Invalid Input", "Number of months must be at least 1")
        elif months > 3:
            messagebox.showerror("Invalid Input", "Maximum number of months is 3")
        else:
            messagebox.showinfo("Generating Statement", "Please wait, Bank statement is being generated")
            root.update_idletasks()  # update the GUI to show the message

            generate_statement(username, months)

            messagebox.showinfo("Statement Sent", "Your bank statement has been sent to your email!")

    deposit_button = ttk.Button(frame, text="Deposit", command=handle_deposit)
    deposit_button.pack(pady=5)

    withdraw_button = ttk.Button(frame, text="Withdraw", command=handle_withdraw)
    withdraw_button.pack(pady=5)

    transfer_button = ttk.Button(frame, text="Transfer", command=handle_transfer)
    transfer_button.pack(pady=5)

    statement_button = ttk.Button(frame, text="Generate Statement", command=generate_statement_with_months)
    statement_button.pack(pady=5)

    logout_button = ttk.Button(frame, text="Logout", command=lambda: create_signin_screen(root, navigate))
    logout_button.pack(pady=5)



