from uuid import uuid4
from database import db
from sqlalchemy.orm import relationship, backref


class Spouse(db.Model):
    __tablename__ = 'spouse'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String(150), nullable=False, unique=False)
    last_name = db.Column(db.String(150), nullable=False, unique=False)
    email = db.Column(db.String(84), nullable=False, unique=False)
    cpf_or_cnpj = db.Column(db.String(16), nullable=False, unique=True)
    legal_person = db.Column(db.Boolean(), default=False)
    rg = db.Column(db.String(20), nullable=False, unique=False)

    income_tax_file = db.Column(db.String(200), nullable=True, unique=False)

    def serialize(self):
        return {
                'id': self.id,
                'email': self.email,
                'active': self.active
                }
