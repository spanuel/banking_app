from banking_app.utils import get_user_balance, update_user_balance, log_transaction, log_error

def deposit_funds(username, amount):
    try:
        balance = get_user_balance(username)
        new_balance = balance + amount
        update_user_balance(username, new_balance)
        log_transaction(username, "Deposit", amount, 0, new_balance)
    except Exception as e:
        log_error(str(e), username)

def withdraw_funds(username, amount):
    try:
        balance = get_user_balance(username)
        if amount > balance:
            raise ValueError("Insufficient funds")
        new_balance = balance - amount
        update_user_balance(username, new_balance)
        log_transaction(username, "Withdraw", 0, amount, new_balance)
    except Exception as e:
        log_error(str(e), username)

def transfer_funds(username, recipient, amount):
    try:
        withdraw_funds(username, amount)
        deposit_funds(recipient, amount)
        log_transaction(username, "Transfer", 0, amount, get_user_balance(username))
        log_transaction(recipient, "Transfer", amount, 0, get_user_balance(recipient))
    except Exception as e:
        log_error(str(e), username)
