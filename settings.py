import os

from dotenv import load_dotenv

load_dotenv()

FLASK_APP = 'run'
DEBUG = os.getenv('DEBUG', True)
SECRET_KEY = os.getenv('SECRET_KEY', 'a0D7oFka0D7vmv1nAjv1NaXpOLIq')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '5Fka0D7op5nsNgZa9vmv1nAjNXpOLIq')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///../database.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', True)
HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 5000)
EMAIL = os.getenv('EMAIL', 'bestcenterempreendimentos@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'adminsenha1')
FILE_UPLOAD = os.getenv('FILE_UPLOAD', 'upload\\')
URL_APP = os.getenv('URL_APP', 'http://localhost:5000/')

COMPANY_CREATION_DATE_CRITERIA = {'Muito bom': 10, "Bom": 5, 'Ruim': 2, 'Muito ruim': 0}
ALLOWED_CPF_CNPJ_SITUATIONS = {'Regular', 'Pendente de regularização'}  # outros: 'Suspensa', 'Cancelada', 'Nula'
APPROVAL_POINTS = {10: 'Aprovado com baixo risco', 7: 'Aprovado com alto risco', 5: 'Não aprovado'}
