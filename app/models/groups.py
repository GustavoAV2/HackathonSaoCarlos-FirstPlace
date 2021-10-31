from uuid import uuid4
from database import db
from sqlalchemy.orm import relationship, backref


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False, unique=True)
    active = db.Column(db.Boolean(), default=True)

    users = relationship("User", backref=backref("users", uselist=True))

    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'active': self.active
                }
