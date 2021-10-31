from typing import Dict, Tuple, Any, List
from flask import Blueprint, jsonify, request, render_template
from app.actions.request_actions import update_request, get_request_by_id, request_next_level


app_request = Blueprint('request', __name__)


@app_request.route('/next_level/<id_request>', methods=['GET', 'PATCH'])
def next_level(id_request) -> Tuple[Any, int]:
    if request.method == 'GET':
        if get_request_by_id(id_request):
            return render_template('accept_client.html', id_request=id_request)
        return render_template('error404.html')

    _request = request_next_level(id_request)
    if _request:
        return render_template('accept_client.html', cpf_or_cnpj=_request.client.cpf_or_cnpj,
                               status=True, message='Solicitação enviada para o FINANCEIRO!')
    return render_template('error404.html')


@app_request.route('/request/approve/<id_request>', methods=['PATCH'])
def approve(id_request) -> Tuple[Any, int]:
    data = {'approved': True}
    _request = update_request(data, id_request)
    return render_template('accept_client.html', cpf_or_cnpj=_request.client.cpf_or_cnpj,
                           status=True, message='Solicitação APROVADA!')


@app_request.route('/request/decline/<id_request>', methods=['PATCH'])
def decline(id_request) -> Tuple[Any, int]:
    data = {'approved': False}
    _request = update_request(data, id_request)
    return render_template('accept_client.html', cpf_or_cnpj=_request.client.cpf_or_cnpj,
                           status=True, message='Solicitação NEGADA!')


# @app_request.route('/request/develop', methods=['GET'])
# def develop_create() -> Tuple[Any, int]:
#     from app.tools.creating_user_groups import create_users_and_groups
#     create_users_and_groups()
#     return jsonify({}), 200
