import json
import requests


def is_cnpj(s):
    return False


def get_info_by_cpf_or_cnpj(cpf_or_cnpj: str):
    """
    API Document: https://www.cpfcnpj.com.br/dev/
    :param cpf_or_cnpj:
    :return:
    """
    package = 9
    if is_cnpj(cpf_or_cnpj):
        package = 6
    status = requests.get(f'https://api.cpfcnpj.com.br/5ae973d7a997af13f0aaf2bf60e65803/{package}/{cpf_or_cnpj}')

    content = json.loads(status.text)
    return content
