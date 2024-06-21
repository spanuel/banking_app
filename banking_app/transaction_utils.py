from datetime import datetime, timedelta
from banking_app.email_utils import send_email
from banking_app.utils import get_user_transactions, log_transaction, log_error, update_balance, get_balance, generate_delay

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

def transfer_funds(username, recipient, amount, immediate=False):
    try:
        balance = get_balance(username)
        if balance >= amount:
            if immediate:
                charge = 10
            else:
                charge = 4.5
                generate_delay()

            new_balance = balance - amount - charge
            update_balance(username, new_balance)
            update_balance(recipient, get_balance(recipient) + amount)
            log_transaction(username, "Transfer", amount, new_balance)
            log_transaction(recipient, "Transfer Received", amount, get_balance(recipient))
            return True
        else:
            log_transaction(username, "Transfer Declined", 3, balance - 3)  # R3 charge for declined transaction
            return False
    except Exception as e:
        log_error(username, str(e))
        return False

def generate_statement(username, months):
    try:
        transactions = get_user_transactions(username, months)
        statement_header = (
            f"Tech Junkies Bank\n\n"
            f"Bank Statement\n"
            f"From Date: {transactions[0]['date']}\n"
            f"To Date: {transactions[-1]['date']}\n"
            f"Print Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            f"Personal Details\n"
            f"{username}\n"
            f"Account Number: {transactions[0]['Account Number']}\n\n"
            f"Transaction Date\tDescription\tMoney In (R)\tMoney Out (R)\tBalance (R)\n"
        )
        statement_body = "\n".join([f"{t['date']}\t{t['description']}\t{t['money_in']}\t{t['money_out']}\t{t['balance']}" for t in transactions])
        send_email(username, "Your Bank Statement", statement_header + statement_body)
    except Exception as e:
        log_error(username, str(e))
