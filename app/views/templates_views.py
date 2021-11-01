import time

from app.models.users import User
from app.actions.groups_actions import get_groups
from app.actions.spouse_actions import create_spouse
from app.actions.request_actions import create_request
from app.actions.users_actions import login, create_user
from flask import Blueprint, render_template, request, redirect
from app.actions.client_actions import create_client, get_client_by_id, update_client
from app.actions.send_email_actions import send_client_analysis_message, send_client_register_spouse_url, \
    send_alert_group


app_views = Blueprint('views', __name__)


# Templates
@app_views.route('/', methods=['GET'])
def home_view():
    return redirect('/register')


@app_views.route('/login', methods=['POST', 'GET'])
def login_view():
    if request.method == 'GET':
        return render_template('login.html', status=True)

    credentials = request.values
    if login(credentials.get('email'), credentials.get("password")):
        return redirect('/')
    return render_template('login.html', status=False)


@app_views.route('/user/register', methods=['POST', 'GET'])
def user_register_view():
    if request.method == 'GET':
        groups = [group.serialize() for group in get_groups()]
        return render_template('register_user.html', status=True, groups=groups)

    content = request.values
    user: User = create_user(content)
    if user:
        if user.active:
            return redirect('/login')
    return render_template('register_user.html', status=False)


@app_views.route('/register', methods=['POST', 'GET'])
def register_view():
    if request.method == 'GET':
        return render_template('register_client.html', status=True)

    content = request.values
    files = request.files
    client = create_client(content, files)
    if client:
        try:
            if content.get('spouse'):
                send_client_register_spouse_url(client.email, f'spouse/{client.id}/register')

                return render_template('register_spouse.html', status=True, message='Cadastre seu conjugê para terminar'
                                                                                    ' a solicitação!')
        except (ValueError, TypeError):
            ...
        if create_request(client.id):
            send_client_analysis_message(client.email)
            time.sleep(1)
            send_alert_group(client.id)
            return render_template('register_client.html', status=True, message='Sua solicitação foi enviada com '
                                   'sucesso!\nApós a analise você terá a resposta por e-mail.')
    return render_template('register_client.html', status=False, message='Erro na solicitação, verifique os campos!')


@app_views.route('/spouse/<_id>/register', methods=['POST', 'GET'])
def spouse_register_view(_id):
    client = get_client_by_id(_id)
    if client:
        if request.method == 'GET':
            return render_template('register_spouse.html', id=_id, status=True)

        content = request.values
        files = request.files
        if files.get('wedding_file'):
            spouse = create_spouse(content, files)
            if spouse:
                update_client(_id, {'spouse_id': spouse.id, 'wedding_file': files.get('wedding_file')})
                if create_request(_id):
                    send_client_analysis_message(client.email)
                    send_alert_group(_id)
                    return render_template('register_spouse.html', status=True, message='Sua solicitação '
                                           'foi enviada com sucesso!\nApós a analise você terá a resposta por e-mail.')

        return render_template('register_spouse.html', status=False,
                               message='Erro na solicitação, verifique os campos!')
    return redirect('/register')
