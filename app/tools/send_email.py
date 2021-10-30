import smtplib
from typing import NoReturn
from settings import EMAIL, EMAIL_PASSWORD


def send_email(user: dict, body_email: str, subject_email: str) -> NoReturn:
    _email_address = EMAIL
    _email_password = EMAIL_PASSWORD
    _email_receiver = user["email"]

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(_email_address, _email_password)
        subject = subject_email
        body = body_email
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(_email_address, _email_receiver, msg)