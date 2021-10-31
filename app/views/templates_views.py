from app.models.users import User
from app.actions.groups_actions import get_groups
from app.actions.spouse_actions import create_spouse
from app.actions.request_actions import create_request
from app.actions.users_actions import login, create_user
from flask import Blueprint, render_template, request, redirect, jsonify
from app.actions.client_actions import create_client, get_client_by_id, update_user, to_approve, to_disapprove
from app.actions.send_email_actions import send_analysis_message, send_register_spouse_url


app_views = Blueprint('views', __name__)


# Templates
@app_views.route('/', methods=['GET'])
def home_view():
    _json = request.get_json()
    return render_template('index.html')


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
    user = create_client(content, files)
    if user:
        try:
            if content.get('spouse'):
                send_register_spouse_url(user.email, f'spouse/{user.id}/register')

                return render_template('register_spouse.html', status=True, message='Cadastre seu conjugê para terminar'
                                                                                    ' a solicitação!')
        except (ValueError, TypeError):
            ...

        send_analysis_message(user.email)
        # consult_score(content)
        return render_template('register_client.html', status=True, message='Sua solicitação foi enviada com sucesso!\n'
                               'Após a analise você terá a resposta por e-mail.')
    return render_template('register_client.html', status=False, message='Erro na solicitação, verifique os campos!')


@app_views.route('/spouse/<_id>/register', methods=['POST', 'GET'])
def spouse_register_view(_id):
    user = get_client_by_id(_id)
    if user:
        if request.method == 'GET':
            return render_template('register_spouse.html', id=_id, status=True)

        content = request.values
        files = request.files
        if files.get('wedding_file'):
            spouse = create_spouse(content, files)
            if spouse:
                update_user(_id, {'spouse_id': spouse.id, 'wedding_file': files.get('wedding_file')})
                if create_request(_id):
                    send_analysis_message(user.email)
                    return render_template('register_spouse.html', status=True, message='Sua solicitação '
                                           'foi enviada com sucesso!\nApós a analise você terá a resposta por e-mail.')

        return render_template('register_spouse.html', status=False,
                               message='Erro na solicitação, verifique os campos!')
    return redirect('/register')


@app_views.route('/1qe1wr3etmnb3r3ety1ym/nb3vcXxzs2b3r3etyh48yt94j/<id_>', methods=['POST', 'GET'])
def link_to_approve(id_: str):
    render_template('/approve.html')
    to_approve(id_)
    return jsonify({}), 200


@app_views.route('/3ety1ymnbmnb3r3ety1ym/nb3vcXxzs2dwrmnb3vcXeyt94j/<id_>', methods=['POST', 'GET'])
def link_to_disapprove(id_: str):

    render_template('/disapprove.html')
    to_disapprove(id_)
    return jsonify({}), 200
