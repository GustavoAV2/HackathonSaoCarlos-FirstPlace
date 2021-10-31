import json
import random
from random import randint

import requests

from app.tools.validate_cpf_and_cnpj import validate_cpf, validate_cnpj
from settings import SERASA_PENDENCIES


def get_receita_by_cpf(cpf: str):
    """
    API Document: https://www.cpfcnpj.com.br/dev/
    :param cpf:
    :return:
    """
    if validate_cpf(cpf):
        package = 9
        status = requests.get(f'https://api.cpfcnpj.com.br/5ae973d7a997af13f0aaf2bf60e65803/{package}/{cpf}')

        content = json.loads(status.text)
        get_score(content)
        return content


def get_receita_by_cnpj(cnpj: str):
    """
    API Document: https://www.cpfcnpj.com.br/dev/
    :param cnpj:
    :return:
    """
    if validate_cnpj(cnpj):
        package = 6
        status = requests.get(f'https://api.cpfcnpj.com.br/5ae973d7a997af13f0aaf2bf60e65803/{package}/{cnpj}')

        content = json.loads(status.text)
        get_score(content)
        return content


def get_score(user):
    """
    Função que deve buscar o score do Cliente via API paga.
    :param user:
    :return:
    """
    user['score'] = randint(1, 1000)
    return user


def get_serasa_pendencies():
    """
    Função que deve buscar o score do Cliente via API paga.
    :param user:
    :return:
    """
    pendencies_list = SERASA_PENDENCIES
    pendency = random.choice(pendencies_list)
    return pendency
