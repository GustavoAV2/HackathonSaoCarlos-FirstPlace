from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user

from app.actions.users_actions import login_manager
from app.models.users import User
from database import db, migrate
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.views.users_views import app_users
from app.views.templates_views import app_views


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('settings')
    JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)
    _register_blueprint(app)
    create_admin_view(app)
    login_manager.init_app(app)
    return app


def _register_blueprint(app: Flask):
    app.register_blueprint(app_users)
    app.register_blueprint(app_views)

def create_admin_view(app):
    admin = Admin(app)
    admin.add_view(AdminView(User, db.session))

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated