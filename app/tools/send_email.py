import os
import smtplib
from typing import NoReturn
from settings import EMAIL, EMAIL_PASSWORD, FILE_UPLOAD
from email.message import EmailMessage


def send_email_app_code(to_user_email: str, body_email: str, subject: str) -> None:
    """
    Function to send email with smtlib, from Marvin email to "to_user_mail"
    inserting "body_content" in content of email

    :param to_user_email:
    :param subject:
    :param body_email:
    :return:
    """
    message = EmailMessage()
    message['subject'] = subject
    message['from'] = EMAIL
    message['to'] = to_user_email
    message.set_content(body_email)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, EMAIL_PASSWORD)
        smtp.send_message(message)


def send_email_app_code_attachment(to_user_email: str, body_email: str, subject: str, birth_file: str,
                                   wedding_file: str, residence_file: str, income_tax_file: str,
                                   income_tax_file_spouse="") -> None:
    message = EmailMessage()
    message['subject'] = subject
    message['from'] = EMAIL
    message['to'] = to_user_email
    message.set_content(body_email)
    files = [birth_file, wedding_file, residence_file, income_tax_file]
    if income_tax_file_spouse:
        files.append(income_tax_file_spouse)
    for file in files:
        try:
            if file:
                if file.startswith('\\'):
                    path = 'upload' + file
                else:
                    path = 'upload\\' + file
                with open(path, 'rb') as f:
                    file_data = f.read()
                    file_name = f.name
                message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        except FileNotFoundError:
            pass
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, EMAIL_PASSWORD)
        smtp.send_message(message)


def send_email(email: str, body_email: str, subject_email: str) -> NoReturn:
    _email_address = EMAIL
    _email_password = EMAIL_PASSWORD
    _email_receiver = email

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(_email_address, _email_password)
        subject = subject_email
        body = body_email
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(_email_address, _email_receiver, msg)
