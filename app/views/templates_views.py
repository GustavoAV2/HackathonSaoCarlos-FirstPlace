from werkzeug.utils import secure_filename
from uuid import uuid4
from app.models.users import User
from app.actions.client_actions import create_client
from app.actions.users_actions import login, create_user
from flask import Blueprint, render_template, request, redirect
import os
import time

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


@app_views.route('/user/register', methods=['POST', 'GET'])
def user_register_view():
    if request.method == 'GET':
        return render_template('register_of.html', status=True)

    content = request.values
    user: User = create_user(content)
    if user:
        if user.active:
            return redirect('/login')
    return render_template('register_of.html', status=False)


@app_views.route('/register', methods=['POST', 'GET'])
def register_view():
    id_user = str(uuid4())
    if request.method == 'GET':
        return render_template('register.html', status=True)
    if request.method == 'POST':
        file1_received = request.files['file1']
        file_saved1 = save_file(file1_received, id_user)

        file2_received = request.files['file2']
        file_saved2 = save_file(file2_received, id_user)

        file3_received = request.files['file3']
        file3_saved = save_file(file3_received, id_user)
        content = request.values
        create_client(content, id_user, file_saved1, file_saved2, file3_saved)
        # consult_score(content)
    return render_template('register.html', status=True)


def save_file(file, user_id):
    upload_folder = os.path.join(os.getcwd(), f'upload\\{user_id}')
    try:
        os.mkdir(upload_folder)
        time.sleep(0.2)
    except (FileExistsError, FileNotFoundError):
        pass
    save_path = os.path.join(upload_folder, secure_filename(file.filename))
    try:
        file.save(save_path)
    except (FileExistsError, FileNotFoundError):
        pass
    print(upload_folder[-43:]+"\\"+file.filename)
    return upload_folder
