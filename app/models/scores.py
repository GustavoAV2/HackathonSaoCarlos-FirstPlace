from uuid import uuid4

from sqlalchemy.orm import relationship, backref

from database import db


class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)

    cpf_or_cnpj_situation = db.Column(db.String(84), default="")
    company_creation_date = db.Column(db.String(84), default="")

    serasa_score = db.Column(db.Integer)
    serasa_pendency = db.Column(db.String(84), nullable=False, default="")

    final_approve = db.Column(db.String(84), nullable=False, default="pendente de aprovação")
    risk_level = db.Column(db.String(84), nullable=False, default="")

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = relationship("Client", backref=backref("clients_scores", uselist=False))

    def serialize(self):
        return {
            'id': self.id,
            'first_approved': self.email,
            'second_approved': self.second_approved,
            'third_approved': self.third_approved,
            'final_approve': self.final_approve
        }
