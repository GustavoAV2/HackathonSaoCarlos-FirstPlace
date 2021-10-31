from brutils import cpf, cnpj

from app.actions.client_actions import get_client_by_id
from app.actions.serasa_actions import get_receita_by_cpf, get_receita_by_cnpj
from app.models.client import Client
from app.models.scores import Score
from app.models.groups import Group
from database.repository import save, delete, commit
from typing import Dict, List

def create_client_scores(client: Client) -> Score or None:
    try:
        client = get_client_by_id(client.id)

        if client:
            return save(Score(
                client_id=client.id
            ))
    except (AttributeError, KeyError, TypeError):
        return



def first_approvation(score:Score) -> Score or None:
    try:
        cpf_or_cnpj = score.client.cpf_or_cnpj
        if cpf.validate(cpf_or_cnpj):
            get_receita_by_cpf(cpf_or_cnpj)
        elif cnpj.validate(cpf_or_cnpj):
            get_receita_by_cnpj(cpf_or_cnpj)

    except (AttributeError, KeyError, TypeError):
        return


def get_groups() -> List[Group]:
    groups = Group.query.all()
    return groups


def get_group_by_name(name: str):
    return Group.query.filter(Group.name == name).first()
