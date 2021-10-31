from datetime import datetime

from app.actions.client_actions import get_client_by_id
from app.actions.serasa_actions import get_receita_by_cpf, get_receita_by_cnpj
from app.models.client import Client
from app.models.scores import Score
from database.repository import save

# Company Settings
COMPANY_CREATION_DATE_CRITERIA = {'very good': 10, "good": 5, 'bad': 2, 'very bad': 0}


def create_client_scores(client: Client) -> Score or None:
    try:
        client = get_client_by_id(client.id)

        if client:
            return save(Score(
                client_id=client.id,
                company_creation_date=get_company_creation_date_from_api(client),
                cpf_or_cnpj_situation=cpf_or_cnpj_situation_from_api(client)
            ))
    except (AttributeError, KeyError, TypeError):
        return


def cpf_or_cnpj_situation_from_api(client: Client) -> Score or None:
    try:
        cpf_or_cnpj = client.cpf_or_cnpj
        if client.legal_person:
            receita_dict = get_receita_by_cpf(cpf_or_cnpj)
        else:
            receita_dict = get_receita_by_cnpj(cpf_or_cnpj)

        cpf_or_cnpj_situation = receita_dict.get('situacao')

        if cpf_or_cnpj_situation:
            return cpf_or_cnpj_situation
        else:
            return ""

    except (AttributeError, KeyError, TypeError):
        return


def get_company_creation_date_from_api(client: Client):
    try:
        if client.legal_person:
            return ""
        else:
            receita_dict = get_receita_by_cnpj(client.cpf_or_cnpj)
            creation_date = receita_dict.get("inicioAtividade")
            if creation_date:
                return creation_date
            else:
                return ""

    except (AttributeError, KeyError, TypeError):
        return


def get_approvals():
    first_approve()
    second_approve()
    third_approve()
    final_approve()


def first_approve(score):
    cpf_or_cnpj_situation = score.cpf_or_cnpj_situation
    company_creation_date_score = calculate_company_creation_date_score(score)
    if cpf_or_cnpj_situation != "Regular":
        score.first_approved = "não aprovado"
        return score.first_approved
    elif company_creation_date_score == "very good":
        pass

    pass

def calculate_company_creation_date_score(score: Score):
    company_creation_date = score.company_creation_date
    today_date = datetime.now()
    date_time_obj = datetime.strptime(company_creation_date, '%d/%m/%Y')

    difference_in_years = (today_date.year - date_time_obj.year) + today_date.month - date_time_obj.month

    for criteria, value in COMPANY_CREATION_DATE_CRITERIA.items():
        if difference_in_years >= value:
            return criteria

def second_approve():
    pass


def third_approve():
    pass


def final_approve():
    pass


print(get_receita_by_cpf('07889706901'))
# print(get_receita_by_cnpj('07526557000100'))
# print(first_approve())
# def get_groups() -> List[Group]:
#     groups = Group.query.all()
#     return groups
#
#
# def get_group_by_name(name: str):
#     return Group.query.filter(Group.name == name).first()
