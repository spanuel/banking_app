import json
import logging
import string
import time
import random
from datetime import datetime, timedelta

logging.basicConfig(filename="data/error_log.txt", level=logging.ERROR, format='%(asctime)s %(message)s')

USERS_FILE = "data/BankData.txt"
TRANSACTIONS_FILE = "data/TransactionLog.txt"

#validating id number
def validate_id_number(id_number, dob):
    if len(id_number)!= 13 or not id_number.isdigit():
        return False

    id_dob = id_number[:6]
    id_year = int(id_dob[:2]) + 1900
    id_month = int(id_dob[2:4])
    id_day = int(id_dob[4:])

    dob_parts = dob.split('/')
    dob_month = int(dob_parts[0])
    dob_day = int(dob_parts[1])
    dob_year = int(dob_parts[2])

    return id_year == dob_year and id_month == dob_month and id_day == dob_day

#generating password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

#generating account number
def generate_account_number():
    first_digit = '6'
    unique_part = str(random.randint(10, 99))
    random_part = ''.join(random.choices('0123456789', k=7))
    return first_digit + unique_part + random_part

#log all transactions to file
def log_transaction(username, description, amount, balance):
    transaction = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "username": username,
        "description": description,
        "amount": amount,
        "type": "deposit" if description == "Deposit" else "withdrawal" if description == "Withdraw" else "transfer",
        "balance": balance
    }
    with open("data/TransactionLog.txt", 'a') as file:
        file.write(json.dumps(transaction) + "\n")

#log all errors to file
def log_error(username, error_message):
    logging.error(f"{username} - {error_message}")

#updating user's account balance
def update_balance(username, new_balance):
    lines = []
    found = False
    with open(USERS_FILE, 'r') as file:
        lines = file.readlines()
    
    with open(USERS_FILE, 'w') as file:
        for line in lines:
            user_details = eval(line.strip())
            if user_details["Username"] == username:
                user_details["Balance"] = new_balance
                found = True
            file.write(str(user_details) + '\n')
    
    if not found:
        log_error(username, "User not found when updating balance")

#get user email
def get_user_email(username):
    with open(USERS_FILE, 'r') as file:
        for line in file:
            user_details = eval(line.strip())
            if user_details["Username"] == username:
                return user_details["Email Address"]
    return None

#get user account number
def get_account_number(username):
    with open(USERS_FILE, 'r') as file:
        for line in file:
            user_details = eval(line.strip())
            if user_details["Username"] == username:
                return user_details["Account Number"]
    return None

#getting balance
def get_balance(username):
    with open(USERS_FILE, 'r') as file:
        for line in file:
            user_details = eval(line.strip())
            if user_details["Username"] == username:
                return float(user_details["Balance"])
    return None

#getting all user transactions
def get_user_transactions(username, months):
    transactions = []
    with open(TRANSACTIONS_FILE, 'r') as file:
        for line in file:
            try:
                transaction = json.loads(line.strip())
                if transaction["username"] == username:
                    transaction_date = datetime.strptime(transaction["date"], '%Y-%m-%d')
                    if transaction_date >= datetime.now() - timedelta(days=months*30):
                        transaction["account_number"] = get_account_number(username)
                        if transaction["type"] == 'deposit':
                            transaction["money_in"] = transaction["amount"]
                            transaction["money_out"] = 0
                        elif transaction["type"] == 'withdrawal':
                            transaction["money_in"] = 0
                            transaction["money_out"] = transaction["amount"]
                        elif transaction["type"] == 'transfer':
                            transaction["money_in"] = 0
                            transaction["money_out"] = transaction["amount"]
                        # Calculate the balance
                        if transactions:
                            if transaction["type"] == 'transfer':
                                # Assuming the transfer is from the current account
                                previous_balance = transactions[-1]["balance"]
                                transaction["balance"] = previous_balance - transaction["amount"]
                            else:
                                previous_balance = transactions[-1]["balance"]
                                transaction["balance"] = previous_balance + transaction["money_in"] - transaction["money_out"]
                        else:
                            if transaction["type"] == 'transfer':
                                # Assuming the initial balance is 0
                                transaction["balance"] = -transaction["amount"]
                            else:
                                transaction["balance"] = transaction["money_in"] - transaction["money_out"]
                        transactions.append(transaction)
            except json.JSONDecodeError:
                log_error(username, "Invalid transaction format")
    return transactions

def generate_delay():
    time.sleep(random.randint(60, 120))  # Delay for 1-2 minutes

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
