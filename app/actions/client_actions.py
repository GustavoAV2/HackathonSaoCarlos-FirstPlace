from werkzeug.utils import secure_filename

from app.models import request
from app.models.client import Client
from database.repository import save, delete, commit
from typing import Dict, List, Tuple
from app.tools.validate_cep import validate_address
import os
import time


def download_file_save(id_user: str, file1_received, file2_received, file3_received) -> Tuple:
    file_saved1 = save_file(file1_received, id_user)
    file_saved2 = save_file(file2_received, id_user)
    file_saved3 = save_file(file3_received, id_user)
    return file_saved1, file_saved2, file_saved3


def save_file(file, user_id: str) -> str:
    upload_folder = os.path.join(os.getcwd(), f'upload\\{user_id}')
    try:
        os.mkdir(upload_folder)
        time.sleep(0.2)
    except (FileExistsError, FileNotFoundError):
        pass
    save_path = os.path.join(upload_folder, secure_filename(file.filename))
    try:
        file.save(save_path)
    except (FileExistsError, FileNotFoundError):
        pass
    print(upload_folder[-43:] + "\\" + file.filename)
    file_path = upload_folder[-43:] + "\\" + file.filename
    return file_path


def create_client(data: Dict, id_user, file1, file2, file3) -> Client or None:
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
