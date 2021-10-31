from uuid import uuid4
from typing import Dict, List, Tuple
from app.models.spouse import Spouse
from sqlalchemy.exc import IntegrityError
from database.repository import save, commit
from app.actions.actions_file import save_file


def create_spouse(data: Dict, files) -> Spouse or None:
    try:
        legal_person = bool(data.get('legal_person')) if data.get('legal_person') else False
    except (TypeError, ValueError):
        legal_person = False

    try:
        _id = str(uuid4())
        spouse = Spouse(
            id=_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            rg=data.get('rg'),
            cpf_or_cnpj=data.get('cpf_or_cnpj'),
            legal_person=legal_person
        )
        spouse.income_tax_file = save_file(files.get('income_tax_file'), 'SPO' + _id + '_income')
        return save(spouse)
    except (AttributeError, KeyError, TypeError, IntegrityError) as ex:
        return
