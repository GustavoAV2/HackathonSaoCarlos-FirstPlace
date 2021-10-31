from typing import List
from settings import URL_APP
from app.tools.send_email import send_email, send_email_app_code
from app.actions.client_actions import get_client_by_id
from app.actions.groups_actions import get_group_by_level
from settings import SEND_ALL_GROUP, STANDARD_MESSAGE, URL_APP, URL_ACCEPT
import threading


def send_client_analysis_message(email: str):
    subject = "Solicitacao em análise"
    body_email = "Obrigado por enviar sua solicitacao!\nEstamos analisando seu pedido."
    send_email_app_code(email, body_email, subject)


def send_client_register_spouse_url(email: str, url: str):
    subject = "Cadastro conjuge"
    body_email = f"Para concluir a solicitacao faça o cadastro do seu conjuge acessando o link abaixo.\n" \
                 f"OBS: Se o cadastro ja foi feito, desconsidere esse email" \
                 f"{URL_APP}{url}"
    send_email_app_code(email, body_email, subject)


def send_alert_group(client_id: str):
    client = get_client_by_id(client_id)
    request = None
    if client.request:
        request = client.request[0]

    group = get_group_by_level(request.level)

    if client and group and client.request:
        if SEND_ALL_GROUP:
            body_message = STANDARD_MESSAGE + '\nUse o link para passar a proposta para o financeiro:' + \
                           URL_APP + URL_ACCEPT + request.id
            emails = [user.email for user in group.users]
            th = threading.Thread(target=send_many_mails,
                                  kwargs={'emails': emails, 'message': body_message, 'subject': STANDARD_MESSAGE})
            th.start()
            return True
        else:
            email = group.email
            if email:
                send_many_mails([email], STANDARD_MESSAGE, STANDARD_MESSAGE)
            return True
    return False


def send_many_mails(emails: List, message: str, subject):
    for email in emails:
        send_email_app_code(email, message, subject)
