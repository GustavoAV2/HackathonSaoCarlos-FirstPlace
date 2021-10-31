from typing import Dict
from app.models.request import Request
from app.actions.client_actions import get_client_by_id
from database.repository import save, delete, commit
from app.actions.groups_actions import get_groups


def create_request(client_id):
    try:
        user = get_client_by_id(client_id)
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

    request.level = data.get('level') if data.get('level') else request.level
    request.active = data.get('active') if list_keys.count('active') else request.active
    request.approved = data.get('approved') if data.get('approved') else request.approved
    request.client_id = data.get('client_id') if data.get('client_id') else request.client_id

    commit()
    return request


def request_next_level(_id: str):
    request = get_request_by_id(_id)
    groups = get_groups()
    new_level = request.level + 1

    if request <= len(groups):
        update_request({'level': new_level})
        return request

    return
