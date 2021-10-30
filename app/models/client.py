from uuid import uuid4
from database import db


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String(150), nullable=False, unique=True)
    last_name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(84), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    address = db.Column(db.String(150), nullable=False, unique=True)
    cep = db.Column(db.String(10), nullable=False, unique=True)
    cpf = db.Column(db.String(16), nullable=False, unique=True)
    legal_person = db.Column(db.Boolean(), default=True)

    rg_file = db.Column(db.String(200), nullable=False, unique=True)
    birth_file = db.Column(db.String(200), nullable=False, unique=True)
    wedding_file = db.Column(db.String(200), nullable=False, unique=True)
    residence_file = db.Column(db.String(200), nullable=False, unique=True)
    income_tax_file = db.Column(db.String(200), nullable=False, unique=True)

    def serialize(self):
        return {
                'id': self.id,
                'email': self.email,
                'active': self.active
                }
