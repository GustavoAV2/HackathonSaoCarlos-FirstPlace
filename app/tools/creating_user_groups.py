from app.actions import groups_actions
from app.actions import users_actions
from settings import EMAIL


def create_users_and_groups():
    email = 'gustavoant.voltolini@gmail.com'
    groups = ['Comercial', 'Financeiro', 'Juridico']
    [groups_actions.create_groups(group, email, index + 1) for index, group in enumerate(groups)]

    for n in groups:
        users_actions.create_user({
            'email': email,
            'password': 'admin',
            'group': n,
        })
    return True
