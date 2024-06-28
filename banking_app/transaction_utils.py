from datetime import datetime, timedelta
import logging
from banking_app.email_utils import send_email
from banking_app.utils import get_account_number, get_full_name, get_user_email,get_user_transactions, get_username_from_account_number, get_username_from_cell_number, log_transaction, log_error, update_balance, get_balance, generate_delay

TRANSACTION_LOG = "data/TransactionLog.txt"

def deposit_funds(username, amount):
    if amount <= 0:
        log_error(username, "Invalid amount for deposit")
        return False

    try:
        balance = get_balance(username)
        new_amount = amount - 5  # Deduct the R5 charge
        new_balance = balance + new_amount  # Add the deposited amount
        update_balance(username, new_balance)
        log_transaction(username, "Deposit", amount, new_balance)
        return True
    except Exception as e:
        log_error(username, str(e))
        return False

def withdraw_funds(username, amount):
    if amount <= 0:
        log_error(username, "Invalid amount for withdrawal")
        return False
    
    try:
        balance = get_balance(username)
        if balance >= amount:
            new_balance = balance - amount - 2 # R2 charge
            update_balance(username, new_balance) 
            log_transaction(username, "Withdraw", amount, new_balance)
            return True
        else:
            log_transaction(username, "Withdraw Declined", 3, balance)  # R3 charge for declined transaction
            update_balance(username, balance - 3)
            return False
    except Exception as e:
        log_error(username, str(e))
        return False

def transfer_funds(username, recipient_identifier, amount, tab_index, is_express=False):
    if amount <= 0:
        log_error(username, "Invalid amount for transfer")
        return False
    
    try:
        sender_balance = get_balance(username)
        if sender_balance is None:
            raise ValueError(f"Could not retrieve balance for sender {username}")

        if tab_index == 0:  # Quick Pay tab
            charge = 0
            recipient_username = get_username_from_cell_number(recipient_identifier)
            if recipient_username is None:
                raise ValueError(f"Could not find username for recipient account number {recipient_identifier}")
        else:  # Beneficiaries tab
            if is_express:
                charge = 10
            else:
                charge = 4.50
            recipient_username = get_username_from_account_number(recipient_identifier)
            if recipient_username is None:
                raise ValueError(f"Could not find username for recipient account number {recipient_identifier}")

        if sender_balance >= amount + charge:
            # Deduct amount and charge from sender's balance
            new_sender_balance = sender_balance - amount - charge
            update_balance(username, new_sender_balance)
            log_transaction(username, "Transfer", amount, new_sender_balance)

            # Add amount to recipient's balance
            recipient_balance = get_balance(recipient_username)
            if recipient_balance is None:
                raise ValueError(f"Could not retrieve balance for recipient {recipient_username}")
            update_balance(recipient_username, recipient_balance + amount)
            log_transaction(recipient_username, "Transfer Received", amount, recipient_balance + amount)

            return True  # Transfer successful
        else:
            log_transaction(username, "Transfer Declined", 3, sender_balance)  # Log declined transaction
            return False  # Insufficient funds for transfer
    except Exception as e:
        log_error(username, str(e))
        return False  # Transfer failed due to exception or error


def generate_statement(username, months):
    try:
        transactions = get_user_transactions(username, months)
        email = get_user_email(username)
        full_name = get_full_name(username)
        account_number = get_account_number(full_name)
        statement_header = (
            f"Tech Junkies Bank\n\n"
            f"Bank Statement\n"
            f"From Date: {transactions[0]['date']}\n"
            f"To Date: {transactions[-1]['date']}\n"
            f"Print Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            f"Personal Details\n"
            f"{full_name}\n"
            f"Account Number: {account_number}\n\n"
            f"{'Date':<26}{'Description':<30}{'Money In (R)':>20} {'Money Out (R)':>20} {'Balance (R)':>15}\n"
            f"{'-' * 80}\n"
        )
        statement_body = "\n".join(
            [
                f"{t['date']:<20}{t['description']:<35}{t['money_in']:>23.2f} {t['money_out']:>15.2f} {t['balance']:>15.2f}"
                for t in transactions
            ]
        )
        statement_footer = f"\n{'-' * 80}\n"
        send_email(email, "Your Bank Statement", statement_header + statement_body + statement_footer)
    except Exception as e:
        log_error(username, str(e))
