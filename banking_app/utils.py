import json
import logging
import os
import string
import time
import random
from datetime import datetime, timedelta

logging.basicConfig(filename="data/error_log.txt", level=logging.ERROR, format='%(asctime)s %(message)s')

USERS_FILE = "data/BankData.txt"
TRANSACTIONS_FILE = "data/TransactionLog.txt"

#validating id number
def validate_id_number(id_number, dob):
    try:
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
    except Exception as e:
        log_error("validate_id_number", f"An error occurred: {e}")
        return False

#validating email
def validate_email(email):
    try:
        if "@" not in email:
            return False
        parts = email.split("@")
        if len(parts)!= 2:
            return False
        local_part, domain = parts
        if len(local_part) > 64 or len(domain) > 253:
            return False
        if not all(c.isalnum() or c in "-._" for c in local_part):
            return False
        if not all(c.isalnum() or c in "-." for c in domain):
            return False
        return True
    except Exception as e:
        log_error("validate_email", f"An error occurred: {e}")
        return False

#validating phone number
def validate_phone_number(phone_number):
    try:
        if len(phone_number)!= 10 or not phone_number.isdigit():
            return False
        return True
    except Exception as e:
        log_error("validate_phone_number", f"An error occurred: {e}")
        return False

#generating password
def generate_random_password(length=12):
    try:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    except Exception as e:
        log_error("generate_password", f"An error occurred: {e}")
        return None

#generating account number
def generate_account_number():
    try:
        first_digit = '6'
        unique_part = str(random.randint(10, 99))
        random_part = ''.join(random.choices('0123456789', k=7))
        return first_digit + unique_part + random_part
    except Exception as e:
        log_error("generate_account_number", f"An error occurred: {e}")
        return None

#log all transactions to file
def log_transaction(username, description, amount, balance):
    try:
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
    except Exception as e:
        log_error(username, f"An error occurred while logging transaction: {e}")

#log all errors to file
def log_error(username, error_message):
    logging.error(f"{username} - {error_message}")

#updating user's account balance
def update_balance(username, amount):
    try:
        lines = []
        found = False
        with open(USERS_FILE, 'r') as file:
            lines = file.readlines()

        with open(USERS_FILE, 'w') as file:
            for line in lines:
                user_details = eval(line.strip())
                if user_details["Username"] == username:
                    user_details["Balance"] = float(amount)
                    found = True
                file.write(str(user_details) + '\n')

        if not found:
            log_error(username, "User not found when updating balance")
    except Exception as e:
        log_error(username, f"An error occurred while updating balance:{e}")

#creating file to add or load beneficiaries from based on user
def create_beneficiary_file(username):
    try:
        filename = f"data/beneficiaries/beneficiaries_{username}.txt"
        with open(filename, "w") as file:
            pass  # Create the file
    except Exception as e:
        log_error(username, f"An error occurred while creating beneficiary file: {e}")

#load the existing list of beneficiaries
def load_beneficiaries(username):
    try:
        filename = f"data/beneficiaries/beneficiaries_{username}.txt"
        if not os.path.exists(filename):
            return [] 
        with open(filename, "r") as file:
            return [eval(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        with open(filename, "w") as file:  # Create the file if it does not exist
            return []  # Return an empty list if the file is new
    except Exception as e:
        log_error(username, f"An error occurred while loading beneficiaries: {e}")
        return []

#this method will be called to save the updated list back to the file
def save_beneficiaries(username, beneficiaries):
    try:
        filename = f"data/beneficiaries/beneficiaries_{username}.txt"
        with open(filename, "w") as file:
            for beneficiary in beneficiaries:
                file.write(str(beneficiary) + "\n")
    except Exception as e:
        log_error(username, f"An error occurred while saving beneficiaries: {e}")

#new beneficiary is added to the list
def add_beneficiary_to_username_list(username, full_name, account_number):
    try:
        beneficiaries = load_beneficiaries(username)
        for beneficiary in beneficiaries:
            if beneficiary["Full Name"] == full_name and beneficiary["Account Number"] == account_number:
                return  # Beneficiary already exists
        beneficiary = {
            "Username": username,
            "Full Name": full_name,  
            "Account Number": account_number  
        }
        beneficiaries.append(beneficiary)
        save_beneficiaries(username, beneficiaries)
    except Exception as e:
        log_error(username, f"An error occurred while adding beneficiary: {e}")

#checking if user cell number exists
def user_exists(cell_number):
    try:
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_details = eval(line.strip())
                if user_details["Phone Number"] == cell_number:
                    return True
        return False
    except Exception as e:
        log_error("user_exists", f"An error occurred: {e}")
        return False

#checking if account exists
def account_exists(account_number):
    try:
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_details = eval(line.strip())
                if user_details["Account Number"] == account_number:
                    return True
        return False
    except Exception as e:
        log_error("account_exists", f"An error occurred: {e}")
        return False

#getting username by cellphone number
def get_username_from_cell_number(cell_number):
    try:
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_details = eval(line.strip())
                if user_details["Phone Number"] == cell_number:
                    return user_details["Username"]
        return None
    except Exception as e:
        log_error("get_username_from_cell_number", f"An error occurred: {e}")
        return None

#getting username by account number
def get_username_from_account_number(account_number):
    try:
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_details = eval(line.strip())
                if user_details["Account Number"] == account_number:
                    return user_details["Username"]
        return None
    except Exception as e:
        log_error("get_username_from_account_number", f"An error occurred: {e}")
        return None

#getting user email
def get_user_email(username):
    try:
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_details = eval(line.strip())
                if user_details["Username"] == username:
                    return user_details["Email Address"]
        return None
    except Exception as e:
        log_error("get_user_email", f"An error occurred: {e}")
        return None

#getting full name
def get_full_name(username):
    with open(USERS_FILE, 'r') as file:
        for line in file:
            user_details = eval(line.strip())
            if user_details["Username"] == username:
                return user_details["Full Name"]
    return None

#getting user account number by full name
def get_account_number(full_name):
    try:
        full_name = full_name.lower()
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_details = eval(line.strip())
                if user_details["Full Name"].lower() == full_name:
                    return user_details["Account Number"]
        return None
    except Exception as e:
        log_error("get_account_number", f"An error occurred: {e}")
        return None

#getting balance
def get_balance(username):
    try:
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_details = eval(line.strip())
                if user_details["Username"] == username:
                    return float(user_details["Balance"])
        return None
    except Exception as e:
        log_error(username, f"An error occurred while getting balance: {e}")
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
                        transactions.append(transaction)
            except (json.JSONDecodeError, ValueError):
                log_error(username, "Invalid transaction format")
    # Sort transactions by date
    transactions.sort(key=lambda x: x["date"])
    # Calculate the balance
    balance = get_balance(username)  # Get the initial balance from somewhere
    for transaction in transactions:
        if transaction["type"] == 'transfer':
            balance -= transaction["amount"]
        else:
            balance += transaction["money_in"] - transaction["money_out"]
        transaction["balance"] = balance
    return transactions

def generate_delay():
    time.sleep(random.randint(60, 120))  # Delay for 1-2 minutes

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
