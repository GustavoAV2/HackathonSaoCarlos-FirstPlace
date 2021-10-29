from flask import Blueprint, render_template


app_views = Blueprint('views', __name__)


# Templates
@app_views.route('/', methods=['GET'])
def home():
    return render_template('index.html')
