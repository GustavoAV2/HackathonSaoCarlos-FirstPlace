from typing import Dict, Tuple, Any, List
from app.actions.send_email_actions import send_alert_group, send_client_decline_message, send_commercial_mail
from flask import Blueprint, jsonify, request, render_template
from app.actions.client_actions import get_client_by_cpf_or_cnpj
from app.actions.request_actions import update_request, get_request_by_id, request_next_level

app_request = Blueprint('request', __name__)


@app_request.route('/next_level/<id_request>', methods=['GET', 'POST'])
def next_level(id_request) -> Tuple[Any, int]:
    if request.method == 'GET':
        if get_request_by_id(id_request):
            return render_template('accept_client.html', id_request=id_request)
        return render_template('error404.html')

    content = request.values
    client = get_client_by_cpf_or_cnpj(content.get('cpf_or_cnpj'))
    if client:
        _request = request_next_level(id_request)
        if _request:
            send_alert_group(client.id)
            return render_template('accept_client.html', cpf_or_cnpj=_request.client.cpf_or_cnpj,
                                   status=True, message='Solicitação enviada para o FINANCEIRO!')

    return render_template('accept_client.html', status=False, message='CPF ou CNPJ não existe!')


@app_request.route('/request/approve/<id_request>', methods=['GET'])
def approve(id_request) -> Tuple[Any, int]:
    data = {'approved': True}
    _request = update_request(data, id_request)
    if request:
        _request = request_next_level(id_request)
        send_alert_group(_request.client_id)
        return render_template('accept_client.html', cpf_or_cnpj=_request.client.cpf_or_cnpj,
                               status=True, message='Solicitação APROVADA!')

    return render_template('accept_client.html', status=False, message='CPF ou CNPJ não existe!')


@app_request.route('/request/decline/<id_request>', methods=['GET'])
def decline(id_request) -> Tuple[Any, int]:
    data = {'approved': False, 'active': False}
    _request = update_request(data, id_request)
    if request:
        send_commercial_mail(_request.client_id)
        send_client_decline_message(_request.client.email)
        return render_template('accept_client.html', cpf_or_cnpj=_request.client.cpf_or_cnpj,
                               status=True, message='Solicitação NEGADA!')
    return render_template('accept_client.html', status=False, message='CPF ou CNPJ não existe!')


@app_request.route('/request/develop', methods=['GET'])
def develop_create() -> Tuple[Any, int]:
    from app.tools.creating_user_groups import create_users_and_groups
    create_users_and_groups()
    return jsonify({}), 200
