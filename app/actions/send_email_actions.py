from settings import URL_APP
from app.tools.send_email import send_email, send_email_app_code
from app.actions.groups_actions import get_groups


def send_analysis_message(email: str):
    subject = "Solicitacao em análise"
    body_email = "Obrigado por enviar sua solicitacao!\nEstamos analisando seu pedido."
    send_email_app_code(email, body_email, subject)


def send_register_spouse_url(email: str, url: str):
    subject = "Cadastro conjuge"
    body_email = f"Para concluir a solicitacao faça o cadastro do seu conjuge acessando o link abaixo.\n" \
                 f"OBS: Se o cadastro ja foi feito, desconsidere esse email" \
                 f"{URL_APP}{url}"
    send_email_app_code(email, body_email, subject)


# def send_alert_group(level: int, client_id: int):
#     send_email_app_code(email, body_email, subject)
