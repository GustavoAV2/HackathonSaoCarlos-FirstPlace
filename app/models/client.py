from uuid import uuid4
from database import db
from sqlalchemy.orm import relationship, backref


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String(150), nullable=False, unique=False)
    last_name = db.Column(db.String(150), nullable=False, unique=False)
    email = db.Column(db.String(84), nullable=False, unique=False)
    phone = db.Column(db.String(20), nullable=True, unique=True)
    address = db.Column(db.String(150), nullable=True, unique=False)
    cep = db.Column(db.String(10), nullable=True, unique=False)
    cpf_or_cnpj = db.Column(db.String(16), nullable=False, unique=True)
    rg = db.Column(db.String(20), nullable=False, unique=False)
    legal_person = db.Column(db.Boolean(), default=True)

    financial_registration_approval = db.Column(db.Boolean(), default=False)

    spouse_id = db.Column(db.Integer, db.ForeignKey('spouse.id'))
    spouse = relationship("Spouse", backref=backref("spouse", uselist=False))
    request = relationship("Request", backref=backref("requests", uselist=False))

    birth_file = db.Column(db.String(200), nullable=False, unique=False)
    wedding_file = db.Column(db.String(200), nullable=True, unique=False)
    residence_file = db.Column(db.String(200), nullable=False, unique=False)
    income_tax_file = db.Column(db.String(200), nullable=False, unique=False)

    def serialize(self):
        return {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'cpf_or_cnpj': self.cpf_or_cnpj,
                'rg': self.rg,
                'address': self.address,
                'phone': self.phone,
                'email': self.email,
                'active': self.active
                }
