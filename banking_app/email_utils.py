import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from banking_app.utils import log_error

def send_email(recipient, subject, body):
    try:
        sender_email = "v.spanuel3@gmail.com"
        sender_password = "PHOKAmofokeng"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
    except Exception as e:
        log_error(str(e))
