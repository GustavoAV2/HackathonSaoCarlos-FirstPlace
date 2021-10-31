from uuid import uuid4

from sqlalchemy.orm import relationship, backref

from database import db


class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    # housing_value = db.Column(db.Float, default=0)
    # car_value = db.Column(db.Float, default=0)
    # salary = db.Column(db.Float, default=0)
    # patrimony = db.Column(db.Float, default=0)

    cpf_or_cnpj_situation = db.Column(db.Boolean(), default=True)
    company_creation_date = db.Column(db.String(84), default="")

    risk_level = db.Column(db.String(84), nullable=False, default="")

    first_approved = db.Column(db.String(84), nullable=False, default="não aprovado")
    second_approved = db.Column(db.String(84), nullable=False, default="não aprovado")
    third_approved = db.Column(db.String(84), nullable=False, default="não aprovado")

    final_approve = db.Column(db.String(84), nullable=False, default="não aprovado")

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = relationship("Client", backref=backref("clients", uselist=False))

    def serialize(self):
        return {
            'id': self.id,
            'first_approved': self.email,
            'second_approved': self.second_approved,
            'third_approved': self.third_approved,
            'final_approve': self.final_approve
        }
