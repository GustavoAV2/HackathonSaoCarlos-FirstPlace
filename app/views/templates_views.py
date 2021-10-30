from app.models.users import User
from app.actions.groups_actions import get_groups
from app.actions.client_actions import create_client
from app.actions.users_actions import login, create_user
from flask import Blueprint, render_template, request, redirect

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
    create_client(content)
    # consult_score(content)
    return render_template('register_client.html', status=True)

