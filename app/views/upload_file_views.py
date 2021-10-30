import os
import time

from flask import render_template, request, redirect, Blueprint
from werkzeug.utils import secure_filename

app_upload_file = Blueprint('upload', __name__)


@app_upload_file.route('/upload_file')
def upload_file():
    return render_template('upload_file.html')


@app_upload_file.route('/upload', methods=['POST'])
def upload(user_id):
    file = request.files['file']
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
        redirect('/upload_file')
    return redirect('/upload_file')
