from uuid import uuid4

from werkzeug.utils import secure_filename
import os.path
from app.models import request
from app.models.client import Client
from database.repository import save, delete, commit
from typing import Dict, List, Tuple
from app.tools.validate_cep import validate_address
import os
import time
import random


def download_file_save(file1_received, file2_received, file3_received) -> Tuple:
    id_user = str(uuid4())
    file_saved1 = save_file(file1_received, id_user)
    file_saved2 = save_file(file2_received, id_user)
    file_saved3 = save_file(file3_received, id_user)
    return id_user, file_saved1, file_saved2, file_saved3


def save_file(file, user_id: str) -> str:
    upload_folder = os.path.join(os.getcwd(), f'upload\\{user_id}')
    try:
        os.mkdir(upload_folder)
        time.sleep(0.2)
    except (FileExistsError, FileNotFoundError):
        pass
    save_path: str = os.path.join(upload_folder, secure_filename(file.filename))
    try:
        if os.path.isfile(save_path):
            random_number: int = random.randint(0, 1000)
            save_path_rename: str = save_path[:-4] + str(random_number) + save_path[-4:]
            file.save(save_path_rename)
        file.save(save_path)

    except (FileExistsError, FileNotFoundError):
        pass

    file_path = upload_folder[-43:] + "\\" + file.filename
    return file_path


def create_client(data: Dict, id_user: str, file1, file2, file3) -> Client or None:
    if validate_address(data.get('cep')) is None:
        return "Endereço inválido"
    else:
        pass
    if not validate_address(data.get('cep', '')):
        return

    try:
        cli = Client()

        return save(Client(
            id=id_user,
            name=data.get('name'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
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
