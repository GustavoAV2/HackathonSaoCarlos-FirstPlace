from typing import Dict, Tuple, Any, List
from flask import Blueprint, jsonify, request
from app.actions.request_actions import update_request


app_request = Blueprint('request', __name__)


@app_request.route('/request/approve/<id_request>', methods=['PATCH'])
def approve(id_request) -> Tuple[Any, int]:
    data = {'approved': True}
    update_request(data, id_request)
    return jsonify(request.serialize()), 200


@app_request.route('/request/decline/<id_request>', methods=['PATCH'])
def decline(id_request) -> Tuple[Any, int]:
    data = {'approved': False}
    update_request(data, id_request)
    return jsonify(request.serialize()), 200
