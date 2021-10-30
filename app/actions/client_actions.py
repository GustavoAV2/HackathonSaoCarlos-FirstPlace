from app.models.client import Client
from database.repository import save, delete, commit
from typing import Dict, List
from app.tools.validate_cep import validate_address


def download_file(file):
    return ""


def create_client(data: Dict, id_user, file1, file2, file3) -> Client or None:
    path_doc1 = download_file(data)
    path_doc2 = download_file(data)
    path_doc3 = download_file(data)

    if validate_address(data.get('cep')) is None:
        return "Endereço inválido"
    else:
        pass
    try:
        return save(Client(
            id=id_user,
            name=data.get('name'),
            email=data.get('email'),
            address=data.get('address'),
            cep=data.get('cep'),
            cpf=data.get('cpf_or_cnpj'),
            legal_person=data.get('legal_person'),

            document=file1,
            document2=file2,
            document3=file3
        ))
    except (AttributeError, KeyError, TypeError):
        return


def get_cep(cep: str):
    pass
