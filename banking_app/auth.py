import hashlib
from banking_app.utils import log_error

def login_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        with open("data/BankData.txt", "r") as file:
            for line in file:
                full_name, dob, id_number, email, phone, uname, pwd_hash, account_number = line.strip().split(',')
                if uname == username and pwd_hash == password_hash:
                    return True
        return False
    except Exception as e:
        log_error(str(e), username)
        return False
