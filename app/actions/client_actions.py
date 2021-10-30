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


def download_file_save(rg_file, birth_file, wedding_file, residence_file, income_tax_file) -> Tuple:
    id_user = str(uuid4())
    rg_file_saved = save_file(rg_file, id_user)
    birth_file_saved = save_file(birth_file, id_user)
    wedding_file_saved = save_file(wedding_file, id_user)
    residence_file_saved = save_file(residence_file, id_user)
    income_tax_file_saved = save_file(income_tax_file, id_user)
    return id_user, rg_file_saved, birth_file_saved, wedding_file_saved, residence_file_saved, income_tax_file_saved


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


def create_client(data: Dict, id_user: str, rg_file, birth_file, wedding_file, residence_file, income_tax_file) -> Client or None:
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

            rg_file=rg_file,
            birth_file=birth_file,
            wedding_file=wedding_file,
            residence_file=residence_file,
            income_tax_file=income_tax_file
        ))
    except (AttributeError, KeyError, TypeError):
        return
