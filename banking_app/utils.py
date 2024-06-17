import hashlib
from datetime import datetime
import random

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

def generate_password(length=8):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+="
    password = "".join(random.choice(characters) for i in range(length))
    return password

def validate_id_number(id_number, dob):
    dob_parts = dob.split('-')
    dob_str = ''.join(dob_parts)
    return id_number.startswith(dob_str)

def generate_account_number():
    return str(random.randint(10000000, 99999999))

def save_user(full_name, dob, id_number, email, phone, username, password, account_number):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    with open("data/BankData.txt", "a") as file:
        file.write(f"{full_name},{dob},{id_number},{email},{phone},{username},{password_hash},{account_number}\n")

def log_transaction(username, description, money_in, money_out, balance):
    with open("data/TransactionLog.txt", "a") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{username},{description},{money_in},{money_out},{balance}\n")

def log_error(error, username=None):
    with open("data/ErrorLog.txt", "a") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{username if username else 'N/A'},{error}\n")

def get_user_balance(username):
    with open("data/BankData.txt", "r") as file:
        for line in file:
            data = line.strip().split(',')
            if data[5] == username:
                return float(data[7])
    return 0

def update_user_balance(username, new_balance):
    users = []
    with open("data/BankData.txt", "r") as file:
        users = file.readlines()
    with open("data/BankData.txt", "w") as file:
        for user in users:
            data = user.strip().split(',')
            if data[5] == username:
                data[7] = str(new_balance)
                file.write(','.join(data) + '\n')
            else:
                file.write(user)

def get_user_transactions(username):
    transactions = []
    with open("data/TransactionLog.txt", "r") as file:
        for line in file:
            data = line.strip().split(',')
            if data[1] == username:
                transactions.append({
                    'date': data[0],
                    'username': data[1],
                    'description': data[2],
                    'money_in': float(data[3]),
                    'money_out': float(data[4]),
                    'balance': float(data[5])
                })
    return transactions

def get_user_details(username):
    with open("data/BankData.txt", "r") as file:
        for line in file:
            data = line.strip().split(',')
            if data[5] == username:
                return {
                    'full_name': data[0],
                    'dob': data[1],
                    'id_number': data[2],
                    'email': data[3],
                    'phone': data[4],
                    'username': data[5],
                    'account_number': data[7]
                }
    return None
