from typing import Dict, List
from datetime import timedelta
from app.models.users import User
from flask_jwt_extended import create_access_token
from database.repository import save, delete, commit
from werkzeug.security import generate_password_hash
from app.actions.groups_actions import get_group_by_name


def login(email, password) -> Dict or None:
    try:
        user = get_user_by_email(email)

        if user:
            if not user.verify_password(password) or not user.active:
                return

            access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=600))
            return {'access_token': access_token}
    except (AttributeError, KeyError, TypeError):
        return


def create_user(data: Dict) -> User or None:
    try:
        group = get_group_by_name(data.get('group'))

        if group:
            return save(User(
                email=data.get('email'),
                password=generate_password_hash(data.get('password')),
                group_id=group.id
            ))
    except (AttributeError, KeyError, TypeError):
        return


def update_user(user_id: str, data: Dict) -> User:
    user: User = get_user_by_id(user_id)
    list_keys = list(data.keys())

    user.email = data.get('email') if data.get('email') else user.email
    user.active = data.get('active') if list_keys.count('active') else user.active
    user.password = generate_password_hash(data.get('password')) if data.get('password') else user.password

    commit()
    return user


def deleted_user(user_id: str) -> User:
    user: User = get_user_by_id(user_id)
    delete(user)
    commit()
    return user


def get_users() -> List[User]:
    users = User.query.all()
    return users


def get_user_by_id(user_id: str) -> User:
    return User.query.get(user_id)


def get_user_by_email(email: str) -> User:
    return User.query.filter(User.email == email).first()
