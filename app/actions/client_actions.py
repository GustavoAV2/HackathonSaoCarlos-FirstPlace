from app.models.client import Client
from database.repository import save, delete, commit
from sqlalchemy.exc import IntegrityError
from typing import Dict, List
from app.tools.validate_cep import validate_address


def download_file(file):
    return ""


def create_client(data: Dict) -> Client or None:
    # birth_file = download_file(data.get('birth_file'))
    # wedding_file = download_file(data.get('wedding_file'))
    # residence_file = download_file(data.get('residence_file'))
    # income_tax_file = download_file(data.get('income_tax_file'))
    birth_file = ""
    wedding_file = ""
    residence_file = ""
    income_tax_file = ""

    try:
        legal_person = bool(data.get('legal_person')) if data.get('legal_person') else False
    except (TypeError, ValueError):
        legal_person = False

    if not validate_address(data.get('zipcode', '')):
        return

    try:
        return save(Client(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            cpf_or_cnpj=data.get('cpf_or_cnpj'),
            rg=data.get('rg'),
            address=data.get('address'),
            email=data.get('email'),
            phone=data.get('phone'),
            cep=data.get('zipcode'),
            legal_person=legal_person,

            birth_file=birth_file,
            wedding_file=wedding_file,
            residence_file=residence_file,
            income_tax_file=income_tax_file,
        ))
    except (AttributeError, KeyError, TypeError, IntegrityError):
        return


def get_client_by_id(_id: str):
    return Client.query.get(_id)


def update_user(client_id: str, data: Dict) -> Client:
    client: Client = get_client_by_id(client_id)
    list_keys = list(data.keys())

    client.active = data.get('active') if list_keys.count('active') else client.active
    client.first_name = data.get('first_name') if data.get('first_name') else client.first_name
    client.last_name = data.get('last_name') if data.get('last_name') else client.last_name
    client.email = data.get('email') if data.get('email') else client.email
    client.phone = data.get('phone') if data.get('phone') else client.phone
    client.address = data.get('address') if data.get('address') else client.address
    client.cep = data.get('cep') if data.get('cep') else client.cep
    client.cpf = data.get('cpf') if data.get('cpf') else client.cpf
    client.legal_person = data.get('legal_person') if data.get('legal_person') else client.legal_person

    # Update files
    client.rg_file = data.get('rg_file') if data.get('rg_file') else client.rg_file
    client.birth_file = data.get('birth_file') if data.get('birth_file') else client.birth_file
    client.wedding_file = data.get('wedding_file') if data.get('wedding_file') else client.wedding_file
    client.residence_file = data.get('residence_file') if data.get('residence_file') else client.residence_file
    client.income_tax_file = data.get('income_tax_file') if data.get('income_tax_file') else client.income_tax_file

    commit()
    return client
