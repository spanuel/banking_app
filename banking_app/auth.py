import bcrypt
from banking_app.utils import log_error

USERS_FILE = "data/BankData.txt"

def login_user(username, password):
    try:
        with open(USERS_FILE, 'r') as file:
            users = file.readlines()
            for user in users:
                user_details = user.strip().split(',')
                if user_details[5] == username and bcrypt.checkpw(password.encode(), user_details[6].encode()):
                    return True
        return False
    except Exception as e:
        log_error(username, str(e))
        return False

def save_user(full_name, dob, id_number, email, phone, username, password, account_number):
    try:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        with open(USERS_FILE, 'a') as file:
            file.write(f"{full_name},{dob},{id_number},{email},{phone},{username},{hashed_password},{account_number}\n")
    except Exception as e:
        log_error(username, str(e))
