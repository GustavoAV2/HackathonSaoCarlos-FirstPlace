from uuid import uuid4
from typing import Dict, NoReturn
from settings import URL_APP
from app.actions.serasa_actions import get_receita_by_cpf, get_receita_by_cnpj
from app.models.client import Client
from sqlalchemy.exc import IntegrityError, InterfaceError

from app.tools.send_email import send_email_app_code_attachment
from database.repository import save, commit
from app.actions.actions_file import save_file
from app.tools.validate_cep import validate_address


def create_client(data: Dict, files) -> Client or None:
    if not validate_address(data.get('zipcode')):
        return
    try:
        legal_person = bool(data.get('legal_person')) if data.get('legal_person') else False
    except (TypeError, ValueError):
        legal_person = False

    try:
        _id = str(uuid4())
        client = Client(
            id=_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            rg=data.get('rg'),
            cep=data.get('zipcode'),
            cpf_or_cnpj=data.get('cpf_or_cnpj'),
            legal_person=legal_person
        )

        client.birth_file = save_file(files.get('birth_file', ''), _id + '_birth')
        client.residence_file = save_file(files.get('residence_file', ''), _id + '_residence')
        client.income_tax_file = save_file(files.get('income_tax_file', ''), _id + '_income')
        client_saved = save(client)
        send_email_with_activation_code(client_saved.id)
        return client_saved
    except (AttributeError, KeyError, TypeError, IntegrityError) as ex:
        return


def get_the_customer_information(cpf_cnpj):
    if len(cpf_cnpj) == 11:
        return get_receita_by_cpf(cpf_cnpj)
    else:
        return get_receita_by_cnpj(cpf_cnpj)


def send_email_with_activation_code(id_user: dict) -> NoReturn:
    user = get_client_by_id(id_user['id']).serialize()
    score_data = get_the_customer_information(user['cpf_or_cnpj'])

    body_email = f""" Seguem os dados para aprovação de cadastro:

                            Nome: {user['first_name']} {user['last_name']}                    
                            CPF: {user['cpf_or_cnpj']}
                            RG: {user['rg']}
                            Email: {user['email']}
                            Endereço: {user['address']}
                            Cep: {user['cep']}
                            Telefone: {user['phone']}

                            Score Serasa: {score_data['score']}
                            Situação da Receita: {score_data['situacao']}

                            Aprovar: {URL_APP}/1qe1wr3etmnb3r3ety1ym/nb3vcXxzs2b3r3etyh48yt94j/{user['id']}

                            Negar: {URL_APP}/3ety1ymnbmnb3r3ety1ym/nb3vcXxzs2dwrmnb3vcXeyt94j/{user['id']}

                            """

    send_email_app_code_attachment(user['email'],
                                   body_email,
                                   f"Aprovação de Cadastro de cliente: {user['first_name']} {user['last_name']}",
                                   score_data['birth_file'], score_data['wedding_file'],
                                   score_data['residence_file'],
                                   score_data['income_tax_file'])


def get_client_by_id(_id: str):
    return Client.query.get(_id)


def to_approve(id: str):
    client = get_client_by_id(id)
    client.financial_registration_approval = True
    return

def to_disapprove(id: str):
    client = get_client_by_id(id)
    client.financial_registration_approval = False
    return


def update_user(client_id: str, data: Dict) -> Client or None:
    try:
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

        client.spouse_id = data.get('spouse_id') if data.get('spouse_id') else client.spouse_id

        # Update files
        client.birth_file = data.get('birth_file') if data.get('birth_file') else client.birth_file
        client.wedding_file = data.get('wedding_file') if data.get('wedding_file') else client.wedding_file
        client.residence_file = data.get('residence_file') if data.get('residence_file') else client.residence_file
        client.income_tax_file = data.get('income_tax_file') if data.get('income_tax_file') else client.income_tax_file

        commit()
        return client
    except (AttributeError, KeyError, TypeError, IntegrityError) as ex:
        return
