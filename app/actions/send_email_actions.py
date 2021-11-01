from typing import List
from app.tools.send_email import send_email_app_code
from app.actions.client_actions import get_client_by_id, send_email_with_activation_code, creating_body_mail
from app.actions.groups_actions import get_group_by_level
from settings import SEND_ALL_GROUP, STANDARD_MESSAGE, URL_APP, URL_ACCEPT
from app.tools.levels_endpoints import links
import threading


def send_client_analysis_message(email: str):
    subject = "Solicitacao em análise"
    body_email = "Obrigado por enviar sua solicitacao!\nEstamos analisando seu pedido."
    send_email_app_code(email, body_email, subject)


def send_client_decline_message(email: str):
    subject = "Proposta negada!"
    body_email = "Obrigado por enviar sua solicitacao!\nMas infelizmente sua proposta foi negada."
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
            data = creating_body_mail(client_id, urls=links.get(group.level)(request.id))
            send_many_mails(group.users, data)
            return True
        else:
            email = group.email
            if email:
                data = creating_body_mail(client_id, urls=links.get(group.level)(request.id))
                send_many_mails(email, data)
            return True
    return False


def send_many_mails(users: List or str, data):
    if isinstance(users, str):
        return send_email_with_activation_code(users, data)

    for user in users:
        send_email_with_activation_code(user.email, data)


def send_commercial_mail(client_id):
    client = get_client_by_id(client_id)
    group = get_group_by_level(1)

    if client and group and client.request:
        if SEND_ALL_GROUP:
            for user in group.users:
                send_email_app_code(user.email, f"Proposta do cliente {client.first_name} {client.last_name}\n"
                                                f"CPF|CNPJ: {client.cpf_or_cnpj}\n"
                                                f"Situacao: NEGADA!",
                                    f"Proposta do cliente {client.last_name}|{client.cpf_or_cnpj} negada!")
            return True
        else:
            email = group.email
            if email:
                send_email_app_code(email, f"Proposta do cliente {client.first_name} {client.last_name}\n"
                                           f"CPF|CNPJ: {client.cpf_or_cnpj}\n"
                                           f"Situacao: NEGADA!",
                                    f"Proposta do cliente {client.last_name}|{client.cpf_or_cnpj} negada!")
            return True
    return False
