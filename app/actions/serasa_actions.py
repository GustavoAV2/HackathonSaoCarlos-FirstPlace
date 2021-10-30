import json
import requests
from app.tools.validate_cpf_and_cnpj import validate_cpf, validate_cnpj


def get_info_by_cpf(cpf: str):
    """
    API Document: https://www.cpfcnpj.com.br/dev/
    :param cpf:
    :return:
    """
    if validate_cpf(cpf):
        package = 9
        status = requests.get(f'https://api.cpfcnpj.com.br/5ae973d7a997af13f0aaf2bf60e65803/{package}/{cpf}')

        content = json.loads(status.text)
        return content


def get_info_by_cnpj(cnpj: str):
    """
    API Document: https://www.cpfcnpj.com.br/dev/
    :param cnpj:
    :return:
    """
    if validate_cnpj(cnpj):
        package = 6
        status = requests.get(f'https://api.cpfcnpj.com.br/5ae973d7a997af13f0aaf2bf60e65803/{package}/{cnpj}')

        content = json.loads(status.text)
        return content
