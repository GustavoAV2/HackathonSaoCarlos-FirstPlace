from settings import FILE_UPLOAD
from werkzeug.utils import secure_filename
from app.models.client import Client
from database.repository import save, commit
from typing import Dict, List, Tuple
from sqlalchemy.exc import IntegrityError
from app.tools.validate_cep import validate_address
import os
import time
import random


def save_file(file, filename: str) -> str:
    if file:
        upload_folder = os.path.join(os.getcwd(), f'{FILE_UPLOAD}{filename}')
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
    return ''


def create_client(data: Dict) -> Client or None:
    if not validate_address(data.get('zipcode')):
        return
    try:
        legal_person = bool(data.get('legal_person')) if data.get('legal_person') else False
    except (TypeError, ValueError):
        legal_person = False

    try:
        files = data.get('files')
        client = Client(
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
        client.birth_file = ''
        client.wedding_file = ''
        client.residence_file = ''
        client.income_tax_file = ''
        # client.birth_file = save_file(files.get('certidao_nascimento'), client.id + '_birth'),
        # client.wedding_file = save_file(files.get('certidao_casamento'), client.id + '_wedding'),
        # client.residence_file = save_file(files.get('comprovante_residencia'), client.id + '_residence'),
        # client.income_tax_file = save_file(files.get('imposto_de_renda'), client.id + '_income')
        return save(client)
    except (AttributeError, KeyError, TypeError, IntegrityError) as ex:
        return


def get_client_by_id(_id: str):
    return Client.query.get(_id)


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
