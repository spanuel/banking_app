import bcrypt
from banking_app.utils import log_error

USERS_FILE = "data/BankData.txt"

def login_user(username, password):
    try:
        with open(USERS_FILE, 'r') as file:
            users = file.readlines()
            for user in users:
                user_details = eval(user.strip())
                if user_details["Username"] == username and bcrypt.checkpw(password.encode(), user_details["Password"].encode()):
                    return True
        return False
    except Exception as e:
        log_error(username, str(e))
        return False

def save_user(full_name, dob, id_number, email, phone, username, password, account_number):
    try:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user_details = {
            "Full Name": full_name,
            "Date of Birth": dob,
            "ID Number": id_number,
            "Email Address": email,
            "Phone Number": phone,
            "Username": username,
            "Password": hashed_password,
            "Account Number": account_number,
            "Balance": 0.0  # Initialize balance to 0.0
        }
        with open(USERS_FILE, 'a') as file:
            file.write(str(user_details) + '\n')
    except Exception as e:
        log_error(username, str(e))
