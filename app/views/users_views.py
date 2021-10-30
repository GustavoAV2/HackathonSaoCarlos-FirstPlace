from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from typing import Dict, Tuple, Any, List

from app.actions.users_actions import \
    get_user_by_id, get_users, update_user, create_user, login, deleted_user

from app.models.users import User


app_users = Blueprint('users', __name__)


@app_users.route('/users', methods=['POST'])
def post() -> Tuple[Any, int]:
    payload = request.get_json()
    user: User = create_user(payload)
    return jsonify(user.serialize()), 201


@app_users.route('/users/<user_id>', methods=['PUT'])
@jwt_required
def update(user_id) -> Tuple[Any, int]:
    payload = request.get_json()
    user = update_user(user_id, payload)
    return jsonify(user.serialize()), 201


@app_users.route('/users', methods=['GET'])
@jwt_required
def get() -> Tuple[List[Dict], int]:
    return jsonify([user.serialize() for user in get_users()]), 200


@app_users.route('/users/<id>', methods=['GET'])
@jwt_required
def get_by_id(user_id) -> Tuple[Any, int]:
    user = get_user_by_id(user_id)
    return jsonify(user.serialize()), 200


@app_users.route('/users/me', methods=['GET'])
@jwt_required
def view_user() -> Tuple[Any, int]:
    user_id: str = get_jwt_identity()
    user: User = get_user_by_id(user_id)
    return jsonify(user.serialize()), 200


@app_users.route('/users/delete/<id_user>', methods=['DELETE'])
@jwt_required
def delete(id_user) -> Tuple[Any, int]:
    user: User = deleted_user(id_user)
    return jsonify(user.serialize()), 200
