from werkzeug.utils import secure_filename
from uuid import uuid4
from app.models.users import User
from app.actions.client_actions import create_client, save_file, download_file_save
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

        file2_received = request.files['file2']

        file3_received = request.files['file3']

        files_saved = download_file_save(id_user, file1_received, file2_received, file3_received)
        content = request.values
        create_client(content, id_user, files_saved[0], files_saved[1], files_saved[2])
        # consult_score(content)
    return render_template('register.html', status=True)

