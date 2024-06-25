from datetime import datetime, timedelta
import logging
from banking_app.email_utils import send_email
from banking_app.utils import get_account_number, get_user_email,get_user_transactions, log_transaction, log_error, update_balance, get_balance, generate_delay

TRANSACTION_LOG = "data/TransactionLog.txt"

def deposit_funds(username, amount):
    try:
        balance = get_balance(username)
        new_balance = balance + amount - 5  # R5 charge
        update_balance(username, new_balance)
        log_transaction(username, "Deposit", amount, new_balance)
        return True
    except Exception as e:
        log_error(username, str(e))
        return False

def withdraw_funds(username, amount):
    try:
        balance = get_balance(username)
        if balance >= amount:
            new_balance = balance - amount - 2  # R2 charge
            update_balance(username, new_balance)
            log_transaction(username, "Withdraw", amount, new_balance)
            return True
        else:
            log_transaction(username, "Withdraw Declined", 3, balance - 3)  # R3 charge for declined transaction
            return False
    except Exception as e:
        log_error(username, str(e))
        return False

def transfer_funds(username, recipient_identifier, amount, immediate=False):
    try:
        sender_balance = get_balance(username)
        if sender_balance is None:
            raise ValueError(f"Could not retrieve balance for sender {username}")

        if sender_balance >= amount:
            # Proceed with the transfer
            if immediate:
                charge = 10  
            else:
                charge = 4.5  
                generate_delay()  # transfer processing delay

            # Deduct amount from sender's balance
            new_sender_balance = sender_balance - amount - charge
            update_balance(username, new_sender_balance)
            log_transaction(username, "Transfer", amount, new_sender_balance)

            # Log the transfer received by recipient (assuming the recipient exists)
            update_balance(recipient_identifier, get_balance(recipient_identifier) + amount)
            log_transaction(recipient_identifier, "Transfer Received", amount, get_balance(recipient_identifier))

            return True  # Transfer successful
        else:
            log_transaction(username, "Transfer Declined", 3, sender_balance - 3)  # R3 charge for declined transaction
            return False  # Insufficient funds for transfer
    except Exception as e:
        log_error(username, str(e))
        return False  # Transfer failed due to exception or error


def generate_statement(username, months):
    try:
        transactions = get_user_transactions(username, months)
        email = get_user_email(username)
        account_number = get_account_number(username)
        statement_header = (
            f"Tech Junkies Bank\n\n"
            f"Bank Statement\n"
            f"From Date: {transactions[0]['date']}\n"
            f"To Date: {transactions[-1]['date']}\n"
            f"Print Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            f"Personal Details\n"
            f"{username}\n"
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
