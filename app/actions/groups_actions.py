from app.models.groups import Group
from database.repository import save, delete, commit
from typing import Dict, List


def create_groups(name: str, email: str, level: int) -> Group or None:
    try:
        return save(Group(
            name=name,
            email=email,
            level=level
        ))
    except (AttributeError, KeyError, TypeError):
        return


def get_groups() -> List[Group]:
    groups = Group.query.all()
    return groups


def get_group_by_name(name: str):
    return Group.query.filter(Group.name == name).first()


def get_group_by_groups(name: str):
    return Group.query.filter(Group.name == name).first()
