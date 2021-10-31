from typing import Dict
from app.models.request import Request
from app.actions.users_actions import get_user_by_id
from database.repository import save, delete, commit


def create_request(client_id):
    try:
        user = get_user_by_id(client_id)
        if user:
            return save(Request(
                client_id=user.id
            ))
    except (AttributeError, KeyError, TypeError):
        return


def get_request_by_id(_id: str):
    return Request.query.get(_id)


def update_request(data: Dict, _id: str):
    request = get_request_by_id(_id)
    list_keys = list(data.keys())

    request.active = data.get('active') if list_keys.count('active') else request.active
    request.approved = data.get('approved') if data.get('approved') else request.approved
    request.client_id = data.get('client_id') if data.get('client_id') else request.client_id

    commit()
    return request
