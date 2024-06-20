import logging
import time
import random
from datetime import datetime, timedelta

logging.basicConfig(filename="data/error_log.txt", level=logging.ERROR, format='%(asctime)s %(message)s')

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

def generate_password():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=12))

def generate_account_number():
    first_digit = '6'
    unique_part = str(random.randint(10, 99))
    random_part = ''.join(random.choices('0123456789', k=7))
    return first_digit + unique_part + random_part

def log_transaction(username, description, amount, balance):
    with open("data/TransactionLog.txt", 'a') as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d')},{username},{description},{amount},{balance}\n")

def log_error(username, error_message):
    logging.error(f"{username} - {error_message}")

def update_balance(username, new_balance):
    lines = []
    found = False
    with open("data/BankData.txt", 'r') as file:
        lines = file.readlines()
    
    with open("data/BankData.txt", 'w') as file:
        for line in lines:
            user_details = line.strip().split(',')
            if user_details[5] == username:
                user_details[8] = str(new_balance)
                found = True
            file.write(','.join(user_details) + '\n')
    
    if not found:
        log_error(username, "User not found when updating balance")

def get_balance(username):
    with open("data/BankData.txt", 'r') as file:
        for line in file:
            user_details = line.strip().split(',')
            if user_details[5] == username:
                return float(user_details[8])
    log_error(username, "User not found when fetching balance")
    return 0.0

def get_user_transactions(username, months):
    transactions = []
    cutoff_date = datetime.now() - timedelta(days=30 * months)
    with open("data/TransactionLog.txt", 'r') as file:
        for line in file:
            date, user, description, amount, balance = line.strip().split(',')
            if user == username and datetime.strptime(date, '%Y-%m-%d') >= cutoff_date:
                transactions.append({
                    "date": date,
                    "description": description,
                    "money_in": amount if description in ["Deposit", "Transfer Received"] else "",
                    "money_out": amount if description in ["Withdraw", "Transfer", "Transfer Declined", "Withdraw Declined"] else "",
                    "balance": balance
                })
    return transactions

def generate_delay():
    time.sleep(random.randint(60, 120))  # Delay for 1-2 minutes

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
