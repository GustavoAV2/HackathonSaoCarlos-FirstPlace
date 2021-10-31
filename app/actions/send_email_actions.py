from settings import URL_APP
from app.tools.send_email import send_email, send_email_app_code


def send_analysis_message(email: str):
    subject = "Solicitacao em análise"
    body_email = "Obrigado por enviar sua solicitacao!\nEstamos analisando seu pedido."
    send_email_app_code(email, body_email, subject)


def send_register_spouse_url(email: str, url: str):
    subject = "Cadastro conjuge"
    body_email = f"Para concluir a solicitacao faça o cadastro do seu conjuge acessando o link abaixo.\n" \
                 f"{URL_APP}{url}"
    send_email_app_code(email, body_email, subject)
