from app.models.users import User
from flask import Blueprint, render_template, request, redirect
from app.actions.users_actions import get_user_by_id, get_users, update_user, create_user, login, deleted_user


app_views = Blueprint('views', __name__)


# Templates
@app_views.route('/', methods=['GET'])
def home_view():
    _json = request.get_json()
    return render_template('index.html')


@app_views.route('/login', methods=['POST', 'GET'])
def login_view():
    if request.method == 'GET':
        return render_template('login_of.html', status=True)

    credentials = request.values
    if login(credentials.get('email'), credentials.get("password")):
        return redirect('/')
    return render_template('login_of.html', status=False)


@app_views.route('/register', methods=['POST', 'GET'])
def register_view():
    if request.method == 'GET':
        return render_template('register_of.html', status=True)

    content = request.values
    user: User = create_user(content)
    if user:
        if user.active:
            return redirect('/login')
    return render_template('register_of.html', status=False)

