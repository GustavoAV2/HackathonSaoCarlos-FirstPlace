from uuid import uuid4
from database import db


class Groups(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    active = db.Column(db.Boolean(), default=True)

    def serialize(self):
        return {
                'id': self.id,
                'name': self.email,
                'active': self.active
                }
