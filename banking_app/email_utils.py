import smtplib
from email.mime.text import MIMEText
from banking_app.utils import log_error

def send_email(to_address, subject, body):
    try:
        from_address = "v.spanuel3@gmail.com"
        password = "prjj duhg irfn inls"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_address, password)
            server.sendmail(from_address, to_address, msg.as_string())
    except Exception as e:
        log_error(to_address, str(e))
