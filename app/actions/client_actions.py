from app.models.client import Client
from database.repository import save, delete, commit
from typing import Dict, List
from app.tools.validate_cep import validate_address


def download_file(file):
    return ""


def create_client(data: Dict) -> Client or None:
    path_doc1 = download_file(data)
    path_doc2 = download_file(data)
    path_doc3 = download_file(data)

    if not validate_address(data.get('cep', '')):
        return

    try:
        return save(Client(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            address=data.get('address'),
            cep=data.get('cep'),
            cpf=data.get('cpf_or_cnpj'),
            legal_person=data.get('legal_person'),

            document=path_doc1,
            document2=path_doc2,
            document3=path_doc3
        ))
    except (AttributeError, KeyError, TypeError):
        return
