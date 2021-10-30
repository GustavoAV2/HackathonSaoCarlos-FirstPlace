from database import db
from app.models.base import Base


class Client(Base, db.Model):
    __tablename__ = 'clients'

    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(84), nullable=False, unique=True)
    address = db.Column(db.String(150), nullable=False, unique=True)
    cep = db.Column(db.String(10), nullable=False, unique=True)
    cpf = db.Column(db.String(16), nullable=False, unique=True)
    legal_person = db.Column(db.Boolean(), default=True)

    document = db.Column(db.String(200), nullable=False, unique=True)
    document2 = db.Column(db.String(200), nullable=False, unique=True)
    document3 = db.Column(db.String(200), nullable=False, unique=True)

    def serialize(self):
        return {
                'id': self.id,
                'email': self.email,
                'active': self.active
                }
