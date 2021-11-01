from datetime import datetime
from typing import List

from app.actions.serasa_actions import get_receita_by_cpf, get_receita_by_cnpj, get_serasa_pendencies
from app.models.client import Client
from app.models.scores import Score
from database.repository import save, commit
from settings import COMPANY_CREATION_DATE_CRITERIA, ALLOWED_CPF_CNPJ_SITUATIONS, MINIMUM_SERASA_SCORE


def create_client_scores(client: Client) -> Score or None:
    try:
        if client:
            return save(Score(
                client_id=client.id,
                company_creation_date=get_company_creation_date_from_api(client),
                cpf_or_cnpj_situation=cpf_or_cnpj_situation_from_api(client),
                serasa_score=get_serasa_score_from_api(client),
                serasa_pendency=get_serasa_pendencies_from_api()
            ))

    except (AttributeError, KeyError, TypeError):
        return


def get_serasa_pendencies_from_api():
    return get_serasa_pendencies()


def get_approval_reasons(score: Score) -> List:
    reasons = []
    firstapprove = first_approve(score)
    secondapprove = second_approve(score)

    if firstapprove.get('approvation') == "Aprovado" and secondapprove.get('approvation') == "Aprovado":
        reasons = (firstapprove.get('reasons') + secondapprove.get('reasons'))

    elif firstapprove.get('approvation') == "Aprovado" and secondapprove.get('approvation') == "Reprovado":
        reasons = secondapprove.get('reasons')

    elif firstapprove.get('approvation') == "Reprovado" and secondapprove.get('approvation') == "Aprovado":
        reasons = firstapprove.get('reasons')

    elif firstapprove.get('approvation') == "Reprovado" and secondapprove.get('approvation') == "Reprovado":
        reasons = (firstapprove.get('reasons') + secondapprove.get('reasons'))

    return reasons


def get_approvals(score):
    firstapprove = first_approve(score)
    secondapprove = second_approve(score)

    if firstapprove.get('approvation') == "Aprovado" and secondapprove.get('approvation') == "Aprovado":
        approvation = "Aprovado"
    else:
        approvation = "Reprovado"

    risk_level = firstapprove.get('risk level') + secondapprove.get('risk level')
    risk_level_string = get_risk_level_string(risk_level)

    update_score(score, risk_level_string, approvation)

    return {"approvation": approvation, 'risk level': risk_level_string}


def update_score(score: Score, risk_level_string, approvation) -> Score:
    score.final_approve = approvation
    score.risk_level = risk_level_string
    commit()
    return score


def get_risk_level_string(risk_level):
    RISK_LEVEL_APPROVAL_POINTS = {0: 'Risco Baixo', 3: 'Risco Moderado', 5: 'Risco Alto', 7: "Risco muito alto"}
    risk_level_points = RISK_LEVEL_APPROVAL_POINTS

    if risk_level >= 7:
        return risk_level_points.get(7)
    elif risk_level >= 5:
        return risk_level_points.get(5)
    elif risk_level >= 3:
        return risk_level_points.get(3)
    elif risk_level >= 0:
        return risk_level_points.get(0)


def first_approve(score):
    '''
    Consulta regularidade de cpf e criação da companhia se houver cnpj
    cpf_or_cnpj_situation pode ser 'regular', 'Pendente de regularização', 'Suspensa' , 'Cancelada' ou 'Nula'

    retorna se foi aprovado ou não, nivel de risco e razões da aprovação/reprovação

    '''
    risk_level = 0
    reasons = []
    cpf_or_cnpj_situation = score.cpf_or_cnpj_situation
    company_creation_date_score = calculate_company_creation_date_score(score)

    # cpf_or_cnpj_situation = "Regular"
    # company_creation_date_score = "Ruim"

    company_time_in_market = COMPANY_CREATION_DATE_CRITERIA.get(company_creation_date_score)
    reasons.append(f"CPF consta como {cpf_or_cnpj_situation} na Receita Federal")

    if cpf_or_cnpj_situation not in ALLOWED_CPF_CNPJ_SITUATIONS:
        risk_level += 4
        return {"approvation": 'Reprovado', "risk level": risk_level, 'reasons': reasons}
    else:
        approvation = "Aprovado"

    if company_creation_date_score == "Muito bom":
        approvation = "Aprovado"
        reasons.append(
            f"A compania está há {company_time_in_market} anos no mercado")

    elif company_creation_date_score == "Bom":
        approvation = "Aprovado"
        risk_level += 1
        reasons.append(
            f"A compania está há {company_time_in_market} anos no mercado")

    elif company_creation_date_score == "Ruim":
        approvation = "Aprovado"
        risk_level += 2
        reasons.append(
            f"A compania está há {company_time_in_market} anos no mercado")

    elif company_creation_date_score == "Muito ruim":
        approvation = "Reprovado"
        risk_level += 3
        reasons.append(
            f"A compania está há {company_time_in_market} anos no mercado")

    return {"approvation": approvation, 'risk level': risk_level, 'reasons': reasons}


def calculate_company_creation_date_score(score: Score):
    company_creation_date = score.company_creation_date
    if company_creation_date != "":
        today_date = datetime.now()

        date_time_obj = datetime.strptime(company_creation_date, '%d/%m/%Y')

        difference_in_years = (today_date.year - date_time_obj.year) + today_date.month - date_time_obj.month

        for criteria, value in COMPANY_CREATION_DATE_CRITERIA.items():
            if difference_in_years >= value:
                return criteria
    else:
        return ""


def second_approve(score: Score):
    '''
    Serasa score 0-300 baixa, 301-500 regular, 501-700 boa, 701-1000, muito boa

    :return:
    '''
    risk_level = 0
    reasons = []
    serasa_score = score.serasa_score
    serasa_pendency = score.serasa_pendency
    # serasa_score = 502
    # serasa_pendency = "Regular"

    if serasa_pendency == "Constam dívidas pendentes do titular":
        approvation = "Reprovado"
        reasons.append('Constam dividas no Serasa')
        risk_level += 4
        return {"approvation": approvation, 'risk level': risk_level, 'reasons': reasons}
    else:
        reasons.append(f'Não constam pendencias no Serasa')

    if serasa_score >= 701:
        reasons.append(f'Score no serasa: {serasa_score}')
    elif serasa_score >= 501:
        reasons.append(f'Score no serasa: {serasa_score}')
        risk_level += 1
    elif serasa_score >= 301:
        reasons.append(f'Score no serasa: {serasa_score}')
        risk_level += 2
    elif serasa_score >= 0:
        reasons.append(f'Score no serasa: {serasa_score}')
        risk_level += 3

    if serasa_score >= MINIMUM_SERASA_SCORE:
        approvation = "Aprovado"
    else:
        approvation = "Reprovado"

    return {"approvation": approvation, 'risk level': risk_level, 'reasons': reasons}


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


def get_serasa_score_from_api(client: Client):
    try:
        receita_dict = get_receita_by_cnpj(client.cpf_or_cnpj)
        serasa_score = receita_dict.get("score")
        if serasa_score:
            return int(serasa_score)
        else:
            return 0

    except (AttributeError, KeyError, TypeError):
        return


def get_score_by_id(score_id: str) -> Score:
    return Score.query.get(score_id)
