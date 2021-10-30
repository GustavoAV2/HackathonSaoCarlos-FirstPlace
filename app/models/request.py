from uuid import uuid4
from database import db
from sqlalchemy.orm import relationship, backref


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    approved = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean(), default=True)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = relationship("Client", backref=backref("clients", uselist=False))

    def serialize(self):
        return {
                'id': self.id,
                'name': self.email,
                'active': self.active
                }
